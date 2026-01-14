-- GlobalVoice AI: Core Database Schema
-- Database: PostgreSQL 15+
-- Architect: db-arch | DB Architect
-- Description: Supports multi-tenant user projects, media asset versioning, and AI workflow tracking.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. USER MANAGEMENT
CREATE TYPE subscription_tier AS ENUM ('free', 'creator', 'pro', 'enterprise');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    tier subscription_tier DEFAULT 'free',
    api_key_hash TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. LANGUAGES & VOICES
CREATE TABLE languages (
    id VARCHAR(10) PRIMARY KEY, -- e.g., 'en-US', 'th-TH', 'ja-JP'
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE voices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id), -- NULL if public/system voice
    name VARCHAR(100) NOT NULL,
    language_id VARCHAR(10) REFERENCES languages(id),
    gender VARCHAR(20),
    reference_audio_s3_path TEXT, -- Path to the 15s-1min sample for cloning
    is_cloned BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. PROJECTS & MEDIA ASSETS
CREATE TYPE project_status AS EN_ENUM ('draft', 'processing', 'completed', 'failed');

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    source_language_id VARCHAR(10) REFERENCES languages(id),
    status project_status DEFAULT 'draft',
    metadata JSONB, -- Stores original duration, resolution, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TYPE asset_type AS ENUM ('original_video', 'extracted_audio', 'translated_audio', 'final_dub');

CREATE TABLE media_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    asset_type asset_type NOT NULL,
    s3_path TEXT NOT NULL,
    file_size_bytes BIGINT,
    mime_type VARCHAR(100),
    language_id VARCHAR(10) REFERENCES languages(id),
    version INT DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. TRANSCRIPTION & TRANSLATION
CREATE TABLE transcripts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    language_id VARCHAR(10) REFERENCES languages(id),
    content JSONB NOT NULL, -- Format: [{start: 0.0, end: 2.5, text: "...", speaker: "A"}]
    is_original BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. WORKFLOW ORCHESTRATION (Task Tracking)
CREATE TYPE task_status AS ENUM ('pending', 'queued', 'processing', 'completed', 'failed');
CREATE TYPE task_type AS ENUM ('ingestion', 'stt', 'nmt', 'tts', 'lip_sync', 'muxing');

CREATE TABLE workflow_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    task_type task_type NOT NULL,
    status task_status DEFAULT 'pending',
    worker_node_id VARCHAR(100), -- Identifies which GPU node is processing
    input_data JSONB,
    output_data JSONB,
    error_log TEXT,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- INDEXING for Performance
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_media_assets_project_id ON media_assets(project_id);
CREATE INDEX idx_workflow_tasks_status ON workflow_tasks(status);
CREATE INDEX idx_transcripts_project_id ON transcripts(project_id);