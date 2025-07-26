#!/bin/bash
echo "Testing Cloud SQL connection..."
echo "Password is: ChangeMeNow123!"
echo ""

# Create a SQL file with the test query
cat > /tmp/test_query.sql << 'EOF'
SELECT 'Connection successful!' as status;
SELECT current_database() as database, current_user as user;
SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = 'public';
SELECT tablename FROM pg_tables WHERE schemaname = 'public' LIMIT 5;
EOF

# Connect and run the test
gcloud sql connect storygrow-database --user=postgres --database=storygrow < /tmp/test_query.sql

# Clean up
rm /tmp/test_query.sql