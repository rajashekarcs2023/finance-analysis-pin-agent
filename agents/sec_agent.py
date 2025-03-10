from utils.helpers import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool

def create_sec_agent(llm: ChatOpenAI, rag_chain):
    """Create an agent specialized in SEC filings analysis."""
    
    system_prompt = """You are a financial analyst specialized in SEC filings analysis.
    
    IMPORTANT: The user query includes their financial profile in [Context: ...] format.
    Always tailor your analysis to this profile, especially considering:
    - Risk tolerance (conservative, moderate, aggressive)
    - Investment horizon (short-term, medium-term, long-term)
    - Specific Apple investment details
    - Financial concerns
    
    After analyzing SEC filings:
    1. If you need market context, clearly state what specific market data you need
    2. If numbers need industry comparison, explicitly request competitor data
    3. Always include specific numbers and trends from the filings
    4. If you spot significant changes or unusual patterns, highlight them
    5. Relate your findings to the user's specific financial situation and concerns
    6. Provide different perspectives based on their risk tolerance
    
    Format your response as:
    1. Data from SEC Filings: [your findings]
    2. Additional Context Needed: [if any]
    3. Analysis: [your insights]
    4. Personalized Implications: [tailored to user's financial profile]
    """
    
    retrieve_tool = Tool(
        name="retrieve_information",
        func=lambda x: rag_chain.invoke(x),
        description="""Use this tool to analyze SEC filings and extract specific 
        information from financial documents. Input should be a clear question 
        about financial metrics, risks, or statements."""
    )
    
    return create_agent(
        llm=llm,
        tools=[retrieve_tool],
        system_prompt=system_prompt
    )