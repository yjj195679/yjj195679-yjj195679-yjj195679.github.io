-- Guestbook replies and MFA-protected administrator access.
-- Run only after creating the intended administrator in Supabase Auth.

alter table public.messages
  add column if not exists reply varchar(1000),
  add column if not exists replied_at timestamptz;

do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conrelid = 'public.messages'::regclass
      and conname = 'messages_reply_length'
  ) then
    alter table public.messages
      add constraint messages_reply_length
      check (reply is null or char_length(reply) between 1 and 1000);
  end if;

  if not exists (
    select 1 from pg_constraint
    where conrelid = 'public.messages'::regclass
      and conname = 'messages_reply_timestamp_consistency'
  ) then
    alter table public.messages
      add constraint messages_reply_timestamp_consistency
      check ((reply is null and replied_at is null) or (reply is not null and replied_at is not null));
  end if;
end
$$;

-- This repository uses one pre-existing Auth user. For a multi-user project,
-- replace the subquery with an explicit, verified user UUID.
update auth.users
set raw_app_meta_data = coalesce(raw_app_meta_data, '{}'::jsonb) || '{"role":"admin"}'::jsonb
where id = (select id from auth.users order by created_at limit 1)
  and (select count(*) from auth.users) = 1;

grant select on table public.messages to authenticated;
grant update (reply, replied_at, is_visible) on table public.messages to authenticated;

drop policy if exists public_read_visible_messages on public.messages;
drop policy if exists public_read_visible_messages_anon on public.messages;
drop policy if exists authenticated_read_messages on public.messages;
drop policy if exists admin_read_all_messages on public.messages;
drop policy if exists public_create_messages on public.messages;

create policy public_read_visible_messages_anon
on public.messages
for select
to anon
using (is_visible = true);

create policy authenticated_read_messages
on public.messages
for select
to authenticated
using (
  is_visible = true
  or (
    ((select auth.jwt())->'app_metadata'->>'role') = 'admin'
    and ((select auth.jwt())->>'aal') = 'aal2'
  )
);

drop policy if exists admin_update_messages on public.messages;
create policy admin_update_messages
on public.messages
for update
to authenticated
using (
  ((select auth.jwt())->'app_metadata'->>'role') = 'admin'
  and ((select auth.jwt())->>'aal') = 'aal2'
)
with check (
  ((select auth.jwt())->'app_metadata'->>'role') = 'admin'
  and ((select auth.jwt())->>'aal') = 'aal2'
);

-- Public submissions use a private trigger with server-side volume limits.

create schema if not exists private;
revoke all on schema private from public, anon, authenticated;

create or replace function private.enforce_guestbook_submission()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  new.name := btrim(new.name);
  new.content := btrim(new.content);

  perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtext('true-path-m:guestbook-submit'));

  if (select count(*) from public.messages where created_at >= pg_catalog.now() - interval '1 minute') >= 12
     or (select count(*) from public.messages where created_at >= pg_catalog.now() - interval '1 day') >= 150 then
    raise sqlstate 'PGRST' using
      message = pg_catalog.json_build_object(
        'code', 'guestbook_rate_limited',
        'message', 'Guestbook rate limit reached.'
      )::text,
      detail = pg_catalog.json_build_object(
        'status', 429,
        'headers', pg_catalog.json_build_object('Retry-After', '60')
      )::text;
  end if;

  return new;
end;
$$;

revoke all on function private.enforce_guestbook_submission() from public, anon, authenticated;

drop trigger if exists enforce_guestbook_submission on public.messages;
create trigger enforce_guestbook_submission
before insert on public.messages
for each row execute function private.enforce_guestbook_submission();

drop function if exists public.submit_guestbook_message(text, text);

grant insert (name, content) on table public.messages to anon, authenticated;

drop policy if exists public_create_messages on public.messages;
create policy public_create_messages
on public.messages
for insert
to anon, authenticated
with check (
  is_visible = true
  and reply is null
  and replied_at is null
);
