# StoryGrow Production Configuration

## Google Cloud Project
- **Project ID**: storygrow-2
- **Region**: europe-west1

## Cloud Run
- **Service Name**: storygrow
- **URL**: https://storygrow-433353767151.europe-west1.run.app
- **Region**: europe-west1

## Firestore
- **Database ID**: database-storygrow
- **Location**: eur3 (europe-west3)
- **Mode**: Native

## Cloud Storage
- **Bucket Name**: bucketstorygrow
- **Location**: eu (multiple regions in European Union)

## APIs & Keys
- **Gemini API Key**: AIzaSyAo3cTkISmK9GqBxt7wFlJABfWWlw51O_A
- **Vertex AI API**: Enabled (using same API key)
- **Generative Language API**: Enabled through Vertex AI
- **Speech-to-Text API**: Enable in GCP Console (no API key needed)
- **Secret Manager**: Enabled (for secure API key storage)

## Service Account
- **Name**: storygrow-app
- **Email**: storygrow-app@storygrow-2.iam.gserviceaccount.com
- **Key File**: Already provided (service-account-key.json)