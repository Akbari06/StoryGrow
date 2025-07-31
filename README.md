# StoryGrow - AI-Powered Family Storytelling Platform (🥈 ODSC x Google Cloud Hackathon)

StoryGrow transforms children's daily experiences into personalized, illustrated stories using AI agents. Children (ages 3-8) share their day through voice or text, and our AI creates magical stories while monitoring emotional well-being for parents.

🌐 **Live Demo**: [https://storygrowth2.web.app](https://storygrowth2.web.app)  
📹 **Demo Video**: [Watch Demo](DEMO.md)  
🚀 **Backend API**: [https://storygrow-433353767151.europe-west1.run.app](https://storygrow-433353767151.europe-west1.run.app)

## ✨ Features

🎙️ **Voice & Text Input** - Children can speak or type their daily experiences  
🤖 **AI Story Generation** - Powered by Google Gemini API for personalized stories  
🎨 **Illustration Prompts** - AI-generated visual descriptions for each scene  
📊 **Emotional Monitoring** - Tracks child's emotional state and alerts parents  
👨‍👩‍👧 **Dual Interface** - Playful kids UI and insightful parent dashboard  
🧠 **Agent Memory** - Remembers preferences and creates consistent characters  

## 🏗️ Architecture

StoryGrow uses an **agentic AI architecture** with specialized agents:

- **Planner Agent** - Breaks down story creation into subtasks
- **Storyteller Agent** - Generates personalized stories using Gemini
- **Emotion Detector Agent** - Analyzes emotional content and flags concerns  
- **Illustrator Agent** - Creates image prompts for story scenes
- **Memory Agent** - Manages child preferences and story history
- **Executor Agent** - Orchestrates all agents and manages dependencies

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ 
- Node.js 18+ (for frontend)
- Google Cloud Account (for deployment)
- Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### 1. Clone Repository
```bash
git clone https://github.com/brmnds/StoryGrow.git
cd StoryGrow
```

### 2. Backend Setup
```bash
cd src/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Frontend Setup (Optional for backend-only)
```bash
cd src/frontend
npm install
```

### 4. Run Tests
```bash
# From project root
./TEST.sh
```

### 5. Run Application
```bash
# Demo mode (shows agent orchestration)
cd src/backend
python main.py --demo

# API Server mode
python main.py

# Frontend (in separate terminal)
cd src/frontend
npm run dev
```

## 📂 Project Structure

```
StoryGrow/
├── src/
│   ├── backend/
│   │   ├── main.py              # Entry point with demo/server modes
│   │   ├── config.py            # Configuration management
│   │   ├── planner.py           # Task planning agent
│   │   ├── executor.py          # Task execution orchestrator
│   │   ├── memory.py            # Persistent memory
│   │   ├── api_server.py        # FastAPI REST API
│   │   ├── agents/              # Specialized AI agents
│   │   │   ├── storyteller.py   # Story generation
│   │   │   ├── emotion_detector.py # Emotional analysis
│   │   │   └── illustrator.py   # Image prompts
│   │   ├── tools/               # Shared utilities
│   │   │   └── gemini_tools.py  # Gemini API client
│   │   └── requirements.txt     # Python dependencies
│   └── frontend/                # Next.js application
│       ├── app/                 # App router pages
│       ├── components/          # React components
│       └── package.json         # Node dependencies
├── .github/workflows/           # CI/CD pipelines
├── firebase.json               # Firebase hosting config
├── Dockerfile                  # Full-stack container
├── environment.yml             # Conda environment
├── TEST.sh                     # Smoke test script
├── ARCHITECTURE.md             # System design
├── EXPLANATION.md              # Technical details
├── DEMO.md                     # Demo video guide
└── README.md                   # This file
```

## 🎯 Core Workflow

1. **Child Input**: Child shares their day via speech or text
2. **Planning**: Planner creates subtasks for story generation
3. **Emotion Analysis**: Emotion detector analyzes sentiment and flags concerns
4. **Story Creation**: Storyteller generates personalized story using Gemini
5. **Illustration**: Illustrator creates image prompts for each scene
6. **Memory Storage**: Story and emotional data stored for future use
7. **Parent Insights**: Dashboard shows emotional trends and story engagement

## 🧪 Demo Mode

Experience the full agent orchestration:

```bash
cd src/backend
python main.py --demo
```

This demonstrates:
- ✅ Planning phase with task breakdown
- ✅ Agent execution with dependency management  
- ✅ Story generation using child's input
- ✅ Emotional analysis and parent alerts
- ✅ Memory usage and context management

Sample output:
```
🌟 StoryGrow Demo Mode - AI Family Storytelling Platform 🌟
📝 Child's Input: "Today I went to the park with mommy..."
🧠 Planning Phase: Created 4 tasks
⚡ Execution Phase: Running agents in parallel
📖 Generated Story: "The Magical Butterfly Adventure"
🎭 Emotion Analysis: happiness 0.85, excitement 0.72
✅ Demo completed successfully!
```

## 🔧 Configuration

Key environment variables in `.env`:

```bash
GEMINI_API_KEY=your_api_key_here       # Required for AI generation
GCP_PROJECT_ID=your_project_id         # Google Cloud project
API_HOST=0.0.0.0                       # API server host
API_PORT=8080                          # API server port
```

## 🚀 Deployment

### Option 1: Using Conda
```bash
conda env create -f environment.yml
conda activate storygrow
cd src/backend && python main.py
```

### Option 2: Using Docker
```bash
docker build -t storygrow .
docker run -p 80:80 -p 8080:8080 storygrow
```

### Option 3: Cloud Deployment

#### Backend (Google Cloud Run)
```bash
cd src/backend
gcloud run deploy storygrow --source . --region europe-west1
```

#### Frontend (Firebase Hosting)
```bash
cd src/frontend
npm run build
firebase deploy --only hosting
```

### CI/CD
Push to main branch triggers automatic deployment via GitHub Actions.

## 📊 API Endpoints

- `POST /api/story/create` - Create new story from child input
- `GET /api/story/{id}` - Retrieve specific story  
- `GET /api/child/{id}/dashboard` - Child dashboard data
- `GET /api/parent/insights/{id}` - Parent emotional insights
- `POST /api/voice/upload` - Upload voice recordings

## 🔒 Safety & Privacy

- All content filtered for age-appropriateness
- Emotional monitoring with parent alerts
- No external image generation (prompts only)
- Secure data storage with Firestore
- GDPR-compliant data handling

## 🏆 Hackathon Submission

- **Technical Excellence**: Robust FastAPI backend with comprehensive error handling
- **Solution Architecture**: Clear agent-based design with proper separation of concerns  
- **Gemini Integration**: Advanced prompt engineering for story generation and emotional analysis
- **Societal Impact**: Supports child development and family bonding through storytelling

## 📚 Documentation

- `ARCHITECTURE.md` - Detailed system architecture and agent design
- `EXPLANATION.md` - Planning process, tool usage, and limitations  
- `DEMO.md` - Video demonstration with timestamps

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `python src/test_setup.py`
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

---

**StoryGrow** - Where every day becomes a magical story! 🌟
