from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph_agent import interaction_graph

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

class InteractionInput(BaseModel):
    input: str
    hcp_name: str = None
    interaction_type: str = "visit"

@app.get("/")
async def root():
    return {"message": "AI-First CRM HCP Module API", "status": "active"}

@app.post("/chat")
async def chat_endpoint(message: ChatMessage):
    try:
        result = interaction_graph.invoke({"input": message.message})
        return {
            "response": result["response"],
            "action_taken": result["current_action"],
            "tools_used": result["tools_used"]
        }
    except Exception as e:
        return {
            "response": f"Error: {str(e)}",
            "action_taken": "error",
            "tools_used": []
        }

@app.post("/log-interaction")
async def log_interaction_endpoint(input_data: InteractionInput):
    try:
        result = interaction_graph.invoke({"input": input_data.input})
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
    import uvicorn
    print("🚀 Starting AI-First CRM Backend...")
    print("📍 Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)