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

## Current Status (July 26, 2024) - IMPORTANT FOR NEXT CLAUDE

### What's Currently Broken:
1. **Story creation is hanging forever** - Stories aren't being saved to the database
2. **Type instead feature not working** - Same issue, hangs on story creation
3. **Database is empty** - No stories are being created despite demo data being inserted
4. **Many navigation links redirect to home page instead of proper pages**:
   - Kids area: "Type instead" link redirects to home
   - Parent dashboard: "Stories", "Insights", and "Settings" all redirect to home page
   - These pages likely don't exist or have routing issues
5. **Voice integration completely broken**:
   - Voice recordings are NOT being uploaded to Cloud Storage
   - Files are saved locally to container filesystem (lost on restart)
   - Need to implement Cloud Storage upload first
   - THEN need speech-to-text integration (Google Speech-to-Text API)
   - Should extract text content AND analyze tone/sentiment
   - Both the transcribed text AND emotional insights should be saved to database
   - Currently the voice upload endpoint returns local path which doesn't work on Cloud Run
   - Saving the Cloud Storage filepath/URL in database is fine once files are properly uploaded

### What We've Done Today:
1. **Switched from Firestore to PostgreSQL** - Created `memory_pg.py` to use Cloud SQL
2. **Fixed table name mismatches**:
   - Changed `emotion_sessions` → `emotion_logs` (actual table name)
   - Changed `parent_alerts` → `alerts`
   - Note: Both `sessions` (for auth) AND `emotion_logs` (for emotions) exist
3. **Added demo data mapping**:
   - `demo_child_123` → UUID `44444444-4444-4444-4444-444444444444`
   - Demo parent and users created with proper UUIDs
4. **Fixed database disconnect error** in `database.py`
5. **Updated emotion_logs insert** to match actual schema (emotion enum, intensity 1-5)

### What's Deployed:
- **Backend**: Revision `storygrow-00042-72q` with PostgreSQL support
- **Frontend**: Auto-deployed via GitHub Actions
- **Cloud SQL**: `storygrow-database` with schema created but voice_recordings table missing
- **API URL**: `https://storygrow-433353767151.europe-west1.run.app`

### Suspected Problems:
1. **Story creation endpoint might be failing** - Need to trace through the full flow
2. **Executor might not be initialized properly** - Check if it has access to MemoryPG
3. **GEMINI_API_KEY might not be working** - Although it's set in env vars
4. **Async execution might be failing** - The planner/executor flow might have issues

### Next Steps to Debug:
1. Check Cloud Run logs during story creation:
   ```bash
   gcloud run services logs read storygrow --region europe-west1 --limit 100
   ```
2. Test story creation endpoint directly:
   ```bash
   curl -X POST https://storygrow-433353767151.europe-west1.run.app/api/story/create \
     -H "Content-Type: application/json" \
     -d '{"text_input": "test story", "child_id": "demo_child_123"}'
   ```
3. Add logging to trace the flow in:
   - `api_server.py` - story creation endpoint
   - `executor.py` - execution flow
   - `memory_pg.py` - database operations
4. Check if Planner/Executor have access to the global `memory` instance

### Database Schema Notes:
- **emotion_logs**: Uses emotion_type enum (happy, sad, angry, etc.) NOT free text
- **sessions**: For auth sessions, NOT emotion data
- **stories**: Main story data
- **story_scenes**: Individual scenes for each story
- **alerts**: Parent notifications

### Files Changed Today:
- `/src/backend/memory_pg.py` - New PostgreSQL memory adapter
- `/src/backend/api_server.py` - Updated to use MemoryPG
- `/src/backend/database.py` - Fixed disconnect error
- `/src/backend/demo_data.sql` - Script to insert demo users
- `/src/backend/insert_demo_data.sql` - Direct SQL for demo data

### Demo Data SQL:
```sql
INSERT INTO kids (id, user_id, parent_id, name, age, avatar_emoji) VALUES
  ('44444444-4444-4444-4444-444444444444'::uuid, 
   '22222222-2222-2222-2222-222222222222'::uuid, 
   '33333333-3333-3333-3333-333333333333'::uuid, 
   'Demo Kid', 7, '🦄')
ON CONFLICT (id) DO NOTHING;
```

---
Last updated: July 26, 2024 (end of session)
This file helps maintain context across Claude Code sessions.