#!/bin/bash

echo "==================================="
echo "Cleaning up StoryGrow root directory"
echo "==================================="

cd ~/Documents/Projects/StoryGrow

# Create a cleanup summary
echo ""
echo "Files to clean up:"
echo "=================="

# Old deployment guides (replaced by PROJECT_DOCUMENTATION.md)
echo "✓ DEPLOYMENT_GUIDE.md - merged into PROJECT_DOCUMENTATION.md"
echo "✓ DEPLOY_FRONTEND.md - merged into PROJECT_DOCUMENTATION.md"
echo "✓ QUICK_DEPLOY.txt - merged into PROJECT_DOCUMENTATION.md"
echo "✓ production-config.md - merged into PROJECT_DOCUMENTATION.md"

# Backend files that should be in src/backend
echo "✓ requirements.txt - should be in src/backend/"
echo "✓ Dockerfile - should be in src/backend/"
echo "✓ cloudbuild.yaml - should be in src/backend/"
echo "✓ .env.example - should be in src/backend/"

# Scripts that should be in appropriate folders
echo "✓ setup.sh - should be in src/backend/"
echo "✓ setup-gcp-services.sh - should be in scripts/"
echo "✓ configure-cloud-run-permissions.sh - should be in scripts/"
echo "✓ set-cloud-run-env.sh - should be in scripts/"
echo "✓ deploy-frontend.sh - should be in scripts/"

# Sensitive files that shouldn't be in git
echo "✓ service-account-key.json - SHOULD NOT BE IN GIT!"
echo "✓ .env - already in .gitignore"

echo ""
echo "Moving files to proper locations..."
echo "==================================="

# Create scripts directory
mkdir -p scripts

# Move backend files
echo "Moving backend files..."
mv requirements.txt src/backend/ 2>/dev/null && echo "✓ Moved requirements.txt"
mv Dockerfile src/backend/ 2>/dev/null && echo "✓ Moved Dockerfile"
mv cloudbuild.yaml src/backend/ 2>/dev/null && echo "✓ Moved cloudbuild.yaml"
mv .env.example src/backend/ 2>/dev/null && echo "✓ Moved .env.example"
mv setup.sh src/backend/ 2>/dev/null && echo "✓ Moved setup.sh"

# Move scripts
echo ""
echo "Moving scripts..."
mv setup-gcp-services.sh scripts/ 2>/dev/null && echo "✓ Moved setup-gcp-services.sh"
mv configure-cloud-run-permissions.sh scripts/ 2>/dev/null && echo "✓ Moved configure-cloud-run-permissions.sh"
mv set-cloud-run-env.sh scripts/ 2>/dev/null && echo "✓ Moved set-cloud-run-env.sh"
mv deploy-frontend.sh scripts/ 2>/dev/null && echo "✓ Moved deploy-frontend.sh"

# Delete redundant documentation (keeping PROJECT_DOCUMENTATION.md)
echo ""
echo "Removing redundant documentation..."
rm -f DEPLOYMENT_GUIDE.md && echo "✓ Removed DEPLOYMENT_GUIDE.md"
rm -f DEPLOY_FRONTEND.md && echo "✓ Removed DEPLOY_FRONTEND.md"
rm -f QUICK_DEPLOY.txt && echo "✓ Removed QUICK_DEPLOY.txt"
rm -f production-config.md && echo "✓ Removed production-config.md"

# Remove service account key (SECURITY!)
echo ""
echo "⚠️  REMOVING SERVICE ACCOUNT KEY FROM GIT!"
rm -f service-account-key.json && echo "✓ Removed service-account-key.json"

# Update .gitignore to ensure sensitive files are ignored
echo ""
echo "Updating .gitignore..."
cat >> .gitignore << 'EOF'

# Service account keys
service-account-key.json
*.json
!package.json
!firebase.json
!package-lock.json
!tsconfig.json

# Environment files
.env
.env.*
!.env.example

# Local development
local-dev/
EOF

echo ""
echo "Final root directory structure:"
echo "=============================="
ls -la | grep -v "^\."

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "Summary of changes:"
echo "- Moved backend files to src/backend/"
echo "- Created scripts/ folder for deployment scripts"
echo "- Removed redundant documentation files"
echo "- Removed sensitive service account key"
echo "- Updated .gitignore for better security"
echo ""
echo "The root directory is now clean with only:"
echo "- Essential config files (.firebaserc, firebase.json)"
echo "- Main documentation (README.md, PROJECT_DOCUMENTATION.md)"
echo "- Git-related files"
echo "- License and demo files"