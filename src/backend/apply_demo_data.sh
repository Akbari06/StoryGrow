#!/bin/bash

echo "🔧 Applying demo data to PostgreSQL..."

# Check if Cloud SQL schema exists
if [ ! -f "cloud_sql_schema.sql" ]; then
    echo "❌ Error: cloud_sql_schema.sql not found"
    exit 1
fi

# Check if demo data exists
if [ ! -f "demo_data.sql" ]; then
    echo "❌ Error: demo_data.sql not found"
    exit 1
fi

# Apply to Cloud SQL
echo "📦 Applying demo data to Cloud SQL..."
gcloud sql connect storygrow-database --user=postgres --database=storygrow < demo_data.sql

echo "✅ Demo data applied successfully!"
echo ""
echo "Demo IDs configured:"
echo "  - Child ID: demo_child_123 → 44444444-4444-4444-4444-444444444444"
echo "  - Parent ID: demo_parent_456 → 33333333-3333-3333-3333-333333333333"
echo ""
echo "You can now create stories with these demo IDs!"