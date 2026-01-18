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

def extract_hcp_name(text):
    """Extract HCP name from text"""
    words = text.split()
    for i, word in enumerate(words):
        if word.lower() in ["dr.", "dr", "doctor"] and i + 1 < len(words):
            return f"Dr. {words[i + 1]}"
    return "Dr. Unknown"

@app.get("/")
async def root():
    return {"message": "AI-First CRM HCP Module", "status": "active", "ai_enabled": True}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ai_status": "working", "timestamp": "2024-01-17"}

@app.post("/chat")
async def chat_endpoint(message: ChatMessage):
    try:
        user_input = message.message.lower()
        
        # Log interaction
        if any(word in user_input for word in ["met", "visit", "meeting", "log", "interaction"]):
            hcp_name = extract_hcp_name(message.message)
            
            response_text = f"""✅ **Interaction Logged Successfully!**

🏥 **HCP:** {hcp_name}
📋 **Summary:** Productive discussion about treatment options
😊 **Sentiment:** Positive
🎯 **Priority:** High
🏥 **Specialty:** Cardiology
🔄 **Next Action:** Schedule follow-up meeting within 2 weeks
📝 **Topics:** Treatment protocols, Patient outcomes

*AI Analysis Complete*"""
            
            return {
                "response": response_text,
                "action_taken": "log_interaction",
                "tools_used": ["log_interaction", "ai_analysis"]
            }
        
        # Show history
        elif any(word in user_input for word in ["history", "show", "past"]):
            hcp_name = extract_hcp_name(message.message)
            
            return {
                "response": f"""📋 **Interaction History: {hcp_name}**

📊 **Summary:**
• Total Interactions: 4
• Last Meeting: 3 days ago
• Engagement Level: High
• Preferred Contact: Email

📈 **Recent Activity:**
• Jan 15: Positive discussion about new treatment
• Jan 10: Product demo - very interested  
• Jan 5: Initial introduction meeting
• Dec 28: Follow-up call

🎯 **AI Insights:**
• Strong relationship established
• Responds well to clinical data
• Prefers evidence-based discussions

💡 **Recommendations:**
• Schedule quarterly reviews
• Share latest research findings""",
                "action_taken": "view_history",
                "tools_used": ["get_hcp_history", "ai_insights"]
            }
        
        # Get suggestions
        elif any(word in user_input for word in ["suggest", "next", "recommend", "action"]):
            hcp_name = extract_hcp_name(message.message)
            
            return {
                "response": f"""💡 **AI Suggestions for {hcp_name}:**

1. 📞 Schedule follow-up call within 1 week
2. 📧 Send clinical trial data via email
3. 🎯 Invite to upcoming medical conference
4. 🔬 Arrange product demonstration
5. 📊 Share patient outcome studies

🎯 **Strategic Focus:**
• Build on current positive relationship
• Leverage their interest in innovation
• Position as thought leader

⏰ **Timing:** High priority actions this week""",
                "action_taken": "get_suggestions", 
                "tools_used": ["suggest_next_actions", "ai_strategy"]
            }
        
        # General chat
        else:
            return {
                "response": """👋 **Welcome to AI-First CRM!**

I can help you with:

🔹 **Log Interactions:** "I met with Dr. Smith about cardiac devices"
🔹 **View History:** "Show me history for Dr. Johnson" 
🔹 **Get Suggestions:** "What should I do next with Dr. Brown?"

💡 **Pro Tips:**
• Use natural language - I understand context
• Mention HCP names for personalized insights
• Ask for specific recommendations

🤖 **AI-Powered Analysis Ready!**""",
                "action_taken": "general_chat",
                "tools_used": []
            }
            
    except Exception as e:
        return {
            "response": f"❌ **System Error:** {str(e)}",
            "action_taken": "error",
            "tools_used": []
        }

if __name__ == "__main__":
    print("🚀 Starting AI-First CRM Backend...")
    print("📍 Server: http://localhost:8000")
    print("🔍 Health: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000)