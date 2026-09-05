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
