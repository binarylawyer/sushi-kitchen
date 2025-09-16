# Database Schema — Sushi Kitchen (logical)

> Source of truth is Postgres (Supabase). Vector search via Qdrant.

## Postgres (DDL sketch)

```sql
-- Users (SSO-backed identities mirrored locally)
create table if not exists app_user (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  display_name text,
  created_at timestamptz default now()
);

-- API keys (scoped tokens) - if we issue local tokens
create table if not exists api_key (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references app_user(id) on delete cascade,
  name text not null,
  hash bytea not null,          -- never store raw
  scope text[] not null,        -- ['llm:read','rag:write',...]
  created_at timestamptz default now(),
  revoked_at timestamptz
);

-- Documents (RAG) metadata; content stored in MinIO; vectors in Qdrant
create table if not exists doc_asset (
  id uuid primary key default gen_random_uuid(),
  bucket text not null,         -- minio bucket
  object_key text not null,     -- path in bucket
  mime text,
  bytes bigint,
  sha256 text,
  created_by uuid references app_user(id),
  created_at timestamptz default now()
);

-- Render jobs (Ramen/Remotion)
create table if not exists render_job (
  id uuid primary key default gen_random_uuid(),
  kind text not null,           -- 'remotion' | 'ffmpeg'
  status text not null,         -- 'queued'|'running'|'done'|'error'
  params jsonb not null,        -- input settings (scenes, durations, assets)
  result_url text,              -- minio URL or path
  logs text,
  created_by uuid references app_user(id),
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
Qdrant
Collections:
docs_default — embeddings of doc_asset chunks
Payload: { doc_id, page, source, sha256, metadata }
