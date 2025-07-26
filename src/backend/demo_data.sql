-- Demo data for StoryGrow with hardcoded UUIDs
-- Run this after creating the database schema

-- Create demo auth users
INSERT INTO public.auth_users (id, email, encrypted_password) VALUES
  ('11111111-1111-1111-1111-111111111111', 'demo@parent.com', 'demo_password_hash'),
  ('22222222-2222-2222-2222-222222222222', 'demo@child.com', 'demo_password_hash')
ON CONFLICT (id) DO NOTHING;

-- Create demo users
INSERT INTO public.users (id, email, role, full_name) VALUES
  ('11111111-1111-1111-1111-111111111111', 'demo@parent.com', 'parent', 'Demo Parent'),
  ('22222222-2222-2222-2222-222222222222', 'demo@child.com', 'kid', 'Demo Child')
ON CONFLICT (id) DO NOTHING;

-- Create demo parent
INSERT INTO public.parents (id, user_id) VALUES
  ('33333333-3333-3333-3333-333333333333', '11111111-1111-1111-1111-111111111111')
ON CONFLICT (id) DO NOTHING;

-- Create demo kid with UUID that matches our hardcoded 'demo_child_123'
-- We'll use a deterministic UUID based on the string
INSERT INTO public.kids (id, user_id, parent_id, name, age, avatar_emoji) VALUES
  ('44444444-4444-4444-4444-444444444444', '22222222-2222-2222-2222-222222222222', '33333333-3333-3333-3333-333333333333', 'Demo Kid', 7, '🦄')
ON CONFLICT (id) DO NOTHING;

-- Create a view to map our demo IDs
CREATE OR REPLACE VIEW demo_id_mapping AS
SELECT 
  'demo_child_123' as demo_id,
  '44444444-4444-4444-4444-444444444444'::uuid as real_id,
  'kid' as type
UNION ALL
SELECT 
  'demo_parent_456' as demo_id,
  '33333333-3333-3333-3333-333333333333'::uuid as real_id,
  'parent' as type;