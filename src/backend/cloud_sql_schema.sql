-- StoryGrow Database Schema for Google Cloud SQL (PostgreSQL)
-- For Cloud SQL Instance: database-storygrow
-- Database name: storygrow

-- Drop existing tables if doing a fresh install (comment out if updating)
-- DROP SCHEMA public CASCADE;
-- CREATE SCHEMA public;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ==============================================
-- USER ROLES AND TYPES
-- ==============================================

-- Create user role enum
CREATE TYPE user_role AS ENUM ('parent', 'kid', 'admin');

-- Create emotion enum for mood tracking
CREATE TYPE emotion_type AS ENUM ('happy', 'sad', 'angry', 'scared', 'excited', 'calm', 'worried', 'frustrated');

-- Create story status enum
CREATE TYPE story_status AS ENUM ('draft', 'generating', 'completed', 'failed');

-- Create alert severity enum
CREATE TYPE alert_severity AS ENUM ('low', 'medium', 'high', 'critical');

-- ==============================================
-- TABLES
-- ==============================================

-- Auth users table (replacing Supabase auth.users)
CREATE TABLE public.auth_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    encrypted_password TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Users table
CREATE TABLE public.users (
    id UUID PRIMARY KEY REFERENCES public.auth_users(id) ON DELETE CASCADE,
    email TEXT UNIQUE,
    role user_role NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Parents table
CREATE TABLE public.parents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    phone TEXT,
    notification_preferences JSONB DEFAULT '{"email": true, "sms": false, "alerts": true}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Kids table
CREATE TABLE public.kids (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    parent_id UUID NOT NULL REFERENCES public.parents(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    age INTEGER CHECK (age >= 3 AND age <= 12),
    avatar_emoji TEXT DEFAULT '🦄',
    preferences JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Stories table
CREATE TABLE public.stories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    kid_id UUID NOT NULL REFERENCES public.kids(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    prompt TEXT NOT NULL,
    status story_status DEFAULT 'draft',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Story scenes table
CREATE TABLE public.story_scenes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    story_id UUID NOT NULL REFERENCES public.stories(id) ON DELETE CASCADE,
    scene_number INTEGER NOT NULL,
    text TEXT NOT NULL,
    image_prompt TEXT,
    image_url TEXT,
    audio_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(story_id, scene_number)
);

-- Voice recordings table
CREATE TABLE public.voice_recordings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    kid_id UUID NOT NULL REFERENCES public.kids(id) ON DELETE CASCADE,
    story_id UUID REFERENCES public.stories(id) ON DELETE SET NULL,
    audio_url TEXT NOT NULL,
    transcript TEXT,
    duration_seconds INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Emotion tracking table
CREATE TABLE public.emotion_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    kid_id UUID NOT NULL REFERENCES public.kids(id) ON DELETE CASCADE,
    emotion emotion_type NOT NULL,
    intensity INTEGER CHECK (intensity >= 1 AND intensity <= 5),
    context TEXT,
    story_id UUID REFERENCES public.stories(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Parent alerts table
CREATE TABLE public.alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    parent_id UUID NOT NULL REFERENCES public.parents(id) ON DELETE CASCADE,
    kid_id UUID NOT NULL REFERENCES public.kids(id) ON DELETE CASCADE,
    type TEXT NOT NULL,
    severity alert_severity NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- AI Analysis table
CREATE TABLE public.ai_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    story_id UUID REFERENCES public.stories(id) ON DELETE CASCADE,
    voice_recording_id UUID REFERENCES public.voice_recordings(id) ON DELETE CASCADE,
    analysis_type TEXT NOT NULL,
    content JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Session management table
CREATE TABLE public.sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==============================================
-- INDEXES
-- ==============================================

CREATE INDEX idx_stories_kid_id ON public.stories(kid_id);
CREATE INDEX idx_stories_created_at ON public.stories(created_at DESC);
CREATE INDEX idx_emotion_logs_kid_id ON public.emotion_logs(kid_id);
CREATE INDEX idx_emotion_logs_created_at ON public.emotion_logs(created_at DESC);
CREATE INDEX idx_alerts_parent_id ON public.alerts(parent_id);
CREATE INDEX idx_alerts_is_read ON public.alerts(is_read);
CREATE INDEX idx_voice_recordings_kid_id ON public.voice_recordings(kid_id);
CREATE INDEX idx_sessions_token ON public.sessions(token);
CREATE INDEX idx_sessions_expires_at ON public.sessions(expires_at);

-- ==============================================
-- HELPER FUNCTIONS (Cloud SQL compatible)
-- ==============================================

-- Function to hash passwords
CREATE OR REPLACE FUNCTION public.hash_password(password TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN crypt(password, gen_salt('bf'));
END;
$$ LANGUAGE plpgsql;

-- Function to verify passwords
CREATE OR REPLACE FUNCTION public.verify_password(password TEXT, hash TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN hash = crypt(password, hash);
END;
$$ LANGUAGE plpgsql;

-- ==============================================
-- TRIGGERS
-- ==============================================

-- Update timestamp trigger
CREATE OR REPLACE FUNCTION public.update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_kids_updated_at BEFORE UPDATE ON public.kids
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_stories_updated_at BEFORE UPDATE ON public.stories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_auth_users_updated_at BEFORE UPDATE ON public.auth_users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ==============================================
-- INITIAL ADMIN USER
-- ==============================================

-- Create initial admin user (change password!)
INSERT INTO public.auth_users (email, encrypted_password) 
VALUES ('admin@storygrow.com', crypt('ChangeThisPassword123!', gen_salt('bf')))
RETURNING id;

-- Use the returned ID to create the user profile
-- INSERT INTO public.users (id, email, role, full_name) 
-- VALUES ('<returned-id>', 'admin@storygrow.com', 'admin', 'Admin User');