"""
Test script to verify StoryGrow setup and demonstrate agent orchestration
"""
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from tools.gemini_tools import GeminiClient
from planner import Planner
from executor import Executor
from memory import Memory

async def test_gemini():
    """Test Gemini API connection"""
    print("Testing Gemini connection...")
    try:
        client = GeminiClient()
        response = await client.generate("Say hello from StoryGrow!", max_tokens=50)
        print(f"✓ Gemini response: {response}")
        return True
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return False

async def test_agents():
    """Test individual agents"""
    print("\nTesting individual agents...")
    
    try:
        from agents.storyteller import StorytellerAgent
        from agents.emotion_detector import EmotionDetectorAgent
        from agents.illustrator import IllustratorAgent
        
        storyteller = StorytellerAgent()
        emotion_detector = EmotionDetectorAgent()
        illustrator = IllustratorAgent()
        
        print("✓ All agents initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Agent initialization error: {e}")
        return False

async def test_orchestration():
    """Test complete orchestration"""
    print("\nTesting complete orchestration...")
    
    try:
        planner = Planner()
        executor = Executor()
        
        # Simple test input
        test_input = {
            'text_input': "I played with my toy dinosaur today!",
            'child_id': 'test_child',
            'session_mood': 'happy',
            'educational_focus': ['imagination'],
            'include_elements': ['dinosaur']
        }
        
        # Plan and execute
        tasks = await planner.plan(test_input)
        print(f"✓ Created {len(tasks)} tasks")
        
        results = await executor.execute(tasks)
        print("✓ Executed all tasks")
        
        # Check results
        if 'story' in results:
            story = results['story']
            print(f"✓ Generated story: '{story.get('title', 'Untitled')}'")
            print(f"  - {len(story.get('scenes', []))} scenes")
        
        if 'emotions' in results:
            emotions = results['emotions']
            print(f"✓ Emotion analysis completed")
            print(f"  - Overall sentiment: {emotions.get('overall_sentiment', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Orchestration error: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 StoryGrow Setup Test")
    print("=" * 40)
    
    # Check configuration
    print("Configuration:")
    print(f"  API Key set: {'Yes' if config.GEMINI_API_KEY else 'No'}")
    print(f"  Project ID: {config.GCP_PROJECT_ID}")
    print(f"  API Port: {config.API_PORT}")
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    if await test_gemini():
        tests_passed += 1
    
    if await test_agents():
        tests_passed += 1
        
    if await test_orchestration():
        tests_passed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! StoryGrow is ready to run.")
        print("\nNext steps:")
        print("  1. Run: python src/main.py --demo")
        print("  2. Or run: python src/main.py (for server mode)")
    else:
        print("❌ Some tests failed. Check the errors above.")
        print("\nCommon issues:")
        print("  - Missing GEMINI_API_KEY in .env file")
        print("  - Missing required Python packages")
        print("  - Network connectivity issues")

if __name__ == "__main__":
    asyncio.run(main())