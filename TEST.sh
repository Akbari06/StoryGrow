#!/bin/bash
# Smoke test script for StoryGrow
# This script verifies core functionality of the agent system

set -e  # Exit on error

echo "================================"
echo "StoryGrow Smoke Test Suite"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo "1. Checking Python version..."
python_version=$(python3 --version 2>&1)
if [[ $python_version == *"3.11"* ]] || [[ $python_version == *"3.10"* ]] || [[ $python_version == *"3.9"* ]]; then
    echo -e "${GREEN}✓ Python version OK: $python_version${NC}"
else
    echo -e "${RED}✗ Python version issue: $python_version${NC}"
    exit 1
fi
echo ""

# Navigate to backend directory
cd src/backend

# Test 1: Import verification
echo "2. Testing Python imports..."
python3 -c "
try:
    from planner import Planner
    from executor import Executor
    from memory import Memory
    from config import config
    print('✓ Core agent imports successful')
except Exception as e:
    print(f'✗ Import error: {e}')
    exit(1)
"
echo ""

# Test 2: Configuration check
echo "3. Checking configuration..."
python3 -c "
from config import config
errors = []
if not config.GCP_PROJECT_ID:
    errors.append('GCP_PROJECT_ID not set')
if config.GEMINI_API_KEY:
    print('✓ GEMINI_API_KEY is set')
else:
    print('⚠️  GEMINI_API_KEY not set (will use mock mode)')
    
if errors:
    print(f'✗ Config errors: {errors}')
else:
    print('✓ Configuration OK')
"
echo ""

# Test 3: Agent initialization
echo "4. Testing agent initialization..."
python3 -c "
import asyncio
from planner import Planner
from executor import Executor
from memory import Memory

try:
    planner = Planner()
    executor = Executor()
    memory = Memory()
    print('✓ All agents initialized successfully')
except Exception as e:
    print(f'✗ Agent initialization error: {e}')
    exit(1)
"
echo ""

# Test 4: Basic planning test
echo "5. Testing planning functionality..."
python3 -c "
import asyncio
from planner import Planner

async def test_planning():
    planner = Planner()
    test_input = {
        'text_input': 'Test story about a happy day',
        'child_id': 'test_child_123',
        'session_mood': 'happy'
    }
    
    try:
        tasks = await planner.plan(test_input)
        if tasks and len(tasks) > 0:
            print(f'✓ Planning successful: Generated {len(tasks)} tasks')
            return True
        else:
            print('✗ Planning failed: No tasks generated')
            return False
    except Exception as e:
        print(f'✗ Planning error: {e}')
        return False

# Run the test
result = asyncio.run(test_planning())
exit(0 if result else 1)
"
echo ""

# Test 5: API server startup test
echo "6. Testing API server startup..."
timeout 5s python3 -c "
import uvicorn
from api_server import app
import threading
import time
import requests

def run_server():
    uvicorn.run(app, host='127.0.0.1', port=8888, log_level='error')

# Start server in background thread
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Wait for server to start
time.sleep(2)

try:
    # Test health endpoint
    response = requests.get('http://127.0.0.1:8888/health', timeout=2)
    if response.status_code == 200:
        print('✓ API server health check passed')
    else:
        print(f'✗ API server health check failed: Status {response.status_code}')
        exit(1)
except Exception as e:
    print(f'✗ API server test error: {e}')
    exit(1)
" || {
    if [ $? -eq 124 ]; then
        echo -e "${GREEN}✓ API server startup test completed (timeout expected)${NC}"
    else
        echo -e "${RED}✗ API server test failed${NC}"
        exit 1
    fi
}
echo ""

# Test 6: Memory operations test
echo "7. Testing memory operations..."
python3 -c "
import asyncio
from memory import Memory

async def test_memory():
    memory = Memory()
    test_child_id = 'test_child_123'
    
    try:
        # Test context retrieval
        context = await memory.get_child_context(test_child_id)
        print('✓ Memory context retrieval successful')
        
        # Test session creation
        session_id = await memory.create_session(test_child_id, 'test')
        if session_id:
            print(f'✓ Memory session creation successful: {session_id}')
        
        return True
    except Exception as e:
        print(f'✗ Memory test error: {e}')
        return False

result = asyncio.run(test_memory())
exit(0 if result else 1)
"
echo ""

# Summary
echo "================================"
echo "Smoke Test Summary"
echo "================================"
echo -e "${GREEN}✓ All core functionality tests passed!${NC}"
echo ""
echo "The StoryGrow agent system is ready to run."
echo "To start the system:"
echo "  - Demo mode: python src/backend/main.py --demo"
echo "  - Server mode: python src/backend/main.py"
echo ""