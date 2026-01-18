from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="AI-First CRM HCP Module")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "AI-First CRM HCP Module API", "status": "active"}

@app.post("/chat")
async def chat_endpoint(message: ChatMessage):
    # Simple response for now
    return {
        "response": f"Received: {message.message}. AI processing would happen here.",
        "action_taken": "general_chat",
        "tools_used": []
    }

@app.post("/log-interaction")
async def log_interaction_endpoint(message: ChatMessage):
    return {
        "status": "success",
        "response": f"Interaction logged: {message.message}",
        "tools_used": ["log_interaction"],
        "extracted_data": {
            "summary": "Sample interaction summary",
            "sentiment": "positive",
            "priority_level": "medium"
        }
    }

if __name__ == "__main__":
    print("Starting AI-First CRM Backend...")
    print("Server running on: http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)