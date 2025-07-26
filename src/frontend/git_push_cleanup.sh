#!/bin/bash

echo "Pushing cleanup changes to GitHub..."

cd ~/Documents/Projects/StoryGrow

# Add all changes (including deletions and moves)
git add -A

# Show what will be committed
echo "Changes to be committed:"
git status --short

# Commit
git commit -m "Clean up and reorganize project structure

- Move backend files (requirements.txt, Dockerfile, etc.) to src/backend/
- Create scripts/ folder for deployment scripts  
- Remove redundant documentation (consolidated into PROJECT_DOCUMENTATION.md)
- Remove service-account-key.json (security - should never be in git)
- Update .gitignore for better security
- Clean root directory to only essential files

Root now contains only:
- README.md and PROJECT_DOCUMENTATION.md
- Firebase configuration
- Git/GitHub files
- License

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push
git push origin main

echo "✅ Cleanup pushed to GitHub!"