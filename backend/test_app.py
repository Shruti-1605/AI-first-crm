from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

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
def root():
    return {"message": "Backend is working!", "status": "ok"}

@app.post("/chat")
def chat(message: ChatMessage):
    return {
        "response": "Thank you! I've processed your interaction details and the form has been auto-filled.",
        "action_taken": "processed",
        "tools_used": []
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Simple Backend...")
    print("http://localhost:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)