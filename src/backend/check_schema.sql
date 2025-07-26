-- Check actual schema of sessions table
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'sessions'
ORDER BY ordinal_position;

-- Check actual schema of stories table
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'stories'
ORDER BY ordinal_position;

-- Check actual schema of kids table
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'kids'
ORDER BY ordinal_position;