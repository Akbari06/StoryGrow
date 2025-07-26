#!/bin/bash

echo "🚀 Starting StoryGrow Local Development Environment"
echo "=================================================="

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to cleanup on exit
cleanup() {
    echo -e "\n${BLUE}Shutting down services...${NC}"
    # Kill all child processes
    pkill -P $$
    exit 0
}

# Set up trap for cleanup
trap cleanup INT TERM EXIT

# Copy local env file to backend
echo -e "${BLUE}Setting up environment...${NC}"
cp "$SCRIPT_DIR/.env.local" "$PROJECT_ROOT/src/.env"

# Start Backend
echo -e "\n${BLUE}Starting Backend API...${NC}"
cd "$PROJECT_ROOT/src"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo -e "${RED}Virtual environment not found!${NC}"
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r ../requirements.txt
fi

# Start backend in background
python main.py &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Start Frontend
echo -e "\n${BLUE}Starting Frontend...${NC}"
cd "$PROJECT_ROOT/src/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Update frontend to use local backend
echo "NEXT_PUBLIC_API_URL=http://localhost:8080" > .env.local

# Start frontend
npm run dev &
FRONTEND_PID=$!

# Display status
echo -e "\n${GREEN}✅ StoryGrow is running locally!${NC}"
echo "=================================="
echo -e "🔧 Backend API: ${GREEN}http://localhost:8080${NC}"
echo -e "📚 API Docs: ${GREEN}http://localhost:8080/docs${NC}"
echo -e "🎨 Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "\n${BLUE}Press Ctrl+C to stop all services${NC}"

# Wait for user to stop
while true; do
    sleep 1
done