#!/bin/bash

# Script to configure Cloud Run permissions for Firestore and other services

PROJECT_ID="storygrow-2"
SERVICE_NAME="storygrow"
REGION="europe-west1"

echo "🔐 Configuring Cloud Run Service Permissions"
echo "==========================================="
echo "Project: $PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Region: $REGION"
echo

# Get the Cloud Run service account
SERVICE_ACCOUNT=$(gcloud run services describe $SERVICE_NAME \
  --region=$REGION \
  --format="value(spec.template.spec.serviceAccountName)" 2>/dev/null)

if [ -z "$SERVICE_ACCOUNT" ]; then
  # Default Cloud Run service account
  SERVICE_ACCOUNT="433353767151-compute@developer.gserviceaccount.com"
  echo "Using default Cloud Run service account: $SERVICE_ACCOUNT"
else
  echo "Found service account: $SERVICE_ACCOUNT"
fi

echo
echo "🔧 Granting required permissions..."

# Grant Firestore permissions
echo "✓ Granting Firestore access..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/datastore.user" \
  --quiet

# Grant Cloud Storage permissions
echo "✓ Granting Cloud Storage access..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/storage.objectAdmin" \
  --quiet

# Grant Vertex AI permissions (for Gemini)
echo "✓ Granting Vertex AI access..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/aiplatform.user" \
  --quiet

# Grant Speech-to-Text permissions
echo "✓ Granting Speech-to-Text access..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/speech.client" \
  --quiet

echo
echo "✅ Permissions configured successfully!"
echo
echo "📝 Next steps:"
echo "1. Restart your Cloud Run service to apply changes:"
echo "   gcloud run services update $SERVICE_NAME --region=$REGION --no-traffic"
echo "   gcloud run services update $SERVICE_NAME --region=$REGION --traffic=100"
echo
echo "2. Check logs for any remaining permission issues:"
echo "   gcloud run logs read --service=$SERVICE_NAME --region=$REGION"