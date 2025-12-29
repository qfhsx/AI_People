#!/bin/bash

# Function to check and kill process on a port
check_and_kill_port() {
    local port=$1
    echo "🔍  Checking port $port..."
    
    # Find PID using lsof. -t gives terse output (only PID), -i selects internet files
    local pid=$(lsof -ti :$port)
    
    if [ -n "$pid" ]; then
        echo "⚠️  Port $port is occupied by PID $pid. Killing process..."
        kill -9 $pid
        sleep 1
        echo "✅  Process on port $port killed."
    else
        echo "✅  Port $port is free."
    fi
}

# Check Python
echo "🔍  Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "❌  Python 3 could not be found"
    exit 1
fi
echo "✅  Python 3 found."

# Check Node
echo "🔍  Checking Node.js environment..."
if ! command -v node &> /dev/null; then
    echo "❌  Node.js could not be found"
    exit 1
fi
echo "✅  Node.js found."

# Handle Backend Port (5000)
check_and_kill_port 5000

echo "🚀  Starting Backend..."
cd backend
echo "📦  Installing backend dependencies..."
pip3 install -r requirements.txt
echo "▶️   Running Flask server..."
python3 run.py &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
echo "⏳  Waiting for backend to initialize..."
sleep 5

# Handle Frontend Port (3000)
check_and_kill_port 3000

echo "🚀  Starting Frontend..."
cd frontend
echo "📦  Installing frontend dependencies..."
npm install
echo "▶️   Running Vite server..."
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉  All services started successfully!"
echo "👉  Backend running at: http://localhost:5000"
echo "👉  Frontend running at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Cleanup on exit
trap "echo '🛑  Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" EXIT INT TERM

wait
