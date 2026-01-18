import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.main import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting AI-First CRM Backend...")
    print("📍 Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)