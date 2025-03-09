import os
import sys
from pinai_agent_sdk import PINAIAgentSDK
from langchain_core.messages import HumanMessage

# Add parent directory to path to enable relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import project modules
from rag.chain import create_rag_chain
from graph.research_graph import create_research_graph, process_financial_query

# Initialize globals
active_sessions = {}

def handle_message(message):
    """
    Process incoming messages and respond
    Args:
        message (dict): Message object with format:
        {
            "session_id": "unique-session-id",
            "id": 12345, # Message ID
            "content": "user message text",
            "created_at": "2023-01-01T12:00:00"
        }
    """
    print(f"Received: {message['content']}")
    
    session_id = message.get("session_id")
    if not session_id:
        print("Message missing session_id, cannot respond")
        return
        
    # Get user's message
    user_message = message.get("content", "")
    
    # Get persona info
    try:
        persona_info = client.get_persona(session_id)
        print(f"Persona for session {session_id}: {persona_info}")
    except Exception as e:
        print(f"Error getting persona: {e}")
        persona_info = {"name": "there"}
    
    # Initialize session if it's new
    if session_id not in active_sessions:
        active_sessions[session_id] = {"history": []}
        welcome_msg = (
            f"Welcome {persona_info.get('name', 'there')}! I'm your Financial Advisor Agent. "
            "I can analyze SEC filings and market data to provide investment insights. "
            "What company would you like to research?"
        )
        client.send_message(content=welcome_msg)
        print(f"Sent welcome message to new session: {session_id}")
        return

    try:
        # Send a typing indicator to show we're processing
        client.send_message(content="Analyzing your financial query...", is_typing=True)
        
        # Process the query through our research graph
        result = process_financial_query(research_graph, user_message)
        
        # Extract the final message from the result
        if isinstance(result, dict) and "messages" in result and result["messages"]:
            final_message = result["messages"][-1].content
        else:
            final_message = str(result)
        
        # Send response back to user
        client.send_message(content=final_message)
        
        # Log the response
        print(f"Sent: Financial analysis response")
        print(f"session_id: {session_id}")
        
    except Exception as e:
        error_message = f"I encountered an error while analyzing your request: {str(e)}"
        client.send_message(content=error_message)
        print(f"Error: {str(e)}")

def main():
    # Get environment variables
    PINAI_API_KEY = os.environ.get("PINAI_API_KEY", "pin_MTI0MDAwMTY6MTY0OTY_L4AzqLCJlNpHymNZ")
    AGENT_ID = os.environ.get("AGENT_ID", "177")
    BASE_URL = os.environ.get("BASE_URL", "https://dev-agent.api.pinai.tech")
    POLLING_INTERVAL = float(os.environ.get("POLLING_INTERVAL", "1.0"))
    
    # Check for API key
    if not PINAI_API_KEY:
        print("Error: PINAI_API_KEY not set in environment")
        return
    
    global client, rag_chain, research_graph
    
    # Initialize client
    client = PINAIAgentSDK(
        api_key=PINAI_API_KEY,
        base_url=BASE_URL,
        polling_interval=POLLING_INTERVAL
    )
    
    # Initialize RAG chain and research graph
    try:
        print("Initializing RAG chain...")
        rag_chain = create_rag_chain("data/raw/apple_10k.pdf")
        
        print("Creating research graph...")
        research_graph = create_research_graph(rag_chain)
    except Exception as e:
        print(f"Error initializing components: {str(e)}")
        return
    
    print(f"Starting Financial Advisor Agent (ID: {AGENT_ID})...")
    
    try:
        # Start the agent
        client.start_and_run(
            on_message_callback=handle_message,
            agent_id=AGENT_ID
        )
    except KeyboardInterrupt:
        print("\nShutting down agent (user interrupt)")
    except Exception as e:
        print(f"Error running agent: {str(e)}")

if __name__ == "__main__":
    main()