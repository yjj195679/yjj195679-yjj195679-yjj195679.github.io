-- Applied migration for 1956799.xyz writing vocabulary.
create table if not exists public.writing_word_progress(
 device_hash text primary key check(device_hash ~ '^[0-9a-f]{64}$'),
 marks jsonb not null default '{}'::jsonb,
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now(),
 constraint writing_word_progress_marks_object check(jsonb_typeof(marks)='object'),
 constraint writing_word_progress_marks_size check(octet_length(marks::text)<=8192)
);
alter table public.writing_word_progress enable row level security;
revoke all on table public.writing_word_progress from public, anon, authenticated;
grant select, insert, update on table public.writing_word_progress to service_role;