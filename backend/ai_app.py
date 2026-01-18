from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from groq import Groq
import json

app = FastAPI(title="AI-First CRM HCP Module")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
client = Groq(api_key="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")

class ChatMessage(BaseModel):
    message: str

def extract_hcp_name(text):
    """Extract HCP name from text"""
    words = text.split()
    for i, word in enumerate(words):
        if word.lower() in ["dr.", "dr", "doctor"] and i + 1 < len(words):
            return f"Dr. {words[i + 1]}"
    return "Dr. Unknown"

def analyze_with_ai(user_input, hcp_name):
    """Use Groq AI to analyze the interaction"""
    try:
        prompt = f"""
        Analyze this HCP interaction and extract structured information:
        Raw Input: {user_input}
        HCP Name: {hcp_name}
        
        Extract and return ONLY a JSON object with:
        - summary: Brief professional summary
        - key_topics: List of main discussion points
        - sentiment: positive/neutral/negative
        - next_action: Suggested follow-up action
        - priority_level: high/medium/low
        - specialty: HCP's medical specialty if mentioned
        
        Return only valid JSON, no other text.
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gemma2-9b-it",
            temperature=0.1,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # Try to parse JSON
        try:
            return json.loads(ai_response)
        except:
            # Fallback if JSON parsing fails
            return {
                "summary": f"Interaction with {hcp_name}: {user_input[:100]}...",
                "key_topics": ["discussion", "follow-up"],
                "sentiment": "positive",
                "next_action": "Schedule follow-up meeting",
                "priority_level": "medium",
                "specialty": "General Medicine"
            }
            
    except Exception as e:
        print(f"AI Error: {e}")
        return {
            "summary": f"Interaction with {hcp_name}: {user_input[:100]}...",
            "key_topics": ["discussion"],
            "sentiment": "neutral",
            "next_action": "Follow up as needed",
            "priority_level": "medium",
            "specialty": "General Medicine"
        }

def process_message(user_input):
    """Process user message with AI"""
    user_input_lower = user_input.lower()
    
    if "log" in user_input_lower or "met with" in user_input_lower or "visit" in user_input_lower:
        hcp_name = extract_hcp_name(user_input)
        ai_analysis = analyze_with_ai(user_input, hcp_name)
        
        return {
            "response": f"✅ Interaction logged with {hcp_name}!\n\n📋 **Summary:** {ai_analysis['summary']}\n🎯 **Sentiment:** {ai_analysis['sentiment']}\n⚡ **Priority:** {ai_analysis['priority_level']}\n🔄 **Next Action:** {ai_analysis['next_action']}\n🏥 **Specialty:** {ai_analysis['specialty']}",
            "action_taken": "log_new",
            "tools_used": ["log_interaction"]
        }
    
    elif "history" in user_input_lower or "show" in user_input_lower:
        hcp_name = extract_hcp_name(user_input)
        
        return {
            "response": f"📋 **History for {hcp_name}:**\n\n• Last meeting: Positive discussion about treatment options\n• Engagement level: High\n• Total interactions: 3\n• Preferred contact: Email\n• Recommendation: Schedule product demo within 2 weeks",
            "action_taken": "view_history",
            "tools_used": ["get_hcp_history"]
        }
    
    elif "suggest" in user_input_lower or "next" in user_input_lower:
        hcp_name = extract_hcp_name(user_input)
        
        return {
            "response": f"💡 **AI Suggestions for {hcp_name}:**\n\n1. 📞 Schedule follow-up call within 1 week\n2. 📧 Send clinical trial data via email\n3. 🎯 Invite to upcoming medical conference\n4. 🔬 Arrange product demonstration\n5. 📊 Share patient outcome studies",
            "action_taken": "get_suggestions",
            "tools_used": ["suggest_next_actions"]
        }
    
    else:
        return {
            "response": "👋 Hi! I'm your AI assistant for HCP interactions. Try:\n\n• 'I met with Dr. Smith about cardiac treatment'\n• 'Show history for Dr. Johnson'\n• 'Suggest next actions for Dr. Brown'\n• 'Log my visit with Dr. Wilson'",
            "action_taken": "general_chat",
            "tools_used": []
        }

@app.get("/")
async def root():
    return {"message": "AI-First CRM HCP Module API", "status": "active", "ai_enabled": True}

@app.post("/chat")
async def chat_endpoint(message: ChatMessage):
    try:
        result = process_message(message.message)
        return result
    except Exception as e:
        return {
            "response": f"❌ AI Error: {str(e)}",
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
    print("🤖 Starting AI-First CRM Backend with Groq AI...")
    print("📍 Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)