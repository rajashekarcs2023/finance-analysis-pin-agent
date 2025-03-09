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
        active_sessions[session_id] = {"history": [], "persona": persona_info}
        welcome_msg = (
            f"Welcome {persona_info.get('name', 'there')}! I'm your Financial Advisor Agent. "
            "I can analyze SEC filings and market data to provide investment insights. "
            "I'll start processing your query right away."
        )
        client.send_message(content=welcome_msg)
        print(f"Sent welcome message to new session: {session_id}")
        # Continue to process the query immediately
    else:
        # Update persona info in case it changed
        active_sessions[session_id]["persona"] = persona_info

    try:
        # Notify user that processing has begun
        client.send_message(content="Analyzing your financial query...")
        
        # Extract relevant persona data to enhance the query
        enhanced_query = enrich_query_with_persona(user_message, persona_info)
        print(f"Enhanced query: {enhanced_query}")
        
        # Process the query through our research graph
        result = process_financial_query(research_graph, enhanced_query)
        
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

def extract_financial_profile(persona_info):
    """
    Extract financial profile information from persona data.
    
    Args:
        persona_info (dict): User persona information
        
    Returns:
        dict: Financial profile with relevant financial information
    """
    # Extract financial profile from persona data
    data = persona_info.get('data', {})
    
    # Look for financial-related fields in the persona data
    financial_profile = {}
    
    # Extract direct financial profile if it exists
    if 'financial_profile' in data:
        financial_profile = data['financial_profile']
    else:
        # Try to extract individual financial fields
        financial_fields = [
            'risk_tolerance',
            'investment_horizon',
            'investment_goals',
            'current_investments',
            'apple_investment',
            'sectors_of_interest',
            'annual_income',
            'income_range',
            'financial_concerns',
            'investment_experience',
            'portfolio_value',
            'retirement_plans',
            'tax_situation'
        ]
        
        for field in financial_fields:
            if field in data:
                financial_profile[field] = data[field]
        
        # Look for Apple-specific investment information
        apple_fields = [field for field in data.keys() if 'apple' in field.lower()]
        if apple_fields and 'apple_investment' not in financial_profile:
            financial_profile['apple_investment'] = {}
            for field in apple_fields:
                financial_profile['apple_investment'][field.replace('apple_', '')] = data[field]
    
    # Extract purchase history for financial insights if available
    if 'purchase_history' in data:
        try:
            purchases = data['purchase_history'].get('Data', [])
            tech_purchases = []
            apple_purchases = []
            
            for purchase_data in purchases:
                if 'purchase_history' in purchase_data:
                    for item in purchase_data.get('purchase_history', []):
                        # Extract tech and Apple purchases
                        categories = item.get('categories', [])
                        brand = item.get('brand', '').lower()
                        
                        if 'Electronics' in categories or 'Technology' in categories:
                            tech_purchases.append(item)
                        
                        if 'apple' in brand:
                            apple_purchases.append(item)
            
            if tech_purchases:
                financial_profile['tech_purchases'] = len(tech_purchases)
            
            if apple_purchases:
                if 'apple_investment' not in financial_profile:
                    financial_profile['apple_investment'] = {}
                financial_profile['apple_investment']['product_purchases'] = len(apple_purchases)
        except Exception as e:
            print(f"Error processing purchase history: {e}")
    
    return financial_profile

def enrich_query_with_persona(query, persona_info):
    """
    Enhance the user query with relevant persona information.
    
    Args:
        query (str): Original user query
        persona_info (dict): User persona information
        
    Returns:
        str: Enhanced query with persona context
    """
    # Extract basic persona data
    name = persona_info.get('name', '')
    occupation = persona_info.get('data', {}).get('occupation', '')
    interests = persona_info.get('data', {}).get('interests', [])
    
    # Extract financial profile
    financial_profile = extract_financial_profile(persona_info)
    
    # Create context string from persona data
    context = ""
    if name:
        context += f"For {name}"
    if occupation:
        context += f", who is a {occupation}"
    if interests:
        interest_str = ", ".join(interests[:3])  # Limit to first 3 interests
        context += f", with interests in {interest_str}"
    
    # Add financial profile information
    financial_context = []
    
    # Add key financial information if available
    for key in ['risk_tolerance', 'investment_horizon', 'investment_experience']:
        if key in financial_profile:
            financial_context.append(f"{key.replace('_', ' ')}: {financial_profile[key]}")
    
    # Add investment goals if available
    if 'investment_goals' in financial_profile:
        goals = financial_profile['investment_goals']
        if isinstance(goals, list):
            goals_str = ", ".join(goals[:3])
        else:
            goals_str = str(goals)
        financial_context.append(f"investment goals: {goals_str}")
    
    # Add Apple-specific investment information
    apple_investment = financial_profile.get('apple_investment', {})
    if apple_investment:
        apple_context = []
        for key, value in apple_investment.items():
            if key in ['owns_shares', 'percentage_of_portfolio', 'holding_period', 'average_cost_basis', 'investment_thesis']:
                apple_context.append(f"{key.replace('_', ' ')}: {value}")
        
        if apple_context:
            financial_context.append(f"Apple investment: {'; '.join(apple_context)}")
    
    # Add sectors of interest
    if 'sectors_of_interest' in financial_profile:
        sectors = financial_profile['sectors_of_interest']
        if isinstance(sectors, list):
            sectors_str = ", ".join(sectors[:3])
        else:
            sectors_str = str(sectors)
        financial_context.append(f"interested in sectors: {sectors_str}")
    
    # Add financial concerns
    if 'financial_concerns' in financial_profile:
        concerns = financial_profile['financial_concerns']
        if isinstance(concerns, list):
            concerns_str = ", ".join(concerns[:2])
        else:
            concerns_str = str(concerns)
        financial_context.append(f"concerned about: {concerns_str}")
    
    # Add the financial context to the overall context
    if financial_context:
        context += f". Financial profile: {'; '.join(financial_context)}"
    
    # Combine original query with persona context
    if context:
        enhanced_query = f"{query} [Context: {context}. Tailor the financial analysis to this person's profile and their interest in Apple investments.]"
    else:
        enhanced_query = query
        
    return enhanced_query

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