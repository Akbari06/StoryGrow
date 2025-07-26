#!/bin/bash

# Script to set all required environment variables in Cloud Run

SERVICE_NAME="storygrow"
REGION="europe-west1"

echo "Setting environment variables for Cloud Run service: $SERVICE_NAME"

# Update the service with all required environment variables
gcloud run services update $SERVICE_NAME \
  --region=$REGION \
  --update-env-vars="GEMINI_API_KEY=AIzaSyAo3cTkISmK9GqBxt7wFlJABfWWlw51O_A,GCP_PROJECT_ID=storygrow-796f0,GCS_BUCKET_NAME=bucketstorygrow,GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json" \
  --service-account="storygrow-app@storygrow-796f0.iam.gserviceaccount.com"

echo "✅ Environment variables updated!"
echo ""
echo "Note: Make sure the service account has these roles:"
echo "- Firestore User (roles/datastore.user)"
echo "- Storage Object Admin (roles/storage.objectAdmin)"
echo "- AI Platform User (roles/aiplatform.user)"