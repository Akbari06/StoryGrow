-- StoryGrow Database Schema for Supabase/PostgreSQL
-- This script creates all tables, relationships, and Row Level Security policies

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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

-- Users table (extends Supabase auth.users)
CREATE TABLE public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
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

-- AI Analysis table (for storing AI insights)
CREATE TABLE public.ai_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    story_id UUID REFERENCES public.stories(id) ON DELETE CASCADE,
    voice_recording_id UUID REFERENCES public.voice_recordings(id) ON DELETE CASCADE,
    analysis_type TEXT NOT NULL, -- 'emotion', 'theme', 'concern'
    content JSONB NOT NULL,
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

-- ==============================================
-- ROW LEVEL SECURITY (RLS)
-- ==============================================

-- Enable RLS on all tables
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.parents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.kids ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.stories ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.story_scenes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.voice_recordings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.emotion_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_analysis ENABLE ROW LEVEL SECURITY;

-- ==============================================
-- HELPER FUNCTIONS
-- ==============================================

-- Function to get user role
CREATE OR REPLACE FUNCTION public.get_user_role()
RETURNS user_role AS $$
BEGIN
    RETURN (
        SELECT role 
        FROM public.users 
        WHERE id = auth.uid()
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to check if user is parent of kid
CREATE OR REPLACE FUNCTION public.is_parent_of(kid_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 
        FROM public.kids k
        JOIN public.parents p ON k.parent_id = p.id
        WHERE k.id = kid_id 
        AND p.user_id = auth.uid()
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get parent's kids
CREATE OR REPLACE FUNCTION public.get_my_kids()
RETURNS SETOF UUID AS $$
BEGIN
    RETURN QUERY
    SELECT k.id
    FROM public.kids k
    JOIN public.parents p ON k.parent_id = p.id
    WHERE p.user_id = auth.uid();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ==============================================
-- ROW LEVEL SECURITY POLICIES
-- ==============================================

-- Users table policies
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (id = auth.uid() OR get_user_role() = 'admin');

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (id = auth.uid());

-- Parents table policies
CREATE POLICY "Parents can view own record" ON public.parents
    FOR SELECT USING (user_id = auth.uid() OR get_user_role() = 'admin');

CREATE POLICY "Parents can update own record" ON public.parents
    FOR UPDATE USING (user_id = auth.uid());

-- Kids table policies
CREATE POLICY "Parents can view their kids" ON public.kids
    FOR SELECT USING (
        parent_id IN (SELECT id FROM public.parents WHERE user_id = auth.uid())
        OR get_user_role() = 'admin'
    );

CREATE POLICY "Kids can view own profile" ON public.kids
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Parents can create kids" ON public.kids
    FOR INSERT WITH CHECK (
        parent_id IN (SELECT id FROM public.parents WHERE user_id = auth.uid())
    );

CREATE POLICY "Parents can update their kids" ON public.kids
    FOR UPDATE USING (
        parent_id IN (SELECT id FROM public.parents WHERE user_id = auth.uid())
    );

-- Stories table policies
CREATE POLICY "Kids can view own stories" ON public.stories
    FOR SELECT USING (
        kid_id IN (SELECT id FROM public.kids WHERE user_id = auth.uid())
    );

CREATE POLICY "Parents can view their kids stories" ON public.stories
    FOR SELECT USING (
        kid_id IN (SELECT id FROM get_my_kids())
        OR get_user_role() = 'admin'
    );

CREATE POLICY "Kids can create stories" ON public.stories
    FOR INSERT WITH CHECK (
        kid_id IN (SELECT id FROM public.kids WHERE user_id = auth.uid())
    );

-- Story scenes policies
CREATE POLICY "Can view scenes of accessible stories" ON public.story_scenes
    FOR SELECT USING (
        story_id IN (
            SELECT id FROM public.stories 
            WHERE kid_id IN (SELECT id FROM public.kids WHERE user_id = auth.uid())
            OR kid_id IN (SELECT id FROM get_my_kids())
        )
        OR get_user_role() = 'admin'
    );

-- Voice recordings policies
CREATE POLICY "Kids can create own recordings" ON public.voice_recordings
    FOR INSERT WITH CHECK (
        kid_id IN (SELECT id FROM public.kids WHERE user_id = auth.uid())
    );

CREATE POLICY "Can view recordings" ON public.voice_recordings
    FOR SELECT USING (
        kid_id IN (SELECT id FROM public.kids WHERE user_id = auth.uid())
        OR kid_id IN (SELECT id FROM get_my_kids())
        OR get_user_role() = 'admin'
    );

-- Emotion logs policies
CREATE POLICY "Parents can view their kids emotions" ON public.emotion_logs
    FOR SELECT USING (
        kid_id IN (SELECT id FROM get_my_kids())
        OR get_user_role() = 'admin'
    );

CREATE POLICY "System can insert emotion logs" ON public.emotion_logs
    FOR INSERT WITH CHECK (true); -- Will be restricted by API

-- Alerts policies
CREATE POLICY "Parents can view own alerts" ON public.alerts
    FOR SELECT USING (
        parent_id IN (SELECT id FROM public.parents WHERE user_id = auth.uid())
    );

CREATE POLICY "Parents can update own alerts" ON public.alerts
    FOR UPDATE USING (
        parent_id IN (SELECT id FROM public.parents WHERE user_id = auth.uid())
    );

-- AI Analysis policies
CREATE POLICY "Parents can view analysis for their kids" ON public.ai_analysis
    FOR SELECT USING (
        story_id IN (
            SELECT id FROM public.stories 
            WHERE kid_id IN (SELECT id FROM get_my_kids())
        )
        OR get_user_role() = 'admin'
    );

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

-- ==============================================
-- INITIAL DATA (Optional)
-- ==============================================

-- Create admin user (you'll need to create this user in Supabase Auth first)
-- INSERT INTO public.users (id, email, role, full_name) 
-- VALUES ('YOUR-ADMIN-UUID', 'admin@storygrow.com', 'admin', 'Admin User');