# Setup Automatic Firebase Deployment from GitHub

Follow these steps to enable automatic deployment when you push to GitHub:

## 1. Create Firebase Service Account

Run this command to create a service account key:

```bash
cd ~/Documents/Projects/StoryGrow/src/frontend
firebase init hosting:github
```

When prompted:
- Select "Yes" to set up workflow
- Enter: `brmnds/StoryGrow` (your GitHub repository)
- Select "Yes" to set up PR previews
- Enter `main` as the branch

This will automatically:
- Create the service account
- Add secrets to your GitHub repository
- Set up the workflow

## 2. Add Environment Secrets to GitHub

Go to your GitHub repository settings:
1. Navigate to: https://github.com/brmnds/StoryGrow/settings/secrets/actions
2. Add these secrets:
   - `NEXT_PUBLIC_API_URL`: `https://storygrow-433353767151.europe-west1.run.app`
   - `NEXT_PUBLIC_GCP_PROJECT_ID`: `storygrow-2`

## 3. Manual Alternative (if automatic setup fails)

### Create Service Account Manually:
```bash
# Create service account
gcloud iam service-accounts create github-actions-deploy \
  --display-name="GitHub Actions Deploy" \
  --project=storygrowth2

# Grant Firebase hosting admin role
gcloud projects add-iam-policy-binding storygrowth2 \
  --member="serviceAccount:github-actions-deploy@storygrowth2.iam.gserviceaccount.com" \
  --role="roles/firebasehosting.admin"

# Create and download key
gcloud iam service-accounts keys create firebase-service-account.json \
  --iam-account=github-actions-deploy@storygrowth2.iam.gserviceaccount.com \
  --project=storygrowth2

# Encode the key
base64 -i firebase-service-account.json
```

### Add to GitHub:
1. Copy the base64 encoded output
2. Go to: https://github.com/brmnds/StoryGrow/settings/secrets/actions
3. Create new secret named `FIREBASE_SERVICE_ACCOUNT`
4. Paste the base64 encoded content

## 4. Test the Setup

Make a small change to the frontend and push:
```bash
cd ~/Documents/Projects/StoryGrow/src/frontend
echo "<!-- Test deployment -->" >> app/page.tsx
git add .
git commit -m "Test automatic deployment"
git push origin main
```

Then check:
- GitHub Actions: https://github.com/brmnds/StoryGrow/actions
- Your live site: https://storygrowth2.web.app

## How It Works

Now, every time you:
1. Push changes to the `main` branch
2. That affect files in `src/frontend/**`
3. GitHub Actions will automatically:
   - Build your Next.js app
   - Deploy to Firebase Hosting
   - Update your live site

No more manual `firebase deploy` needed! 🎉