# StoryGrow - Complete Project Documentation

## 🏗️ Project Overview

StoryGrow is an AI-powered family storytelling platform that transforms children's daily experiences into personalized, illustrated stories while providing parents with emotional insights and growth tracking.

### Key Components
- **Frontend**: Next.js 15 React application (TypeScript)
- **Backend**: Python FastAPI server with AI agents
- **Database**: PostgreSQL on Google Cloud SQL
- **AI**: Google Gemini Pro for story generation
- **Hosting**: Firebase (frontend) + Cloud Run (backend)

## 📁 Detailed Project Structure

```
StoryGrow/
├── src/
│   ├── backend/                    # Python Backend (API + AI Agents)
│   │   ├── api_server.py          # FastAPI server with endpoints
│   │   ├── main.py                # Main application entry point
│   │   ├── config.py              # Configuration management
│   │   ├── planner.py             # Task planning agent
│   │   ├── executor.py            # Task execution orchestrator
│   │   ├── memory.py              # Persistent memory management
│   │   ├── test_setup.py          # Setup verification script
│   │   │
│   │   ├── agents/                # AI Agents
│   │   │   ├── __init__.py
│   │   │   ├── storyteller.py     # Story generation using Gemini
│   │   │   ├── emotion_detector.py # Emotional analysis
│   │   │   └── illustrator.py     # Image prompt generation
│   │   │
│   │   ├── tools/                 # Utilities
│   │   │   ├── __init__.py
│   │   │   ├── gemini_tools.py    # Gemini API wrapper
│   │   │   └── secrets.py         # Secret management
│   │   │
│   │   ├── cloud_sql_schema.sql   # PostgreSQL database schema
│   │   ├── create_new_database.sh # Database creation script
│   │   ├── test_connection.sh     # Database connection test
│   │   └── .env.cloud_sql         # Database configuration (create this)
│   │
│   └── frontend/                  # Next.js Frontend
│       ├── app/                   # Next.js 15 app directory
│       │   ├── layout.tsx         # Root layout
│       │   ├── page.tsx           # Landing page
│       │   ├── globals.css        # Global styles
│       │   │
│       │   ├── (kids)/            # Kids section
│       │   │   ├── layout.tsx     # Kids layout with theme
│       │   │   └── kids/
│       │   │       ├── home/page.tsx    # Kids dashboard
│       │   │       ├── story/page.tsx   # Story viewer
│       │   │       └── record/page.tsx  # Voice recording
│       │   │
│       │   └── (parents)/         # Parents section
│       │       ├── layout.tsx     # Parents layout with sidebar
│       │       └── parents/
│       │           ├── dashboard/page.tsx # Parent dashboard
│       │           └── login/page.tsx     # Parent login
│       │
│       ├── components/            # React Components
│       │   ├── StoryViewer.tsx    # Story display component
│       │   ├── VoiceRecorder.tsx  # Voice recording interface
│       │   ├── MoodSelector.tsx   # Emotion selection UI
│       │   ├── EmotionChart.tsx   # Emotion tracking chart
│       │   └── AlertCard.tsx      # Parent alert component
│       │
│       ├── lib/                   # Utilities
│       │   └── config.ts          # Frontend configuration
│       │
│       ├── public/                # Static assets
│       ├── package.json           # Node dependencies
│       ├── next.config.ts         # Next.js configuration
│       ├── tailwind.config.js     # Tailwind CSS config
│       ├── postcss.config.mjs     # PostCSS configuration
│       └── .env.local             # Frontend environment vars
│
├── .github/
│   └── workflows/
│       └── deploy-frontend.yml    # GitHub Actions for auto-deploy
│
├── .firebaserc                    # Firebase project config
├── firebase.json                  # Firebase hosting config
└── README.md                      # Basic readme
```

## 🔧 Complete Environment Configuration

### Backend Environment Variables (`src/backend/.env`)
```env
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=storygrow-2
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Gemini API
GEMINI_API_KEY=aefb9e6eb6b37c4513fea431792c0e7cfdc03d60

# API Server
API_HOST=0.0.0.0
API_PORT=8080

# Environment
ENVIRONMENT=development  # or production
```

### Database Configuration (`src/backend/.env.cloud_sql`)
```env
# Cloud SQL Configuration
INSTANCE_CONNECTION_NAME=storygrow-2:europe-west1:storygrow-database
DB_USER=postgres
DB_PASSWORD=<CHANGE_THIS_PASSWORD>
DB_NAME=storygrow
DB_HOST=34.79.91.186  # Cloud SQL public IP
DB_PORT=5432

# Application Database User
DB_APP_USER=storygrow_app
DB_APP_PASSWORD=<CHANGE_THIS_PASSWORD>

# For Cloud Run deployment
INSTANCE_UNIX_SOCKET=/cloudsql/storygrow-2:europe-west1:storygrow-database
```

### Frontend Environment Variables (`src/frontend/.env.local`)
```env
# Backend API
NEXT_PUBLIC_API_URL=https://storygrow-433353767151.europe-west1.run.app

# Google Cloud Project
NEXT_PUBLIC_GCP_PROJECT_ID=storygrow-2

# Firebase (auto-configured by Firebase CLI)
# No manual configuration needed
```

## 🏢 Services and Infrastructure

### Google Cloud Platform (Project: `storygrow-2`)

#### 1. Cloud SQL (PostgreSQL)
- **Instance Name**: `storygrow-database`
- **Database Name**: `storygrow`
- **Region**: `europe-west1`
- **Version**: PostgreSQL 15
- **Tier**: `db-f1-micro` (development)
- **Connection Name**: `storygrow-2:europe-west1:storygrow-database`
- **Public IP**: `34.79.91.186`
- **Backup**: Daily at 03:00 UTC
- **Maintenance**: Sunday 04:00 UTC

#### 2. Cloud Run
- **Service Name**: `storygrow`
- **URL**: `https://storygrow-433353767151.europe-west1.run.app`
- **Region**: `europe-west1`
- **Container**: Auto-built from source
- **Memory**: 512Mi
- **CPU**: 1
- **Max Instances**: 100
- **Min Instances**: 0

#### 3. APIs Enabled
- Cloud SQL Admin API
- Cloud Run API
- Cloud Build API
- Vertex AI API (for Gemini)
- Secret Manager API

### Firebase (Project: `storygrowth2`)
**Note**: Different project than Google Cloud!

- **Hosting URL**: `https://storygrowth2.web.app`
- **Services**: Hosting only
- **Auto-deploy**: Via GitHub Actions

### External Services

#### GitHub
- **Repository**: `https://github.com/brmnds/StoryGrow`
- **Auto-deployment**: Pushes to `main` trigger Firebase deployment
- **Secrets Required**:
  - `FIREBASE_SERVICE_ACCOUNT`
  - `NEXT_PUBLIC_API_URL`
  - `NEXT_PUBLIC_GCP_PROJECT_ID`

## 📊 Database Schema Details

### User Management
```sql
-- User roles: 'parent', 'kid', 'admin'
auth_users          # Authentication (email, password)
users               # User profiles with roles
parents             # Parent-specific data
kids                # Child profiles (linked to parents)
sessions            # Active user sessions
```

### Content Storage
```sql
stories             # Story metadata (title, status, kid_id)
story_scenes        # Individual scenes (text, image_url, audio_url)
voice_recordings    # Audio files with transcripts
```

### Analytics & Safety
```sql
emotion_logs        # Emotion tracking (type, intensity, context)
alerts              # Parent notifications (severity levels)
ai_analysis         # AI insights (emotion, theme, concerns)
```

### Key Relationships
- One parent → Many kids
- One kid → Many stories
- One story → Many scenes
- One kid → Many emotion logs
- Alerts link parents and kids

## 🚀 Deployment Instructions

### Local Development Setup

#### 1. Backend Setup
```bash
cd src/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install fastapi uvicorn google-cloud-aiplatform google-cloud-sql-python psycopg2-binary

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run backend
python main.py
```

#### 2. Frontend Setup
```bash
cd src/frontend

# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Edit .env.local

# Run development server
npm run dev
```

### Production Deployment

#### 1. Deploy Backend to Cloud Run
```bash
cd src/backend

# Ensure you're authenticated
gcloud auth login
gcloud config set project storygrow-2

# Deploy (builds container automatically)
gcloud run deploy storygrow \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --add-cloudsql-instances storygrow-2:europe-west1:storygrow-database \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=storygrow-2"
```

#### 2. Deploy Frontend to Firebase
```bash
cd src/frontend

# Build production version
npm run build

# Deploy to Firebase
firebase deploy --only hosting

# Or let GitHub Actions handle it automatically
```

## 🔑 Critical Information

### Database Access
```bash
# Connect to production database
gcloud sql connect storygrow-database --user=postgres --database=storygrow

# Default passwords (MUST CHANGE!)
# Postgres: ChangeMeNow123!
# App user: AppPassword123!
```

### API Endpoints
- `POST /api/story/create` - Create story from child input
- `GET /api/story/{story_id}` - Get specific story
- `GET /api/child/{child_id}/stories` - List child's stories
- `GET /api/child/{child_id}/emotions` - Emotion history
- `GET /api/parent/{parent_id}/alerts` - Parent alerts
- `POST /api/voice/upload` - Upload voice recording

### Security Checklist
- [ ] Change all default passwords
- [ ] Set up Cloud SQL authorized networks
- [ ] Enable Cloud SQL SSL
- [ ] Configure CORS in FastAPI
- [ ] Set up API authentication
- [ ] Enable audit logging
- [ ] Configure backup retention
- [ ] Set up monitoring alerts

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check Cloud SQL instance is running
   - Verify IP is whitelisted
   - Check password is correct
   - Ensure `psql` is installed locally

2. **Frontend Can't Reach Backend**
   - Verify Cloud Run URL in `.env.local`
   - Check CORS settings in `api_server.py`
   - Ensure Cloud Run allows unauthenticated

3. **GitHub Actions Failing**
   - Check Firebase service account secret
   - Verify environment secrets are set
   - Check Node version matches

4. **Tailwind CSS Not Working**
   - Must use Tailwind v3, not v4
   - Check `postcss.config.mjs` configuration
   - Verify build process includes CSS

## 📈 Monitoring

### Google Cloud Console
- Cloud Run metrics: CPU, memory, requests
- Cloud SQL: Connections, storage, performance
- Error Reporting: Application errors
- Cloud Logging: Application logs

### Costs (Estimated Monthly)
- Cloud SQL (db-f1-micro): $10-15
- Cloud Run: $0-10 (pay per use)
- Firebase Hosting: Free
- Gemini API: Check quota limits

## 🔄 Maintenance Tasks

### Daily
- Monitor error logs
- Check database connections
- Review parent alerts

### Weekly
- Review emotion trends
- Check storage usage
- Update dependencies

### Monthly
- Analyze usage patterns
- Review and optimize costs
- Database maintenance
- Security audit

## 🚧 Future Enhancements

1. **Authentication**: Migrate to Firebase Auth
2. **Real-time**: Add WebSocket support
3. **Mobile Apps**: React Native versions
4. **Payments**: Stripe integration
5. **Analytics**: Google Analytics 4
6. **CDN**: CloudFlare for assets
7. **Search**: Elasticsearch for stories
8. **Export**: PDF story generation

## 📞 Support Information

- **GitHub Issues**: `https://github.com/brmnds/StoryGrow/issues`
- **Cloud Console**: `https://console.cloud.google.com/home/dashboard?project=storygrow-2`
- **Firebase Console**: `https://console.firebase.google.com/project/storygrowth2`

---

**Last Updated**: July 2024
**Maintained By**: StoryGrow Team