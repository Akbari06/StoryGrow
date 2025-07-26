# Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              StoryGrow Platform                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────┐                    ┌──────────────────────┐      │
│  │   User Interfaces   │                    │   External Services  │      │
│  ├─────────────────────┤                    ├──────────────────────┤      │
│  │ • Kids Interface    │                    │ • Google Gemini API  │      │
│  │ • Parents Dashboard │                    │ • Cloud SQL Database │      │
│  │ • Voice Recording   │                    │ • Cloud Storage      │      │
│  └──────────┬──────────┘                    └──────────┬───────────┘      │
│             │                                           │                   │
│             ▼                                           ▼                   │
│  ┌─────────────────────────────────────────────────────────────────┐      │
│  │                        API Gateway (FastAPI)                     │      │
│  │                     src/backend/api_server.py                    │      │
│  └─────────────────────────────────┬───────────────────────────────┘      │
│                                    │                                       │
│                                    ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐      │
│  │                    Agent Orchestration System                    │      │
│  ├─────────────────────────────────────────────────────────────────┤      │
│  │                                                                  │      │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │      │
│  │  │   Planner   │  │  Executor   │  │   Memory    │            │      │
│  │  │             │  │             │  │             │            │      │
│  │  │ Decomposes  │──▶│ Coordinates │──▶│  Stores    │            │      │
│  │  │   tasks     │  │   agents    │  │  context   │            │      │
│  │  └─────────────┘  └──────┬──────┘  └─────────────┘            │      │
│  │                           │                                     │      │
│  │                           ▼                                     │      │
│  │  ┌────────────────────────────────────────────────────┐        │      │
│  │  │              Specialized AI Agents                  │        │      │
│  │  ├────────────────────────────────────────────────────┤        │      │
│  │  │                                                    │        │      │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐│        │      │
│  │  │  │ Storyteller  │  │   Emotion    │  │Illustrator│        │      │
│  │  │  │    Agent     │  │   Detector   │  │   Agent   │        │      │
│  │  │  │              │  │              │  │           │        │      │
│  │  │  │ • Generate   │  │ • Analyze    │  │ • Create  │        │      │
│  │  │  │   stories    │  │   emotions   │  │   prompts │        │      │
│  │  │  │ • Age-aware  │  │ • Safety     │  │ • Scene   │        │      │
│  │  │  │   content    │  │   alerts     │  │   design  │        │      │
│  │  │  └──────────────┘  └──────────────┘  └──────────┘│        │      │
│  │  └────────────────────────────────────────────────────┘        │      │
│  └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Components

### 1. **User Interface**
   - **Kids Interface** (`src/frontend/app/kids/`): 
     - Colorful, intuitive design with large buttons
     - Voice recording capability
     - Story viewing with illustrations
   - **Parents Dashboard** (`src/frontend/app/parents/`):
     - Professional interface for monitoring
     - View child's stories and emotional analytics
     - Safety alerts and content filtering

### 2. **Agent Core**
   - **Planner** (`src/backend/planner.py`): 
     - Analyzes child input (text/voice)
     - Creates task dependency graph
     - Optimizes execution order
   
   - **Executor** (`src/backend/executor.py`): 
     - Manages agent lifecycle
     - Handles parallel/sequential execution
     - Aggregates results from all agents
   
   - **Memory** (`src/backend/memory.py`): 
     - PostgreSQL-backed persistent storage
     - Child context (age, preferences, history)
     - Session management and story archive

### 3. **Specialized Agents** (`src/backend/agents/`)
   - **Storyteller Agent**: 
     - Gemini Pro for story generation
     - Age-appropriate content filtering
     - Educational theme integration
   
   - **Emotion Detector Agent**: 
     - Sentiment analysis on child input
     - Parent alert generation for concerning content
     - Emotional pattern tracking
   
   - **Illustrator Agent**: 
     - Scene description generation
     - Image prompt creation for each story segment
     - Visual consistency maintenance

### 4. **Tools / APIs** (`src/backend/tools/`)
   - **Google Gemini API**: Primary LLM for content generation
   - **Cloud SQL**: PostgreSQL database for persistent storage
   - **Cloud Storage**: Audio recordings and generated images
   - **Voice-to-Text**: Converting audio input to text

### 5. **Observability**
   - **Structured Logging**: Each agent logs its decisions
   - **Execution Traces**: Full task graph execution history
   - **Error Handling**: Retry logic with exponential backoff
   - **Performance Metrics**: Response time tracking

## Data Flow

1. **Input Processing**
   ```
   Child Input (Text/Voice) → API Gateway → Planner
   ```

2. **Task Orchestration**
   ```
   Planner → Task Graph → Executor → Agent Pool
   ```

3. **Story Generation**
   ```
   Storyteller → Emotion Detector → Illustrator → Result Aggregation
   ```

4. **Output Delivery**
   ```
   Aggregated Results → API Response → Frontend Display
   ```

## Deployment Architecture

- **Frontend**: Firebase Hosting (static Next.js)
- **Backend**: Google Cloud Run (containerized Python)
- **Database**: Google Cloud SQL (PostgreSQL)
- **Storage**: Google Cloud Storage (media files)
- **CI/CD**: GitHub Actions for automated deployment