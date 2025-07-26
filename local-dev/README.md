# Local Development Setup

This directory contains scripts and configuration for running StoryGrow locally.

## 🚀 Quick Start

```bash
# Run everything locally
./start-local.sh
```

This will:
1. Start the backend API on http://localhost:8080
2. Start the frontend on http://localhost:3000

## 📁 Files

- `start-local.sh` - Start both backend and frontend
- `start-backend.sh` - Start only the backend
- `start-frontend.sh` - Start only the frontend
- `.env.local` - Local environment variables

## 🔧 Prerequisites

### Backend
- Python 3.11+
- Virtual environment with dependencies

### Frontend  
- Node.js 18+
- npm or yarn

## 🌟 Local vs Production

| Component | Local URL | Production URL |
|-----------|-----------|----------------|
| Backend API | http://localhost:8080 | https://storygrow-433353767151.europe-west1.run.app |
| Frontend | http://localhost:3000 | https://storygrow-2.web.app |

## 💡 Tips

1. **Use local backend**: Update `src/frontend/.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8080
   ```

2. **Use production backend**: Update `src/frontend/.env.local`:
   ```
   NEXT_PUBLIC_API_URL=https://storygrow-433353767151.europe-west1.run.app
   ```

3. **Check logs**: Backend and frontend logs appear in the terminal