# StoryGrow Testing Guide

## 🎯 Testing the Deployed Application

### Backend API Testing

Your backend is deployed at: `https://storygrow-433353767151.europe-west1.run.app`

#### 1. Test API Health
```bash
curl https://storygrow-433353767151.europe-west1.run.app/health
```
Expected: `{"status":"healthy"}`

#### 2. Test API Root
```bash
curl https://storygrow-433353767151.europe-west1.run.app/
```
Expected: Service information JSON

#### 3. Test API Documentation
Open in browser: `https://storygrow-433353767151.europe-west1.run.app/docs`

### Frontend Testing

Once deployed to Firebase Hosting: `https://storygrow-2.web.app`

#### Test Flow:
1. **Home Page**: Choose Kids or Parents portal
2. **Kids Flow**:
   - Select mood
   - Record or type story
   - View generated story
3. **Parents Flow**:
   - Login (demo mode)
   - View dashboard
   - Check emotional insights

## 🧪 API Endpoint Testing

### Create a Story (POST)
```bash
curl -X POST https://storygrow-433353767151.europe-west1.run.app/api/story/create \
  -H "Content-Type: application/json" \
  -d '{
    "child_id": "test_child_123",
    "text_input": "I saw a butterfly today",
    "session_mood": "happy",
    "educational_focus": ["nature", "curiosity"]
  }'
```

### Get Story (GET)
```bash
curl https://storygrow-433353767151.europe-west1.run.app/api/story/{story_id}
```

## 🔍 Troubleshooting

### Backend Issues

#### Check Logs
```bash
gcloud run logs read --service=storygrow --region=europe-west1 --limit=50
```

#### Common Issues:
1. **500 Error**: Check Gemini API key is set
2. **403 Error**: Run `./configure-cloud-run-permissions.sh`
3. **Firestore Error**: Verify database exists and permissions

### Frontend Issues

#### Build Errors
```bash
cd src/frontend
npm run build
```

#### Common Issues:
1. **API calls fail**: Check CORS and backend URL
2. **Page not found**: Verify Firebase hosting configuration
3. **Blank page**: Check browser console for errors

## 🏠 Local Testing

### Backend Local Test
```bash
cd src
python main.py --demo
```

### Frontend Local Test
```bash
cd src/frontend
npm run dev
```
Then open: http://localhost:3000

## ✅ Testing Checklist

- [ ] Backend health check returns 200
- [ ] API docs page loads
- [ ] Can create a story via API
- [ ] Frontend home page loads
- [ ] Kids mood selection works
- [ ] Story generation completes
- [ ] Parent dashboard displays
- [ ] No console errors in browser

## 📊 Performance Testing

### Backend Response Times
- Health check: < 200ms
- Story creation: < 5 seconds
- Story retrieval: < 500ms

### Frontend Load Times
- Initial page load: < 3 seconds
- Navigation: < 1 second
- API responses visible: < 5 seconds