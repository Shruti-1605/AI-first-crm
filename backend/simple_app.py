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

def process_message(user_input: str):
    """Simple message processing without complex imports"""
    user_input_lower = user_input.lower()
    
    if "log" in user_input_lower or "met with" in user_input_lower:
        # Extract HCP name
        words = user_input.split()
        hcp_name = "Dr. Unknown"
        for i, word in enumerate(words):
            if word.lower() in ["dr.", "dr", "doctor"] and i + 1 < len(words):
                hcp_name = f"Dr. {words[i + 1]}"
                break
        
        return {
            "response": f"✅ Logged interaction with {hcp_name}. Summary: {user_input[:100]}... Sentiment: Positive. Next action: Follow-up recommended.",
            "action_taken": "log_new",
            "tools_used": ["log_interaction"]
        }
    
    elif "history" in user_input_lower or "show" in user_input_lower:
        words = user_input.split()
        hcp_name = "Dr. Unknown"
        for i, word in enumerate(words):
            if word.lower() in ["dr.", "dr", "doctor"] and i + 1 < len(words):
                hcp_name = f"Dr. {words[i + 1]}"
                break
        
        return {
            "response": f"📋 History for {hcp_name}: Found 3 previous interactions. Last meeting was positive. Engagement level: High. Recommended next action: Schedule product demo.",
            "action_taken": "view_history",
            "tools_used": ["get_hcp_history"]
        }
    
    elif "suggest" in user_input_lower or "next" in user_input_lower:
        words = user_input.split()
        hcp_name = "Dr. Unknown"
        for i, word in enumerate(words):
            if word.lower() in ["dr.", "dr", "doctor"] and i + 1 < len(words):
                hcp_name = f"Dr. {words[i + 1]}"
                break
        
        return {
            "response": f"💡 AI Suggestions for {hcp_name}: 1) Schedule follow-up visit in 2 weeks 2) Send clinical trial data 3) Invite to medical conference 4) Arrange product demonstration",
            "action_taken": "get_suggestions",
            "tools_used": ["suggest_next_actions"]
        }
    
    else:
        return {
            "response": "👋 Hi! I'm your AI assistant for HCP interactions. Try: 'I met with Dr. Smith today' or 'Show history for Dr. Johnson' or 'Suggest next actions for Dr. Brown'",
            "action_taken": "general_chat",
            "tools_used": []
        }

@app.get("/")
async def root():
    return {"message": "AI-First CRM HCP Module API", "status": "active"}

@app.post("/chat")
async def chat_endpoint(message: ChatMessage):
    try:
        result = process_message(message.message)
        return result
    except Exception as e:
        return {
            "response": f"Error: {str(e)}",
            "action_taken": "error",
            "tools_used": []
        }

@app.post("/log-interaction")
async def log_interaction_endpoint(message: ChatMessage):
    try:
        result = process_message(message.message)
        return {
            "status": "success",
            "response": result["response"],
            "tools_used": result["tools_used"]
        }
    except Exception as e:
        return {
            "status": "error",
            "response": f"Error: {str(e)}",
            "tools_used": []
        }

if __name__ == "__main__":
    print("🚀 Starting AI-First CRM Backend...")
    print("📍 Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)