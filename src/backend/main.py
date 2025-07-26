"""
Entry point for StoryGrow - demonstrates agent orchestration
Can run in demo mode (for hackathon) or server mode (production)
"""
import argparse
import asyncio
import os
import subprocess
import sys
from datetime import datetime

from planner import Planner
from executor import Executor
from memory import Memory
from config import config

async def demo_mode():
    """
    Demo mode for hackathon video.
    Shows complete agent orchestration flow.
    """
    print("=" * 60)
    print("🌟 StoryGrow Demo Mode - AI Family Storytelling Platform 🌟")
    print("=" * 60)
    print()
    
    # Initialize core components
    print("Initializing AI agents...")
    planner = Planner()
    executor = Executor()
    memory = Memory()
    print("✓ Agents initialized")
    print()
    
    # Demo scenario
    demo_child_id = "demo_child_123"
    demo_input = {
        'text_input': "Today I went to the park with mommy and saw a big yellow butterfly! "
                     "It landed on a flower and I tried to catch it but it flew away. "
                     "Then we had ice cream and played on the swings!",
        'child_id': demo_child_id,
        'session_mood': 'happy',
        'educational_focus': ['nature', 'patience', 'friendship'],
        'include_elements': ['butterfly', 'park', 'ice cream', 'swings']
    }
    
    print("📝 Child's Input:")
    print(f"   \"{demo_input['text_input']}\"")
    print(f"   Mood: {demo_input['session_mood']} 😊")
    print(f"   Educational Focus: {', '.join(demo_input['educational_focus'])}")
    print()
    
    # Step 1: Planning
    print("🧠 Planning Phase:")
    print("   Breaking down into subtasks...")
    tasks = await planner.plan(demo_input)
    
    print(f"   Created {len(tasks)} tasks:")
    for task in tasks:
        deps = f" (depends on: {', '.join(task.depends_on)})" if task.depends_on else ""
        print(f"   • {task.agent}.{task.action}{deps}")
    print()
    
    # Step 2: Execution
    print("⚡ Execution Phase:")
    results = await executor.execute(tasks)
    
    # Step 3: Show results
    print()
    print("📖 Generated Story:")
    print("-" * 50)
    
    story = results.get('story', {})
    if story:
        print(f"Title: {story.get('title', 'Untitled')}")
        print()
        
        scenes = story.get('scenes', [])
        for scene in scenes:
            print(f"Scene {scene['sceneNumber']}:")
            print(f"  {scene['text']}")
            print(f"  [Image: {scene['imagePrompt'][:60]}...]")
            print()
    
    # Show emotion analysis
    print("-" * 50)
    emotions = results.get('emotions', {})
    if emotions:
        print("🎭 Emotion Analysis:")
        emotion_scores = emotions.get('emotions', {})
        for emotion, score in emotion_scores.items():
            bar = "█" * int(score * 10)
            print(f"   {emotion:10} {bar:<10} {score:.2f}")
        
        print(f"\n   Overall Sentiment: {emotions.get('overall_sentiment', 'unknown').upper()}")
            
        if emotions.get('alerts'):
            print("\n⚠️  Alerts for Parents:")
            for alert in emotions['alerts']:
                print(f"   - {alert['message']} (Severity: {alert['severity']})")
    
    # Show memory usage
    print("\n" + "-" * 50)
    print("🧠 Memory & Context:")
    context = await memory.get_child_context(demo_child_id)
    print(f"   Child Age: {context.get('age', 'Unknown')}")
    print(f"   Favorite Characters: {', '.join(context['preferences'].get('favoriteCharacters', []))}")
    print(f"   Favorite Themes: {', '.join(context['preferences'].get('favoriteThemes', []))}")
    
    print()
    print("✅ Demo completed successfully!")
    print("=" * 60)

def server_mode():
    """
    Production server mode - runs backend API server
    """
    print("🚀 Starting StoryGrow API Server")
    print("-" * 40)
    
    # Check if running in Cloud Run
    is_cloud_run = os.getenv('K_SERVICE') is not None
    
    processes = []
    
    try:
        # Check environment
        if not config.GEMINI_API_KEY:
            print("⚠️  Warning: GEMINI_API_KEY not set. Set it in .env file.")
            print("   Get your API key from: https://makersuite.google.com/app/apikey")
            print()
        
        # Start backend API server
        print("Starting API server...")
        
        if is_cloud_run:
            # In Cloud Run, run directly without subprocess
            import uvicorn
            print(f"✓ API server starting on http://{config.API_HOST}:{config.API_PORT}")
            uvicorn.run("api_server:app", 
                       host=config.API_HOST, 
                       port=config.API_PORT,
                       log_level="info",
                       reload=False)  # No reload in production
        else:
            # Local development - use subprocess
            api_process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "api_server:app", 
                 "--host", config.API_HOST, 
                 "--port", str(config.API_PORT),
                 "--reload"],
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            processes.append(api_process)
            print(f"✓ API server running at http://{config.API_HOST}:{config.API_PORT}")
            
            # Only try to start frontend in local development
            frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
            if os.path.exists(frontend_path) and os.path.exists(os.path.join(frontend_path, "package.json")):
                print("\nStarting frontend development server...")
                frontend_process = subprocess.Popen(
                    ["npm", "run", "dev"],
                    cwd=frontend_path,
                    shell=True if os.name == 'nt' else False
                )
                processes.append(frontend_process)
                print("✓ Frontend running at http://localhost:3000")
            else:
                print("\n📍 Note: Frontend should be deployed separately (e.g., Firebase Hosting, Vercel)")
                print("   For local development with frontend:")
                print("   cd src/frontend && npm run dev")
        
        if not is_cloud_run:
            print("\n✨ StoryGrow is running!")
            print("📱 Open http://localhost:3000 to use the app")
            print("📚 API docs available at http://localhost:8080/docs")
            print("Press Ctrl+C to stop all services")
            print("-" * 40)
            
            # Wait for keyboard interrupt
            try:
                while True:
                    # Check if processes are still running
                    for process in processes[:]:
                        if process.poll() is not None:
                            print(f"Process {process.pid} exited")
                            processes.remove(process)
                    
                    if not processes:
                        print("All processes exited")
                        break
                        
                    asyncio.get_event_loop().run_until_complete(asyncio.sleep(1))
            except KeyboardInterrupt:
                pass
            
    except KeyboardInterrupt:
        print("\n\nShutting down services...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
        print("Goodbye! 👋")

def test_mode():
    """Test mode to verify installation and configuration"""
    print("🧪 StoryGrow Test Mode")
    print("-" * 30)
    
    # Test configuration
    print("1. Testing configuration...")
    if config.GEMINI_API_KEY:
        print("   ✓ GEMINI_API_KEY is set")
    else:
        print("   ❌ GEMINI_API_KEY is not set")
        
    print(f"   ✓ Project ID: {config.GCP_PROJECT_ID}")
    print(f"   ✓ API Host: {config.API_HOST}:{config.API_PORT}")
    
    # Test imports
    print("\n2. Testing imports...")
    try:
        from tools.gemini_tools import GeminiClient
        print("   ✓ GeminiClient imported")
        
        from agents.storyteller import StorytellerAgent
        from agents.emotion_detector import EmotionDetectorAgent
        from agents.illustrator import IllustratorAgent
        print("   ✓ All agents imported")
        
        from memory import Memory
        print("   ✓ Memory imported")
        
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return
    
    # Test Gemini connection
    print("\n3. Testing Gemini connection...")
    if config.GEMINI_API_KEY:
        try:
            import asyncio
            async def test_gemini():
                client = GeminiClient()
                response = await client.generate("Say 'Hello from StoryGrow!'", max_tokens=50)
                return response
            
            response = asyncio.run(test_gemini())
            print(f"   ✓ Gemini response: {response[:50]}...")
        except Exception as e:
            print(f"   ❌ Gemini error: {e}")
    else:
        print("   ⚠️  Skipping Gemini test - API key not set")
    
    print("\n✅ Test completed!")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='StoryGrow - AI-Powered Family Storytelling Platform'
    )
    parser.add_argument(
        '--demo', 
        action='store_true',
        help='Run in demo mode to show agent orchestration'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run tests to verify installation'
    )
    
    args = parser.parse_args()
    
    if args.demo:
        # Run demo
        asyncio.run(demo_mode())
    elif args.test:
        # Run tests
        test_mode()
    else:
        # Run server
        server_mode()

if __name__ == "__main__":
    main()