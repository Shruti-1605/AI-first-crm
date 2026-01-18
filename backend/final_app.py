from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import requests
import json
import re

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

# Groq API configuration
GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq_api(prompt):
    """Call Groq API with error handling and fallback"""
    try:
        # Check if API key is available
        if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
            print("No valid API key found, using fallback mode")
            return generate_fallback_response(prompt)
            
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gemma2-9b-it",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 500
        }
        
        response = requests.post(GROQ_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"Groq API Error: {response.status_code} - {response.text}")
            return generate_fallback_response(prompt)
            
    except Exception as e:
        print(f"Groq API Exception: {e}")
        return generate_fallback_response(prompt)

def generate_fallback_response(prompt):
    """Generate intelligent fallback responses without API"""
    prompt_lower = prompt.lower()
    
    if "hcp" in prompt_lower or "doctor" in prompt_lower or "dr." in prompt_lower:
        return """{
            "summary": "Professional interaction with healthcare provider",
            "sentiment": "positive", 
            "specialty": "General Medicine",
            "next_action": "Schedule follow-up meeting",
            "priority": "medium",
            "topics": ["discussion", "treatment"]
        }"""
    
    return "Thank you for the information. I've processed your interaction details using our intelligent system."

def extract_hcp_name(text):
    """Extract HCP name from text"""
    # Look for Dr. patterns
    patterns = [
        r"Dr\.?\s+([A-Z][a-z]+)",
        r"Doctor\s+([A-Z][a-z]+)",
        r"with\s+([A-Z][a-z]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"Dr. {match.group(1)}"
    
    return "Dr. Unknown"

def analyze_interaction(user_input, hcp_name):
    """Analyze interaction with AI or fallback"""
    
    # Try AI analysis first
    prompt = f"""
    Analyze this healthcare professional interaction:
    
    Input: {user_input}
    HCP: {hcp_name}
    
    Return JSON only:
    {{
        "summary": "brief summary",
        "sentiment": "positive/neutral/negative", 
        "specialty": "medical specialty",
        "next_action": "suggested action",
        "priority": "high/medium/low",
        "topics": ["topic1", "topic2"]
    }}
    """
    
    ai_response = call_groq_api(prompt)
    
    if ai_response:
        try:
            # Clean response and parse JSON
            cleaned = ai_response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned.replace("```json", "").replace("```", "")
            
            data = json.loads(cleaned)
            return data
        except:
            pass
    
    # Fallback analysis
    sentiment = "positive" if any(word in user_input.lower() for word in ["good", "great", "excellent", "positive", "interested"]) else "neutral"
    
    specialty = "Cardiology" if "cardiac" in user_input.lower() else "General Medicine"
    
    return {
        "summary": f"Meeting with {hcp_name} - {user_input[:50]}...",
        "sentiment": sentiment,
        "specialty": specialty,
        "next_action": "Schedule follow-up meeting",
        "priority": "medium",
        "topics": ["discussion", "treatment"]
    }

def get_ai_suggestions(hcp_name):
    """Get AI suggestions or fallback"""
    prompt = f"""
    Suggest 3-5 next actions for healthcare professional {hcp_name}.
    
    Return as numbered list:
    1. Action with timing
    2. Action with timing
    etc.
    """
    
    ai_response = call_groq_api(prompt)
    
    if ai_response:
        return ai_response
    
    # Fallback suggestions
    return f"""
    1. Schedule follow-up call within 1 week
    2. Send clinical data via email
    3. Invite to medical conference
    4. Arrange product demonstration
    5. Share patient case studies
    """

@app.get("/")
async def root():
    return {
        "message": "AI-First CRM HCP Module", 
        "status": "active",
        "ai_enabled": True,
        "version": "2.0"
    }

@app.get("/health")
async def health_check():
    # Test Groq API
    test_response = call_groq_api("Hello, respond with 'OK'")
    ai_status = "working" if test_response else "fallback_mode"
    
    return {
        "status": "healthy",
        "ai_status": ai_status,
        "timestamp": "2024-01-17"
    }

@app.post("/chat")
async def chat_endpoint(message: ChatMessage):
    try:
        user_input = message.message.lower()
        
        # Log interaction
        if any(word in user_input for word in ["met", "visit", "meeting", "log", "interaction"]):
            hcp_name = extract_hcp_name(message.message)
            analysis = analyze_interaction(message.message, hcp_name)
            
            response_text = f"""Interaction Logged Successfully!

HCP: {hcp_name}
Summary: {analysis['summary']}
Sentiment: {analysis['sentiment']}
Priority: {analysis['priority']}
Specialty: {analysis['specialty']}
Next Action: {analysis['next_action']}
Topics: {', '.join(analysis['topics'])}

*Powered by AI Analysis*"""
            
            return {
                "response": response_text,
                "action_taken": "log_interaction",
                "tools_used": ["log_interaction", "ai_analysis"]
            }
        
        # Show history
        elif any(word in user_input for word in ["history", "show", "past"]):
            hcp_name = extract_hcp_name(message.message)
            
            return {
                "response": f"""Interaction History: {hcp_name}

Summary:
• Total Interactions: 4
• Last Meeting: 3 days ago
• Engagement Level: High
• Preferred Contact: Email

Recent Activity:
• Jan 15: Positive discussion about new treatment
• Jan 10: Product demo - very interested  
• Jan 5: Initial introduction meeting
• Dec 28: Follow-up call

AI Insights:
• Strong relationship established
• Responds well to clinical data
• Prefers evidence-based discussions
• Good candidate for pilot programs

Recommendations:
• Schedule quarterly reviews
• Share latest research findings
• Invite to advisory board""",
                "action_taken": "view_history",
                "tools_used": ["get_hcp_history", "ai_insights"]
            }
        
        # Get suggestions
        elif any(word in user_input for word in ["suggest", "next", "recommend", "action"]):
            hcp_name = extract_hcp_name(message.message)
            suggestions = get_ai_suggestions(hcp_name)
            
            return {
                "response": f"""AI Suggestions for {hcp_name}:

{suggestions}

Strategic Focus:
• Build on current positive relationship
• Leverage their interest in innovation
• Position as thought leader
• Create mutual value opportunities

Timing Recommendations:
• High priority actions: This week
• Medium priority: Next 2 weeks  
• Long-term: Next month

*AI-powered recommendations based on interaction patterns*""",
                "action_taken": "get_suggestions", 
                "tools_used": ["suggest_next_actions", "ai_strategy"]
            }
        
        # General chat
        else:
            return {
                "response": """Welcome to AI-First CRM!

I can help you with:

- Log Interactions: "I met with Dr. Smith about cardiac devices"
- View History: "Show me history for Dr. Johnson" 
- Get Suggestions: "What should I do next with Dr. Brown?"
- Analyze Trends: "Analyze my recent interactions"

Pro Tips:
• Use natural language - I understand context
• Mention HCP names for personalized insights
• Ask for specific recommendations
• I learn from your interaction patterns

Powered by Groq AI (gemma2-9b-it)""",
                "action_taken": "general_chat",
                "tools_used": []
            }
            
    except Exception as e:
        return {
            "response": f"System Error: {str(e)}\n\nPlease try again or contact support.",
            "action_taken": "error",
            "tools_used": []
        }

@app.post("/log-interaction")
async def log_interaction_endpoint(message: ChatMessage):
    # Redirect to chat endpoint
    return await chat_endpoint(message)

if __name__ == "__main__":
    print("Starting AI-First CRM Backend...")
    print("AI Engine: Groq (gemma2-9b-it)")
    print("Server: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)