from typing import TypedDict, List
from tools import (
    log_interaction,
    edit_interaction, 
    get_hcp_history,
    analyze_interaction_trends,
    suggest_next_actions
)

class AgentState(TypedDict):
    input: str
    response: str
    tools_used: List[str]

def simple_agent(user_input: str):
    """
    Simple agent that processes user input and returns appropriate response
    """
    user_input_lower = user_input.lower()
    
    if "log" in user_input_lower or "met with" in user_input_lower:
        # Extract HCP name (simple approach)
        words = user_input.split()
        hcp_name = "Dr. Unknown"
        for i, word in enumerate(words):
            if word.lower() in ["dr.", "dr", "doctor"] and i + 1 < len(words):
                hcp_name = f"Dr. {words[i + 1]}"
                break
        
        result = log_interaction.invoke({
            "raw_input": user_input,
            "hcp_name": hcp_name,
            "interaction_type": "visit"
        })
        
        return {
            "response": f"✅ Logged interaction with {hcp_name}. Summary: {result['extracted_data']['summary']}",
            "tools_used": ["log_interaction"],
            "current_action": "log_new"
        }
    
    elif "history" in user_input_lower or "show" in user_input_lower:
        # Extract HCP name
        words = user_input.split()
        hcp_name = "Dr. Unknown"
        for i, word in enumerate(words):
            if word.lower() in ["dr.", "dr", "doctor"] and i + 1 < len(words):
                hcp_name = f"Dr. {words[i + 1]}"
                break
        
        result = get_hcp_history.invoke({"hcp_name": hcp_name})
        
        return {
            "response": f"📋 History for {hcp_name}: {result['total_interactions']} interactions found. {result['ai_insights']}",
            "tools_used": ["get_hcp_history"],
            "current_action": "view_history"
        }
    
    elif "suggest" in user_input_lower or "next" in user_input_lower:
        # Extract HCP name
        words = user_input.split()
        hcp_name = "Dr. Unknown"
        for i, word in enumerate(words):
            if word.lower() in ["dr.", "dr", "doctor"] and i + 1 < len(words):
                hcp_name = f"Dr. {words[i + 1]}"
                break
        
        result = suggest_next_actions.invoke({"hcp_name": hcp_name})
        
        return {
            "response": f"💡 Suggestions for {hcp_name}: {result['ai_suggestions']}",
            "tools_used": ["suggest_next_actions"],
            "current_action": "get_suggestions"
        }
    
    else:
        return {
            "response": "👋 Hi! I can help you log HCP interactions. Try: 'I met with Dr. Smith today' or 'Show history for Dr. Johnson'",
            "tools_used": [],
            "current_action": "general_chat"
        }

# Simple graph simulation
class InteractionGraph:
    def invoke(self, state):
        user_input = state.get("input", "")
        return simple_agent(user_input)

interaction_graph = InteractionGraph()