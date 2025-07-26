#!/bin/bash

# Automated Database Setup Script for StoryGrow
# This script moves database files to backend and sets up Cloud SQL

echo "==================================="
echo "StoryGrow Database Setup Automation"
echo "==================================="

# Check if we're in the frontend directory
if [[ ! "$PWD" =~ "frontend" ]]; then
    echo "Please run this script from the frontend directory"
    exit 1
fi

# Move database files to backend
echo "Moving database files to backend directory..."
mv cloud_sql_schema.sql ../backend/ 2>/dev/null && echo "✓ Moved cloud_sql_schema.sql" || echo "⚠ cloud_sql_schema.sql not found or already moved"
mv database_schema.sql ../backend/ 2>/dev/null && echo "✓ Moved database_schema.sql" || echo "⚠ database_schema.sql not found or already moved"
mv database_setup_instructions.md ../backend/ 2>/dev/null && echo "✓ Moved database_setup_instructions.md" || echo "⚠ database_setup_instructions.md not found or already moved"
mv setup_cloud_sql.sh ../backend/ 2>/dev/null && echo "✓ Moved setup_cloud_sql.sh" || echo "⚠ setup_cloud_sql.sh not found or already moved"

# Navigate to backend
echo ""
echo "Navigating to backend directory..."
cd ../backend

# Set the project
echo "Setting Google Cloud project..."
gcloud config set project storygrow-2

# Create the database if it doesn't exist
echo ""
echo "Creating 'storygrow' database if it doesn't exist..."
gcloud sql databases create storygrow --instance=database-storygrow 2>/dev/null && echo "✓ Database created" || echo "✓ Database already exists"

# Create a temporary file with all SQL commands
echo ""
echo "Preparing database schema..."
cat > /tmp/auto_setup.sql << 'EOF'
-- First, drop existing objects for clean setup (optional)
DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS emotion_type CASCADE;
DROP TYPE IF EXISTS story_status CASCADE;
DROP TYPE IF EXISTS alert_severity CASCADE;

-- Now include the main schema
\i cloud_sql_schema.sql

-- Verify setup
\echo ''
\echo '==================================='
\echo 'Tables created:'
\echo '==================================='
\dt

\echo ''
\echo '==================================='
\echo 'Database setup complete!'
\echo '==================================='
EOF

# Execute the setup
echo ""
echo "Connecting to database and executing schema..."
echo "You will be prompted for the postgres password."
echo ""
gcloud sql connect database-storygrow --user=postgres --database=storygrow < /tmp/auto_setup.sql

# Clean up
rm /tmp/auto_setup.sql

# Create a simple test script
cat > test_database_connection.sql << 'EOF'
-- Test database connection
SELECT 'Database connection successful!' as message;
SELECT current_database() as database, current_user as user;
SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = 'public';
EOF

echo ""
echo "==================================="
echo "✓ Setup Complete!"
echo "==================================="
echo ""
echo "Database files have been moved to: $(pwd)"
echo "Database 'storygrow' has been created in instance 'database-storygrow'"
echo ""
echo "To test the connection, run:"
echo "gcloud sql connect database-storygrow --user=postgres --database=storygrow < test_database_connection.sql"
echo ""
echo "To connect manually:"
echo "gcloud sql connect database-storygrow --user=postgres --database=storygrow"