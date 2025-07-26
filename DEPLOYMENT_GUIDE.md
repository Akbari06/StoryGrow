# 🚀 StoryGrow Complete Deployment Guide

## Current Status
- ✅ **Backend**: Deployed and running at `https://storygrow-433353767151.europe-west1.run.app`
- ⏳ **Frontend**: Built but needs to be deployed to Firebase Hosting

## 🎯 What You Need to Do

### Step 1: Open Mac Terminal
1. Press `Cmd + Space` 
2. Type "Terminal"
3. Press Enter

### Step 2: Navigate to Project
```bash
cd /Users/tilmanresch/Documents/Projects/StoryGrow
```

### Step 3: Install Firebase CLI (if not installed)
```bash
# Try this first
npm install -g firebase-tools

# If that doesn't work, use this instead:
curl -sL https://firebase.tools | bash
```

### Step 4: Login to Firebase
```bash
firebase login
```
- This will open a browser window
- Login with your Google account that owns the storygrow-2 project

### Step 5: Deploy Frontend
```bash
firebase deploy --only hosting
```

### Step 6: Verify Deployment
Visit: https://storygrow-2.web.app

## 📁 Important Information

### Your Project Details
- **Project ID**: storygrow-2
- **Backend URL**: https://storygrow-433353767151.europe-west1.run.app
- **Frontend URL**: https://storygrow-2.web.app (after deployment)
- **Gemini API Key**: AIzaSyAo3cTkISmK9GqBxt7wFlJABfWWlw51O_A

### Already Completed
- ✅ Frontend is built (files are in `src/frontend/out/`)
- ✅ Firebase configuration files are created
- ✅ Backend is running with environment variables set

### File Locations
- Frontend code: `/src/frontend/`
- Built files: `/src/frontend/out/`
- Firebase config: `/firebase.json` and `/.firebaserc`

## 🆘 Troubleshooting

### If "firebase: command not found"
```bash
# Check if npm is working
npm --version

# If npm works, try installing with sudo
sudo npm install -g firebase-tools

# Or use Homebrew
brew install firebase-cli
```

### If deployment fails
1. Check you're in the right directory:
   ```bash
   pwd  # Should show: /Users/tilmanresch/Documents/Projects/StoryGrow
   ```

2. Check the out folder exists:
   ```bash
   ls -la src/frontend/out/
   ```

3. Check Firebase project:
   ```bash
   firebase use
   # Should show: storygrow-2
   ```

### If website shows 404 after deployment
The deployment might take 2-3 minutes to propagate. Try:
- Clear browser cache
- Try incognito/private window
- Wait a few minutes

## 🔍 How to Check Everything is Working

1. **Backend API**: 
   - Go to: https://storygrow-433353767151.europe-west1.run.app
   - You should see: `{"service":"StoryGrow API","version":"1.0.0",...}`

2. **Frontend**: 
   - Go to: https://storygrow-2.web.app
   - You should see the StoryGrow homepage with Kids/Parents options

3. **Full Test**:
   - Click "For Kids!"
   - Select a mood
   - Try to record or type a story

## 📝 Quick Commands Reference

```bash
# Check current directory
pwd

# Go to project
cd /Users/tilmanresch/Documents/Projects/StoryGrow

# Check Firebase CLI version
firebase --version

# Deploy only hosting
firebase deploy --only hosting

# See deployment history
firebase hosting:channel:list

# If you need to rebuild frontend
cd src/frontend
npm run build
cd ../..
firebase deploy --only hosting
```

## 🎉 Success Indicators
- Terminal shows: "Deploy complete!"
- Terminal shows hosting URLs
- https://storygrow-2.web.app loads without 404
- You can see the colorful Kids/Parents selection page

## 📞 Next Steps After Deployment
1. Test the Kids flow (mood → record → story)
2. Test the Parents flow (login → dashboard)
3. Check if API calls work (create a story)

## 🔐 Don't Forget
- Your backend is already configured with all environment variables
- The frontend is configured to use your Cloud Run backend
- Everything is set up - you just need to deploy!

Good luck! The deployment should only take about 5 minutes once Firebase CLI is installed.