#!/bin/bash
echo "Testing Cloud SQL connection..."
gcloud sql connect storygrow-database --user=postgres --database=storygrow --command="SELECT 'Connection successful!' as status, current_database() as database;"
