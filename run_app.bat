@echo off
echo Starting Market Analysis App...

:: Set current directory to the script's directory
cd /d "%~dp0"

:: Check if virtual environment exists
if not exist venv\Scripts\python.exe (
    echo Error: Virtual environment not found in .\venv
    pause
    exit /b
)

:: Start FastAPI Backend in the background
echo Starting Backend API...
start /B venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000

:: Wait a moment for backend to initialize
timeout /t 3 /nobreak > nul

:: Start Streamlit Frontend
echo Starting Streamlit Dashboard...
venv\Scripts\streamlit.exe run streamlit_app.py

:: Note: When you close the terminal, the backend might still be running. 
:: You can find it in Task Manager under 'python.exe' if needed.
