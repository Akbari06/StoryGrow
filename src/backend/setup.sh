#!/bin/bash

echo "🚀 Setting up StoryGrow..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install it first."
    echo "   Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No active gcloud project. Please run:"
    echo "   gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "Using project: $PROJECT_ID"

# Enable required APIs
echo "Enabling Google Cloud APIs..."
gcloud services enable \
    aiplatform.googleapis.com \
    generativelanguage.googleapis.com \
    firestore.googleapis.com \
    storage-component.googleapis.com \
    storage-api.googleapis.com \
    speech.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    secretmanager.googleapis.com

# Create Firestore database
echo "Setting up Firestore..."
gcloud firestore databases create \
    --location=us-central1 \
    --type=firestore-native 2>/dev/null || echo "Firestore database may already exist"

# Create Cloud Storage bucket
BUCKET_NAME="${PROJECT_ID}-storygrow-assets"
echo "Creating storage bucket: $BUCKET_NAME"
gsutil mb -p $PROJECT_ID -l us-central1 gs://$BUCKET_NAME/ 2>/dev/null || echo "Bucket may already exist"

# Create service account
echo "Creating service account..."
gcloud iam service-accounts create storygrow-app \
    --display-name="StoryGrow Application" 2>/dev/null || echo "Service account may already exist"

# Grant necessary permissions
echo "Granting permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:storygrow-app@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user" --quiet

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:storygrow-app@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/datastore.user" --quiet

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:storygrow-app@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin" --quiet

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:storygrow-app@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/speech.client" --quiet

# Create service account key
echo "Creating service account key..."
gcloud iam service-accounts keys create \
    ./service-account-key.json \
    --iam-account=storygrow-app@${PROJECT_ID}.iam.gserviceaccount.com 2>/dev/null || echo "Key may already exist"

# Update .env file
echo "Creating .env file..."
cat > .env << EOF
# Google Cloud
GEMINI_API_KEY=your_gemini_api_key_here
GCP_PROJECT_ID=$PROJECT_ID
GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json

# API Configuration
API_HOST=0.0.0.0
API_PORT=8080
FRONTEND_URL=http://localhost:3000

# Cloud Storage
GCS_BUCKET_NAME=$BUCKET_NAME
EOF

# Create frontend .env.local
mkdir -p src/frontend
cat > src/frontend/.env.local << EOF
# API endpoint
NEXT_PUBLIC_API_URL=http://localhost:8080

# Public config
NEXT_PUBLIC_GCP_PROJECT_ID=$PROJECT_ID
EOF

echo "✅ Setup complete!"
echo ""
echo "🔑 Next steps:"
echo "1. Get your Gemini API key:"
echo "   → Visit https://makersuite.google.com/app/apikey"
echo "   → Update GEMINI_API_KEY in .env file"
echo ""
echo "2. Install dependencies:"
echo "   → pip install -r requirements.txt"
echo ""
echo "3. Test the setup:"
echo "   → python src/test_setup.py"
echo ""
echo "4. Run the application:"
echo "   → python src/main.py --demo (for demo mode)"
echo "   → python src/main.py (for server mode)"
echo ""
echo "5. Create frontend (optional):"
echo "   → cd src && npx create-next-app@latest frontend --typescript --tailwind --app"
echo "   → cd frontend && npm install"