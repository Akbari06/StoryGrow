#!/bin/bash

# Script to reorganize backend structure
echo "Reorganizing project structure..."

cd ~/Documents/Projects/StoryGrow/src

# Create backend directory if it doesn't exist
echo "Creating backend directory..."
mkdir -p backend

# Move Python files to backend
echo "Moving Python files to backend..."
mv *.py backend/ 2>/dev/null
mv agents backend/ 2>/dev/null
mv tools backend/ 2>/dev/null
mv __pycache__ backend/ 2>/dev/null

# Move database files from frontend to backend
echo "Moving database files to backend..."
mv frontend/create_new_database.sh backend/ 2>/dev/null
mv frontend/cloud_sql_schema.sql backend/ 2>/dev/null
mv frontend/test_connection.sh backend/ 2>/dev/null
mv frontend/database_schema.sql backend/ 2>/dev/null
mv frontend/database_setup_instructions.md backend/ 2>/dev/null
mv frontend/setup_cloud_sql.sh backend/ 2>/dev/null
mv frontend/test_database_connection.sql backend/ 2>/dev/null
mv frontend/move_and_setup_database.sh backend/ 2>/dev/null

# List the new structure
echo ""
echo "New structure:"
echo "=============="
echo "src/"
echo "├── backend/"
ls -la backend/ | head -10
echo "└── frontend/"
ls -la frontend/ | grep -E "^d" | head -5

echo ""
echo "✅ Reorganization complete!"
echo ""
echo "To navigate to backend:"
echo "cd ~/Documents/Projects/StoryGrow/src/backend"