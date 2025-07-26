-- Insert demo data directly
-- Run this in SQL Studio to set up demo users

-- First, insert demo auth users
INSERT INTO auth_users (id, email, encrypted_password) VALUES
  ('11111111-1111-1111-1111-111111111111'::uuid, 'demo@parent.com', 'demo_password_hash'),
  ('22222222-2222-2222-2222-222222222222'::uuid, 'demo@child.com', 'demo_password_hash')
ON CONFLICT (id) DO NOTHING;

-- Insert demo users
INSERT INTO users (id, email, role, full_name) VALUES
  ('11111111-1111-1111-1111-111111111111'::uuid, 'demo@parent.com', 'parent', 'Demo Parent'),
  ('22222222-2222-2222-2222-222222222222'::uuid, 'demo@child.com', 'kid', 'Demo Child')
ON CONFLICT (id) DO NOTHING;

-- Insert demo parent
INSERT INTO parents (id, user_id) VALUES
  ('33333333-3333-3333-3333-333333333333'::uuid, '11111111-1111-1111-1111-111111111111'::uuid)
ON CONFLICT (id) DO NOTHING;

-- Insert demo kid
INSERT INTO kids (id, user_id, parent_id, name, age, avatar_emoji) VALUES
  ('44444444-4444-4444-4444-444444444444'::uuid, '22222222-2222-2222-2222-222222222222'::uuid, '33333333-3333-3333-3333-333333333333'::uuid, 'Demo Kid', 7, '🦄')
ON CONFLICT (id) DO NOTHING;

-- Verify the data
SELECT 'Users:' as table_name;
SELECT * FROM users;

SELECT 'Kids:' as table_name;
SELECT * FROM kids;

SELECT 'Parents:' as table_name;
SELECT * FROM parents;