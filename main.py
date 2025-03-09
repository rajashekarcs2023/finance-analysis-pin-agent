import os
import sys
from pinai_agent_sdk import PINAIAgentSDK
from langchain_core.messages import HumanMessage

# Add parent directory to path to enable relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import project modules
from config.settings import PINAI_API_KEY, AGENT_ID, BASE_URL, POLLING_INTERVAL
from rag.chain import create_rag_chain
from graph.research_graph import create_research_graph, process_financial_query

# Initialize globals
active_sessions = {}

def handle_message(message):
    """Process incoming messages and respond with financial analysis"""
    # Implementation from previous response
    # ...

def main():
    # Check for API key
    if not PINAI_API_KEY:
        print("Error: PINAI_API_KEY not set in environment")
        return
        
    # Initialize client
    client = PINAIAgentSDK(
        api_key=PINAI_API_KEY,
        base_url=BASE_URL,
        polling_interval=POLLING_INTERVAL
    )
    
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