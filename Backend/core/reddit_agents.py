from agents import Agent, WebSearchTool, Runner, trace
from functions import supabase
from prompts import prompt_0, prompt_1, prompt_2, prompt_3, prompt_4
from functions import (
    check_subreddit_exists,
    scrape_subreddit_posts,
    calculate_pain_score,
    store_exceptional_solution,
    get_stored_solutions,
    export_final_report,
    export_exceptional_solutions,
    export_both_reports
)

# Agent 0 - RouterAgent
agent_0 = Agent(
    name="RouterAgent", 
    instructions=prompt_0,
    tools=[
        WebSearchTool(),
        check_subreddit_exists,
        get_stored_solutions,
        export_final_report,
        export_exceptional_solutions,
        export_both_reports
    ], 
    model="gpt-4o-mini"
)

# Agent 2 - ScrapingAgent (converti en tool)
agent_2 = Agent(
    name="ScrapingAgent",
    instructions=prompt_2,
    tools=[
        scrape_subreddit_posts
    ],
    model="gpt-4o-mini"
)

# Agent 3 - PainAnalysisAgent (converti en tool)
agent_3 = Agent(
    name="PainAnalysisAgent",
    instructions=prompt_3,
    tools=[
        calculate_pain_score,
        store_exceptional_solution,
        get_stored_solutions
    ],
    model="gpt-4o-mini"
)

# Agent 4 - RecommendationsAgent (converti en tool)
agent_4 = Agent(
    name="RecommendationsAgent",
    instructions=prompt_4,
    tools=[],
    model="gpt-4o-mini"
)

# Convertir les agents en tools
Scraper_tool = agent_2.as_tool(tool_name="scraper_tool", tool_description="scrape a subreddit")
PainAnalysis_tool = agent_3.as_tool(tool_name="pain_analysis_tool", tool_description="analyze the pain of a subreddit")
Recommendations_tool = agent_4.as_tool(tool_name="recommendations_tool", tool_description="generate recommendations")


# Agent 1 - WorkflowManager (avec les tools)
agent_1 = Agent(
    name="WorkflowManager",
    instructions=prompt_1,
    tools=[
        Scraper_tool,
        PainAnalysis_tool,
        Recommendations_tool
    ],
    model="gpt-4o-mini"
)

agent_0.handoffs = [agent_1]
agent_1.handoffs = [agent_0]

# Agent principal pour l'export
ROUTER_AGENT = agent_0




async def run_chat(message: str, session_id: str = "default") -> dict:
    """
    Fonction principale pour le chat avec l'agent RouterAgent
    (Adapté Version_00 pour Supabase)
    """
    try:
        # Construire le contexte avec l'historique
        context = get_conversation_history(session_id)
        full_context = f"{context}\nHumain: {message}\nAssistant: "
        
        # Lancer l'agent principal
        with trace(f"chat_session_{session_id}"):
            result = await Runner.run(agent_0, full_context)
            
            # Sauvegarder dans l'historique
            save_to_history(session_id, message, result.final_output)
            
            return {
                "success": True,
                "response": result.final_output,
                "session_id": session_id
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "session_id": session_id
        }

def get_conversation_history(session_id: str) -> str:
    """
    Récupère l'historique de conversation depuis Supabase
    """
    try:
        result = supabase.table("conversation_history").select("user_message, agent_response").eq("session_id", session_id).order("timestamp", desc=False).execute()
        
        context = ""
        for msg in result.data:
            context += f"Humain: {msg['user_message']}\nAssistant: {msg['agent_response']}\n"
        
        return context
        
    except Exception:
        return ""

def save_to_history(session_id: str, user_message: str, agent_response: str):
    """
    Sauvegarde un échange dans l'historique Supabase
    """
    try:
        supabase.table("conversation_history").insert({
            "session_id": session_id,
            "user_message": user_message,
            "agent_response": agent_response
        }).execute()
        
    except Exception as e:
        print(f"Erreur sauvegarde historique: {e}")

def clear_conversation_history(session_id: str):
    """
    Efface l'historique de conversation
    """
    try:
        supabase.table("conversation_history").delete().eq("session_id", session_id).execute()
        
    except Exception as e:
        print(f"Erreur nettoyage historique: {e}")