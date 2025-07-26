#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up Google Cloud services for StoryGrow...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI not found. Please install it first.${NC}"
    echo "   Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ No active gcloud project. Please run:${NC}"
    echo "   gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo -e "${GREEN}Using project: $PROJECT_ID${NC}"

# Enable required APIs
echo -e "${BLUE}Enabling Google Cloud APIs...${NC}"
apis=(
    "aiplatform.googleapis.com"
    "generativelanguage.googleapis.com"
    "firestore.googleapis.com"
    "storage-component.googleapis.com"
    "storage-api.googleapis.com"
    "speech.googleapis.com"
    "run.googleapis.com"
    "cloudbuild.googleapis.com"
    "secretmanager.googleapis.com"
    "cloudresourcemanager.googleapis.com"
)

for api in "${apis[@]}"; do
    echo -n "Enabling $api... "
    if gcloud services enable $api --quiet 2>/dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}Already enabled or error${NC}"
    fi
done

# Create Firestore database
echo -e "${BLUE}Setting up Firestore...${NC}"
echo "Checking if Firestore database exists..."
if ! gcloud firestore databases describe --database="(default)" 2>/dev/null; then
    echo "Creating Firestore database..."
    gcloud firestore databases create \
        --location=europe-west1 \
        --type=firestore-native \
        --database="(default)"
else
    echo -e "${GREEN}Firestore database already exists${NC}"
fi

# Create Cloud Storage bucket
BUCKET_NAME="${PROJECT_ID}-storygrow-assets"
echo -e "${BLUE}Creating storage bucket: $BUCKET_NAME${NC}"
if ! gsutil ls -b gs://$BUCKET_NAME 2>/dev/null; then
    gsutil mb -p $PROJECT_ID -l europe-west1 gs://$BUCKET_NAME/
    # Set CORS for frontend access
    echo '[{"origin": ["*"],"method": ["GET", "POST", "PUT", "DELETE"],"responseHeader": ["*"],"maxAgeSeconds": 3600}]' > /tmp/cors.json
    gsutil cors set /tmp/cors.json gs://$BUCKET_NAME
    rm /tmp/cors.json
    echo -e "${GREEN}Bucket created with CORS enabled${NC}"
else
    echo -e "${GREEN}Bucket already exists${NC}"
fi

# Create service account
SERVICE_ACCOUNT_NAME="storygrow-app"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
echo -e "${BLUE}Creating service account...${NC}"
if ! gcloud iam service-accounts describe $SERVICE_ACCOUNT_EMAIL 2>/dev/null; then
    gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
        --display-name="StoryGrow Application"
else
    echo -e "${GREEN}Service account already exists${NC}"
fi

# Grant necessary permissions
echo -e "${BLUE}Granting permissions...${NC}"
roles=(
    "roles/aiplatform.user"
    "roles/datastore.user"
    "roles/storage.objectAdmin"
    "roles/speech.client"
    "roles/secretmanager.secretAccessor"
    "roles/firestore.serviceAgent"
)

for role in "${roles[@]}"; do
    echo -n "Granting $role... "
    gcloud projects add-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
        --role="$role" --quiet 2>/dev/null
    echo -e "${GREEN}✓${NC}"
done

# Grant Cloud Run service account permissions
echo -e "${BLUE}Granting Cloud Run permissions...${NC}"
CLOUD_RUN_SA="${PROJECT_ID}-compute@developer.gserviceaccount.com"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$CLOUD_RUN_SA" \
    --role="roles/datastore.user" --quiet

# Create service account key
echo -e "${BLUE}Creating service account key...${NC}"
KEY_FILE="./service-account-key.json"
if [ ! -f "$KEY_FILE" ]; then
    gcloud iam service-accounts keys create $KEY_FILE \
        --iam-account=$SERVICE_ACCOUNT_EMAIL
    echo -e "${GREEN}Service account key created${NC}"
else
    echo -e "${GREEN}Service account key already exists${NC}"
fi

# Update Cloud Run service with environment variables
echo -e "${BLUE}Updating Cloud Run service configuration...${NC}"
CLOUD_RUN_SERVICE="storygrow"
REGION="europe-west1"

# Check if service exists
if gcloud run services describe $CLOUD_RUN_SERVICE --region=$REGION 2>/dev/null; then
    echo "Updating environment variables for Cloud Run..."
    gcloud run services update $CLOUD_RUN_SERVICE \
        --region=$REGION \
        --update-env-vars="GCP_PROJECT_ID=$PROJECT_ID,GCS_BUCKET_NAME=$BUCKET_NAME" \
        --quiet
    echo -e "${GREEN}Cloud Run service updated${NC}"
else
    echo -e "${RED}Cloud Run service not found. Deploy the backend first.${NC}"
fi

# Create .env.production file for local reference
echo -e "${BLUE}Creating .env.production file...${NC}"
cat > .env.production << EOF
# Google Cloud Production Settings
GEMINI_API_KEY=your_gemini_api_key_here
GCP_PROJECT_ID=$PROJECT_ID
GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json

# API Configuration
API_HOST=0.0.0.0
API_PORT=8080
FRONTEND_URL=https://your-frontend-url.com

# Cloud Storage
GCS_BUCKET_NAME=$BUCKET_NAME

# Cloud Run Backend URL
BACKEND_URL=https://storygrow-433353767151.europe-west1.run.app
EOF

echo -e "${GREEN}✅ Google Cloud services setup complete!${NC}"
echo
echo -e "${BLUE}Summary:${NC}"
echo "- Project ID: $PROJECT_ID"
echo "- Firestore: Enabled (europe-west1)"
echo "- Storage Bucket: gs://$BUCKET_NAME"
echo "- Service Account: $SERVICE_ACCOUNT_EMAIL"
echo "- Backend URL: https://storygrow-433353767151.europe-west1.run.app"
echo
echo -e "${BLUE}Next steps:${NC}"
echo "1. Add your Gemini API key to Cloud Run:"
echo "   gcloud run services update storygrow --region=europe-west1 --update-env-vars=\"GEMINI_API_KEY=your_key_here\""
echo
echo "2. Build and deploy the frontend"
echo
echo "3. Test the full application"