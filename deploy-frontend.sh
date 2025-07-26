#!/bin/bash

echo "🚀 Deploying StoryGrow Frontend to Firebase Hosting"
echo "================================================"

# Check if firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Please install it first:"
    echo "   npm install -g firebase-tools"
    echo "   or"
    echo "   curl -sL https://firebase.tools | bash"
    exit 1
fi

# Navigate to frontend directory
cd src/frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build the Next.js app
echo "🔨 Building Next.js app..."
npm run build

# The static files are now in 'out' directory due to output: 'export'
echo "✅ Build complete!"

# Go back to project root
cd ../..

# Deploy to Firebase
echo "🚀 Deploying to Firebase Hosting..."
firebase deploy --only hosting

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your app should be available at:"
echo "   https://storygrow-2.web.app"
echo "   https://storygrow-2.firebaseapp.com"
echo ""
echo "📝 Note: Make sure you're logged in to Firebase:"
echo "   firebase login"