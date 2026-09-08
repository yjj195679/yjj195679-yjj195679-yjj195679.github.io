-- Restore public submissions and enforce volume limits inside the database.

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
