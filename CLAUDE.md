# Claude Code Context

This file contains important context and learnings for anyone using Claude Code to work on this project.

## Project Overview
StoryGrow is an AI-powered storytelling platform for children with parent monitoring capabilities. It uses:
- Frontend: Next.js 15 with TypeScript in `src/frontend/`
- Backend: Python FastAPI with AI agents in `src/backend/`
- Database: PostgreSQL on Google Cloud SQL (`storygrow-database`)
- AI: Google Gemini Pro for story generation

## Important Project Names
- **Google Cloud Project**: `storygrow-2` (NOT storygrow)
- **Firebase Project**: `storygrowth2` (NOT storygrow2)
- **Cloud SQL Instance**: `storygrow-database`
- **Database Name**: `storygrow`
- **Cloud Run Service**: `storygrow`

## Key Learnings & Gotchas

### 1. Tailwind CSS Version
- Must use Tailwind CSS v3, NOT v4
- v4 has incompatible PostCSS configuration
- If CSS isn't rendering, check the Tailwind version

### 2. Directory Structure
- Backend files go in `src/backend/`
- Frontend files go in `src/frontend/`
- Don't mix Python files in the root or src directory

### 3. Database Setup
- The SQL schema is PostgreSQL-specific
- Use `cloud_sql_schema.sql` for Google Cloud SQL
- Don't use `database_schema.sql` (that's for Supabase)

### 4. Authentication
- Currently using `storygrow3000@gmail.com` for Google Cloud
- Make sure you're using the right Google account for deployments

### 5. Environment Variables
- Backend: Copy `.env.example` to `.env`
- Frontend: Copy `.env.example` to `.env.local`
- Never commit actual .env files

### 6. Common Commands
```bash
# Backend
cd ~/Documents/Projects/StoryGrow/src/backend
python main.py

# Frontend
cd ~/Documents/Projects/StoryGrow/src/frontend
npm run dev

# Database connection
gcloud sql connect storygrow-database --user=postgres --database=storygrow

# Deploy frontend
firebase deploy --only hosting

# Deploy backend
gcloud run deploy storygrow --source . --region europe-west1
```

## AI Agent Architecture
The backend uses specialized agents:
- **Planner**: Breaks down tasks
- **Storyteller**: Generates stories using Gemini
- **Emotion Detector**: Analyzes emotional content
- **Illustrator**: Creates image prompts
- **Executor**: Orchestrates all agents

## Testing Approach
- Frontend: Check if gradients and styles render
- Backend: Run `python test_setup.py`
- Database: Use `./test_connection.sh`

## Security Notes
- Change all default passwords immediately
- Never commit service-account-key.json
- Use Secret Manager for production API keys

## Future Work Ideas
- Implement proper authentication (Firebase Auth)
- Add real-time updates with WebSockets
- Create mobile apps
- Add payment processing
- Implement voice recording upload

## Useful Context for Claude
When working on this project, Claude should know:
- The project aims to help children express themselves through stories
- Parent safety and monitoring is a key feature
- The AI should generate age-appropriate content only
- The dual interface (kids/parents) has different design languages
- Performance and security are priorities

## Common Issues & Solutions
1. **"Module not found" errors**: Check if you're in the right directory
2. **Database connection fails**: Verify you're using the right project and credentials
3. **Frontend styles not working**: Check Tailwind version and PostCSS config
4. **API calls failing**: Verify Cloud Run URL in frontend .env.local

---
Last updated: July 2024
This file helps maintain context across Claude Code sessions.