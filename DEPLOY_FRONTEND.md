# Frontend Deployment Guide - Firebase Hosting

## Prerequisites

### 1. Install Firebase CLI
Choose one of these methods:

```bash
# Option 1: Using npm
npm install -g firebase-tools

# Option 2: Using standalone binary
curl -sL https://firebase.tools | bash

# Option 3: On macOS with Homebrew
brew install firebase-cli
```

### 2. Login to Firebase
```bash
firebase login
```

## Quick Deploy

Just run:
```bash
./deploy-frontend.sh
```

## Manual Steps (if needed)

### 1. Build the Frontend
```bash
cd src/frontend
npm install
npm run build
```

### 2. Deploy to Firebase
```bash
# From project root
firebase deploy --only hosting
```

## Your Frontend URLs

Once deployed, your app will be available at:
- https://storygrow-2.web.app
- https://storygrow-2.firebaseapp.com

## Configuration

The frontend is already configured to use your backend:
- Backend API: https://storygrow-433353767151.europe-west1.run.app
- This is set in `src/frontend/.env.local`

## Troubleshooting

### If deployment fails:
1. Make sure you're logged in: `firebase login`
2. Check that the project is set: `firebase use storygrow-2`
3. Ensure Firebase Hosting is enabled in your Firebase Console

### If the app doesn't load:
1. Check browser console for errors
2. Verify the backend is running at the Cloud Run URL
3. Check CORS settings if API calls fail