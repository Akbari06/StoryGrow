#!/bin/bash

# StoryGrow Cloud SQL Setup Script
# This script sets up the database schema in the existing Cloud SQL instance

echo "==================================="
echo "StoryGrow Cloud SQL Setup"
echo "Instance: database-storygrow"
echo "Project: storygrow-2"
echo "==================================="

# Set the project
echo "Setting project to storygrow-2..."
gcloud config set project storygrow-2

# Create the storygrow database if it doesn't exist
echo "Creating database 'storygrow' if not exists..."
gcloud sql databases create storygrow --instance=database-storygrow 2>/dev/null || echo "Database 'storygrow' already exists"

# Connect and execute the schema
echo "Connecting to database-storygrow to execute schema..."
echo "You will be prompted for the postgres password."
echo "Once connected, the schema will be automatically executed."

# Create a temporary SQL file that includes the schema
cat > /tmp/setup_storygrow.sql << 'EOF'
-- Connect to the storygrow database
\c storygrow

-- Drop existing types if they exist (for clean re-run)
DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS emotion_type CASCADE;
DROP TYPE IF EXISTS story_status CASCADE;
DROP TYPE IF EXISTS alert_severity CASCADE;

-- Execute the main schema
\i cloud_sql_schema.sql

-- Verify tables were created
\dt

-- Show success message
\echo 'Database schema created successfully!'
EOF

# Connect and run the setup
gcloud sql connect database-storygrow --user=postgres < /tmp/setup_storygrow.sql

# Clean up
rm /tmp/setup_storygrow.sql

echo "==================================="
echo "Setup complete!"
echo "==================================="
echo ""
echo "Connection details for your application:"
echo "Instance: database-storygrow"
echo "Database: storygrow"
echo ""
echo "To get the connection name for your app:"
echo "gcloud sql instances describe database-storygrow --format='value(connectionName)'"