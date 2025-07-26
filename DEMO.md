# StoryGrow Demo Video

## Demo Video Link
🎥 **[Watch the StoryGrow Demo](https://youtu.be/cMIXp53Qfvs)**

*Note: Please update this link with your actual demo video URL*

## Video Timestamps

### Introduction (0:00 - 0:30)
- Project overview and motivation
- Problem statement: Helping children express themselves through AI

### System Architecture (0:30 - 1:30)
- High-level architecture walkthrough
- Multi-agent system explanation
- Technology stack overview

### Live Demo - Child Interface (1:30 - 3:30)
- **1:30** - Child login and interface tour
- **2:00** - Voice recording demonstration
- **2:30** - Text input example: "Today I saw a rainbow"
- **3:00** - Story generation in real-time
- **3:20** - Viewing generated story with illustrations

### Live Demo - Parent Dashboard (3:30 - 4:30)
- **3:30** - Parent login and dashboard overview
- **3:45** - Viewing child's stories
- **4:00** - Emotional analytics display
- **4:15** - Safety alerts demonstration

### Behind the Scenes (4:30 - 5:30)
- **4:30** - Agent orchestration visualization
- **4:45** - Planner breaking down tasks
- **5:00** - Parallel agent execution
- **5:15** - Database and memory operations

### Technical Deep Dive (5:30 - 6:30)
- **5:30** - Code walkthrough of agent system
- **5:45** - Gemini API integration
- **6:00** - Safety filtering demonstration
- **6:15** - Performance optimizations

### Deployment Demo (6:30 - 7:00)
- **6:30** - GitHub Actions CI/CD pipeline
- **6:45** - Cloud Run deployment
- **7:00** - Firebase hosting for frontend

### Conclusion (7:00 - 7:30)
- Summary of key features
- Future enhancements
- Call to action

## Key Features Demonstrated

1. **Multi-Agent Orchestration**
   - Planner, Executor, and specialized agents working together
   - Task dependency resolution
   - Parallel execution for performance

2. **Child Safety**
   - Content filtering
   - Emotional analysis
   - Parent notifications

3. **User Experience**
   - Intuitive kid-friendly interface
   - Professional parent dashboard
   - Real-time story generation

4. **Technical Excellence**
   - Cloud-native architecture
   - Automated testing and deployment
   - Comprehensive observability

## Running the Demo Locally

To run the demo yourself:

```bash
# Clone the repository
git clone https://github.com/brmnds/StoryGrow.git
cd StoryGrow

# Run the smoke tests
./TEST.sh

# Start the demo
python src/backend/main.py --demo
```

## Additional Resources

- [Architecture Diagram](ARCHITECTURE.md)
- [Technical Explanation](EXPLANATION.md)
- [Setup Instructions](README.md)
- [Live Application](https://storygrowth2.web.app)