# StoryGrow - AI-Powered Family Storytelling Platform

StoryGrow transforms children's daily experiences into personalized, illustrated stories using AI agents. Children (ages 3-8) share their day through voice or text, and our AI creates magical stories while monitoring emotional well-being for parents.

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

### 1. Clone Repository
```bash
git clone <repository-url>
cd StoryGrow
```

### 2. Set Up Environment
```bash
# Run the setup script
./setup.sh

# Get your Gemini API key from https://makersuite.google.com/app/apikey
# Update .env file with your API key
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Test Installation
```bash
python src/test_setup.py
```

### 5. Run Application
```bash
# Demo mode (for hackathon presentation)
python src/main.py --demo

# Server mode (full application)
python src/main.py
```

## 📂 Project Structure

```
StoryGrow/
├── src/
│   ├── main.py              # Entry point with demo and server modes
│   ├── config.py            # Configuration management
│   ├── planner.py           # Task planning agent
│   ├── executor.py          # Task execution orchestrator
│   ├── memory.py            # Persistent memory with Firestore
│   ├── api_server.py        # FastAPI REST API
│   ├── agents/              # Specialized AI agents
│   │   ├── storyteller.py   # Story generation with Gemini
│   │   ├── emotion_detector.py # Emotional analysis
│   │   └── illustrator.py   # Image prompt generation
│   ├── tools/               # Shared tools and utilities
│   │   └── gemini_tools.py  # Gemini API client
│   └── frontend/            # Next.js frontend (optional)
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── cloudbuild.yaml         # Google Cloud Build config
├── setup.sh                # Automated setup script
└── README.md               # This file
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
python src/main.py --demo
```

This demonstrates:
- ✅ Planning phase with task breakdown
- ✅ Agent execution with dependency management  
- ✅ Story generation using child's input
- ✅ Emotional analysis and parent alerts
- ✅ Memory usage and context management

## 🔧 Configuration

Key environment variables in `.env`:

```bash
GEMINI_API_KEY=your_api_key_here       # Required for AI generation
GCP_PROJECT_ID=your_project_id         # Google Cloud project
API_HOST=0.0.0.0                       # API server host
API_PORT=8080                          # API server port
```

## 🚀 Deployment

### Local Development
```bash
python src/main.py  # Starts both API and frontend
```

### Google Cloud Run
```bash
gcloud builds submit --config cloudbuild.yaml
```

### Docker
```bash
docker build -t storygrow .
docker run -p 8080:8080 storygrow
```

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