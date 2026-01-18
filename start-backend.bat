@echo off
echo Starting AI-First CRM Backend Server...
echo.

cd /d "%~dp0backend"

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

cd agent
python main.py