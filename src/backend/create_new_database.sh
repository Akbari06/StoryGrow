#!/bin/bash

# StoryGrow - Create New Cloud SQL Database
# This script creates a new Cloud SQL instance and sets up the database

echo "=========================================="
echo "StoryGrow - Creating New Cloud SQL Database"
echo "=========================================="
echo ""
echo "Project: storygrow-2"
echo "Account: storygrow3000@gmail.com"
echo ""

# Ensure we're in the correct project
echo "Setting project to storygrow-2..."
gcloud config set project storygrow-2

# Enable required APIs
echo ""
echo "Enabling required APIs..."
gcloud services enable sqladmin.googleapis.com
gcloud services enable sql-component.googleapis.com
gcloud services enable sql-admin.googleapis.com

# Create Cloud SQL instance
echo ""
echo "Creating Cloud SQL PostgreSQL instance..."
echo "This will take 5-10 minutes..."
gcloud sql instances create storygrow-database \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=europe-west1 \
  --root-password=ChangeMeNow123! \
  --database-flags=cloudsql.iam_authentication=on \
  --backup \
  --backup-start-time=03:00 \
  --maintenance-window-day=SUN \
  --maintenance-window-hour=04

# Wait for instance to be ready
echo ""
echo "Waiting for instance to be ready..."
sleep 10

# Create the database
echo ""
echo "Creating 'storygrow' database..."
gcloud sql databases create storygrow \
  --instance=storygrow-database

# Get connection details
echo ""
echo "Getting connection details..."
CONNECTION_NAME=$(gcloud sql instances describe storygrow-database --format='value(connectionName)')
PUBLIC_IP=$(gcloud sql instances describe storygrow-database --format='value(ipAddresses[0].ipAddress)')

# Create environment variables file for backend
echo ""
echo "Creating environment configuration..."
cat > ../backend/.env.cloud_sql << EOF
# Cloud SQL Configuration
INSTANCE_CONNECTION_NAME=$CONNECTION_NAME
DB_USER=postgres
DB_PASSWORD=ChangeMeNow123!
DB_NAME=storygrow
DB_HOST=$PUBLIC_IP
DB_PORT=5432

# For Cloud Run deployment
INSTANCE_UNIX_SOCKET=/cloudsql/$CONNECTION_NAME
EOF

# Execute the schema
echo ""
echo "Setting up database schema..."
echo "Password is: ChangeMeNow123!"
echo ""

# Create a combined setup SQL
cat > /tmp/complete_setup.sql << 'EOF'
-- Connect to storygrow database
\c storygrow

-- Execute the schema
\i cloud_sql_schema.sql

-- Create application user for better security
CREATE USER storygrow_app WITH PASSWORD 'AppPassword123!';
GRANT CONNECT ON DATABASE storygrow TO storygrow_app;
GRANT USAGE ON SCHEMA public TO storygrow_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO storygrow_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO storygrow_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO storygrow_app;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO storygrow_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO storygrow_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT EXECUTE ON FUNCTIONS TO storygrow_app;

-- Show created tables
\echo ''
\echo 'Created tables:'
\dt
\echo ''
\echo 'Database setup complete!'
EOF

# Connect and execute
gcloud sql connect storygrow-database --user=postgres --database=storygrow < /tmp/complete_setup.sql

# Clean up
rm /tmp/complete_setup.sql

# Create a connection test script
cat > test_connection.sh << 'EOF'
#!/bin/bash
echo "Testing Cloud SQL connection..."
gcloud sql connect storygrow-database --user=postgres --database=storygrow --command="SELECT 'Connection successful!' as status, current_database() as database;"
EOF
chmod +x test_connection.sh

echo ""
echo "=========================================="
echo "✅ Database Creation Complete!"
echo "=========================================="
echo ""
echo "Instance Name: storygrow-database"
echo "Database Name: storygrow"
echo "Region: europe-west1"
echo "Connection Name: $CONNECTION_NAME"
echo "Public IP: $PUBLIC_IP"
echo ""
echo "⚠️  IMPORTANT SECURITY STEPS:"
echo "1. Change the root password:"
echo "   gcloud sql users set-password postgres --instance=storygrow-database --password=YOUR_NEW_SECURE_PASSWORD"
echo ""
echo "2. Change the app user password in the database:"
echo "   gcloud sql connect storygrow-database --user=postgres --database=storygrow"
echo "   Then run: ALTER USER storygrow_app WITH PASSWORD 'YOUR_NEW_APP_PASSWORD';"
echo ""
echo "3. Update the passwords in ../backend/.env.cloud_sql"
echo ""
echo "To connect to your database:"
echo "gcloud sql connect storygrow-database --user=postgres --database=storygrow"
echo ""
echo "To test the connection:"
echo "./test_connection.sh"