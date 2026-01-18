@echo off
echo Starting AI-First CRM Frontend...
echo.

cd /d "%~dp0frontend"

echo Installing Node.js dependencies...
npm install

echo.
echo Starting React development server on http://localhost:3000
echo The application will open in your browser automatically
echo Press Ctrl+C to stop the server
echo.

npm start