from langchain.tools import tool
from typing import Dict, Any
import json

@tool
def log_interaction(raw_input: str, hcp_name: str, interaction_type: str = "visit") -> Dict[str, Any]:
    """
    Logs interaction with HCP using AI to extract and structure data from raw input.
    """
    try:
        # Simple mock response for now
        extracted_data = {
            "summary": f"Interaction with {hcp_name}: {raw_input[:100]}...",
            "key_topics": ["discussion", "follow-up"],
            "sentiment": "positive",
            "next_action": "Schedule follow-up meeting",
            "priority_level": "medium",
            "specialty": "General Medicine"
        }
        
        return {
            "status": "success",
            "interaction_id": 1,
            "extracted_data": extracted_data,
            "message": "Interaction logged successfully"
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@tool
def edit_interaction(interaction_id: int, updated_notes: str = None, updated_summary: str = None) -> Dict[str, Any]:
    """
    Edit existing interaction with AI re-analysis if notes are updated.
    """
    try:
        return {
            "status": "success",
            "message": "Interaction updated successfully",
            "interaction_id": interaction_id
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@tool
def get_hcp_history(hcp_name: str, limit: int = 10) -> Dict[str, Any]:
    """
    Fetch comprehensive interaction history for an HCP.
    """
    try:
        mock_interactions = [{
            "id": 1,
            "date": "2024-01-17T10:00:00",
            "type": "visit",
            "summary": f"Previous interaction with {hcp_name}",
            "sentiment": "positive",
            "priority": "medium"
        }]
        
        return {
            "status": "success",
            "hcp_name": hcp_name,
            "total_interactions": 1,
            "interactions": mock_interactions,
            "ai_insights": f"Good relationship with {hcp_name}. Regular engagement recommended."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@tool
def analyze_interaction_trends(days: int = 30) -> Dict[str, Any]:
    """
    Analyze interaction trends and patterns using AI for strategic insights.
    """
    try:
        trend_data = {
            "total_interactions": 5,
            "sentiment_distribution": {"positive": 3, "neutral": 2},
            "interaction_types": {"visit": 3, "call": 2},
            "priority_levels": {"high": 1, "medium": 3, "low": 1}
        }
        
        return {
            "status": "success",
            "period_days": days,
            "raw_data": trend_data,
            "ai_analysis": "Overall positive trend in interactions. Engagement levels are good."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@tool
def suggest_next_actions(hcp_name: str) -> Dict[str, Any]:
    """
    AI-powered suggestions for next actions based on HCP interaction history.
    """
    try:
        suggestions = f"""
        Suggested actions for {hcp_name}:
        1. Schedule follow-up visit within 2 weeks
        2. Send product information via email
        3. Invite to upcoming medical conference
        4. Arrange product demonstration
        """
        
        return {
            "status": "success",
            "hcp_name": hcp_name,
            "ai_suggestions": suggestions,
            "based_on_interactions": 3
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}