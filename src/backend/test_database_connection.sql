-- Test database connection
SELECT 'Database connection successful!' as message;
SELECT current_database() as database, current_user as user;
SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = 'public';
