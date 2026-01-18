@echo off
echo ========================================
echo    AI-First CRM - Quick Start
echo ========================================
echo.

echo [1/3] Installing Backend Dependencies...
cd backend
pip install fastapi uvicorn langgraph langchain langchain-groq python-dotenv sqlalchemy python-multipart

echo.
echo [2/3] Starting Backend Server...
python run.py