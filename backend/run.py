import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Base, engine
from agent.main import app
import uvicorn

# Create database tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database setup complete!")

if __name__ == "__main__":
    print("Starting AI-First CRM Backend...")
    print("Server will run on: http://localhost:8000")
    print("API docs available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)