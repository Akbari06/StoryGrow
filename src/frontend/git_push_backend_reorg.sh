#!/bin/bash

# Script to commit and push backend reorganization

echo "Preparing to push backend reorganization to GitHub..."

# Navigate to project root
cd ~/Documents/Projects/StoryGrow

# Check status
echo "Current git status:"
git status

# Add all backend changes
echo ""
echo "Adding backend folder and changes..."
git add src/backend/
git add -u src/  # Track moved/deleted files

# Create commit
echo ""
echo "Creating commit..."
git commit -m "Reorganize project structure: separate backend and frontend

- Create dedicated backend/ folder for Python API and database
- Move all Python files to backend/ (api_server.py, main.py, etc.)
- Move database scripts to backend/
- Clean separation: src/backend/ (API) and src/frontend/ (React)
- Add database setup scripts and Cloud SQL schema

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Done! Backend reorganization pushed to GitHub."