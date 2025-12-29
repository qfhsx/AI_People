@echo off
echo Checking requirements...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found!
    pause
    exit /b
)
echo ✅  Python found.

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js not found!
    pause
    exit /b
)
echo ✅  Node.js found.

REM Function to check and kill process on a port
:check_and_kill_port
    setlocal
    set "port=%~1"
    echo 🔍  Checking port %port%...
    
    REM Find PID using netstat
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%port%') do (
        set "pid=%%a"
        goto :kill_process
    )
    
    echo ✅  Port %port% is free.
    goto :end
    
    :kill_process
    echo ⚠️  Port %port% is occupied by PID %pid%. Killing process...
    taskkill /PID %pid% /F >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅  Process on port %port% killed.
    ) else (
        echo ❌  Failed to kill process on port %port%.
    )
    
    :end
    endlocal
    exit /b

REM Check Backend Port (5000)
call :check_and_kill_port 5000

echo 🚀  Starting Backend...
start "Backend Server" /k "cd backend && pip install -r requirements.txt && python run.py"

REM Wait a bit for backend to initialize
echo ⏳  Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Check Frontend Port (3000)
call :check_and_kill_port 3000

echo 🚀  Starting Frontend...
start "Frontend Server" /k "cd frontend && npm install && npm run dev"

echo.
echo 🎉  All services started successfully!
echo 👉  Backend running at: http://localhost:5000
echo 👉  Frontend running at: http://localhost:3000
echo.
echo Press any key to stop all services...
pause >nul

echo 🛑  Stopping services...
REM Try to find and kill the backend and frontend processes
taskkill /FI "WINDOWTITLE eq Backend Server" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend Server" /F >nul 2>&1

echo ✅  All services stopped.
