# StoryGrow Database Setup Instructions

## Prerequisites
- Supabase project created
- Access to Supabase SQL Editor or psql CLI

## Setup Steps

### 1. Execute the Schema
Run the `database_schema.sql` file in your Supabase SQL editor or via terminal:

```bash
# Via Supabase CLI
supabase db push database_schema.sql

# Or via psql
psql -h <your-supabase-host> -U postgres -d postgres -f database_schema.sql
```

### 2. Configure Authentication

In Supabase Dashboard:
1. Go to Authentication → Providers
2. Enable Email authentication
3. Configure email templates for kids-friendly messages

### 3. Create Storage Buckets

In Supabase Dashboard → Storage:

```sql
-- Run in SQL Editor to create storage buckets
INSERT INTO storage.buckets (id, name, public)
VALUES 
  ('story-images', 'story-images', true),
  ('voice-recordings', 'voice-recordings', false),
  ('avatars', 'avatars', true);
```

### 4. Set Storage Policies

```sql
-- Story images bucket - public read
CREATE POLICY "Public can view story images" ON storage.objects
  FOR SELECT USING (bucket_id = 'story-images');

CREATE POLICY "Authenticated can upload story images" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'story-images' 
    AND auth.role() = 'authenticated'
  );

-- Voice recordings bucket - private
CREATE POLICY "Users can upload own recordings" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'voice-recordings' 
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can view own recordings" ON storage.objects
  FOR SELECT USING (
    bucket_id = 'voice-recordings' 
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

-- Parents can view their kids' recordings
CREATE POLICY "Parents can view kids recordings" ON storage.objects
  FOR SELECT USING (
    bucket_id = 'voice-recordings'
    AND EXISTS (
      SELECT 1 FROM public.kids k
      JOIN public.parents p ON k.parent_id = p.id
      WHERE p.user_id = auth.uid()
      AND k.id::text = (storage.foldername(name))[1]
    )
  );
```

### 5. Create Initial Admin User

1. Create user in Supabase Auth
2. Then run:

```sql
INSERT INTO public.users (id, email, role, full_name) 
VALUES ('<auth-user-id>', 'admin@storygrow.com', 'admin', 'Admin User');
```

### 6. Environment Variables

Add to your `.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-key
```

## Database Schema Overview

### User Roles
- **Admin**: Full access to all data
- **Parent**: Can manage their kids, view stories, emotions, and receive alerts
- **Kid**: Can create stories, record voice, limited profile access

### Key Tables
1. **users**: Base user table linked to Supabase Auth
2. **parents**: Parent-specific data and preferences
3. **kids**: Child profiles linked to parents
4. **stories**: Story metadata and status
5. **story_scenes**: Individual scenes with text and images
6. **voice_recordings**: Audio recordings with transcripts
7. **emotion_logs**: Mood tracking over time
8. **alerts**: Parent notifications for concerning patterns
9. **ai_analysis**: AI-generated insights

### Security Features
- Row Level Security (RLS) enabled on all tables
- Parents can only see their own children's data
- Kids can only access their own content
- Admin role for support and monitoring

## Testing the Setup

### 1. Create Test Parent
```sql
-- First create auth user, then:
INSERT INTO public.users (id, email, role, full_name) 
VALUES ('<auth-id>', 'parent@test.com', 'parent', 'Test Parent');

INSERT INTO public.parents (user_id) 
VALUES ('<auth-id>');
```

### 2. Create Test Kid
```sql
INSERT INTO public.kids (parent_id, name, age, avatar_emoji) 
VALUES (
  (SELECT id FROM public.parents WHERE user_id = '<parent-auth-id>'),
  'Emma',
  7,
  '🦄'
);
```

### 3. Test RLS Policies
```sql
-- As parent user, should see their kid
SELECT * FROM public.kids;

-- As different user, should see nothing
SELECT * FROM public.kids;
```

## Monitoring & Maintenance

### Regular Tasks
1. Monitor emotion_logs for concerning patterns
2. Clean up old voice recordings (storage management)
3. Archive completed stories older than 6 months
4. Review AI analysis for accuracy

### Useful Queries

```sql
-- Kids with recent concerning emotions
SELECT k.name, COUNT(*) as concern_count
FROM public.kids k
JOIN public.emotion_logs e ON k.id = e.kid_id
WHERE e.emotion IN ('sad', 'angry', 'scared', 'worried')
  AND e.created_at > NOW() - INTERVAL '7 days'
  AND e.intensity >= 4
GROUP BY k.id, k.name
HAVING COUNT(*) > 3;

-- Storage usage by kid
SELECT k.name, COUNT(vr.id) as recordings, SUM(vr.duration_seconds) as total_seconds
FROM public.kids k
LEFT JOIN public.voice_recordings vr ON k.id = vr.kid_id
GROUP BY k.id, k.name;
```