# StoryGrow Project Configuration

## Important: Two Different Projects

### 1. Google Cloud Project
- **Project ID**: `storygrow-2`
- **Used for**:
  - Cloud Run backend API
  - Cloud SQL database (if using)
  - Cloud Storage
  - Other Google Cloud services
- **API Key**: aefb9e6eb6b37c4513fea431792c0e7cfdc03d60

### 2. Firebase Project
- **Project ID**: `storygrowth2`
- **Used for**:
  - Firebase Hosting (frontend deployment)
  - Firebase Authentication (if using)
  - Firestore (if using)
- **Hosting URL**: https://storygrowth2.web.app

## Configuration Usage

### Frontend (.env.local)
```env
# Google Cloud backend
NEXT_PUBLIC_API_URL=https://storygrow-433353767151.europe-west1.run.app
NEXT_PUBLIC_GCP_PROJECT_ID=storygrow-2

# Firebase hosting is configured separately in firebase.json
```

### Database
- **Cloud SQL Instance**: `database-storygrow` (in `storygrow-2` project)
- This is the ONLY database for the StoryGrow application

### Deployment Commands
```bash
# For Google Cloud backend
gcloud config set project storygrow-2

# For Firebase hosting
firebase use storygrowth2
firebase deploy --only hosting
```

## Common Confusion Points
1. **storygrow-2** ≠ **storygrowth2** - They are different projects!
2. Backend API runs in Google Cloud (`storygrow-2`)
3. Frontend is hosted on Firebase (`storygrowth2`)
4. Database location depends on your choice (Cloud SQL vs Supabase)