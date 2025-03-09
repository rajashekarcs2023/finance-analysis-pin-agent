
# FinGenius - Personal Financial Advisor Agent powered by PIN AI

A sophisticated AI-powered agent that analyzes SEC filings and market data to provide personalized investment insights based on users' comprehensive financial profiles.

## Overview

This project implements a financial advisor agent using the PINAI Agent SDK and LangGraph. The agent combines:

- **Deeply Personalized Financial Advice**: Tailored recommendations based on detailed user financial profiles
- **SEC Filing Analysis**: Deep analysis of 10-K reports and other regulatory documents
- **Market Research**: Real-time market data and analyst opinions
- **Financial Planning**: Custom financial advice aligned with user's specific financial situation
- **Conversational Interface**: Natural dialogue with users about financial topics

## Features

- Integration with users' detailed financial profiles (income, expenses, debt, savings, investments)
- Multi-agent architecture for specialized financial analysis
- RAG (Retrieval Augmented Generation) for extracting insights from SEC documents
- Session management to maintain conversation context
- Financial goal-oriented recommendations that account for current financial status

## Technical Architecture

The system uses a supervisor-agent pattern with specialized workers:

1. **Supervisor**: Coordinates between specialized agents and determines which should handle each query
2. **SEC Analyst**: Analyzes regulatory filings to extract financial metrics and risk factors
3. **Search Agent**: Gathers current market data, news, and analyst opinions
4. **Financial Profile Analyzer**: Processes user financial data to create tailored recommendations

## Setup

### Prerequisites

- Python 3.8+
- Valid API keys for:
  - PINAI Agent SDK
  - OpenAI (or other LLM provider)
  - Tavily (for search capabilities)

### Installation

1. **Clone the repository**
   ```
   git clone [repository-url]
   cd financial-advisor-agent
   ```

2. **Create a virtual environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```
   pip install pinai-agent-sdk langchain langchain-openai langchain-community langchain-core langgraph langchain-asi openai tiktoken qdrant-client pymupdf tavily-python
   ```

4. **Set up environment variables**
   ```
   export PINAI_API_KEY="your-pinai-api-key"
   export OPENAI_API_KEY="your-openai-api-key"
   export TAVILY_API_KEY="your-tavily-api-key"
   ```

5. **Add SEC filings for analysis**
   - Download 10-K filings from the SEC website
   - Place them in the `data/raw/` directory

### Running the Agent

```
python main.py
```

## Project Structure

```
financial_advisor_agent/
│
├── main.py                  # Entry point for running the agent
│
├── agents/                  # Specialized agent implementations
│   ├── __init__.py
│   ├── search_agent.py      # Market research agent
│   ├── sec_agent.py         # SEC filings analysis agent
│   └── supervisor_agent.py  # Agent coordinator
│
├── graph/                   # LangGraph implementation
│   ├── __init__.py
│   └── research_graph.py    # Multi-agent orchestration
│
├── rag/                     # Retrieval Augmented Generation
│   ├── __init__.py
│   ├── chain.py             # RAG chain creation
│   └── loader.py            # Document loading utilities
│
├── utils/                   # Shared utilities
│   ├── __init__.py
│   └── helpers.py           # Helper functions
│
├── data/                    # Data storage
│   ├── raw/                 # SEC filings storage
│   └── processed/           # Processed data
│
└── requirements.txt         # Dependencies
```

## Financial Profile Integration

The agent analyzes detailed user financial data including:
- Income levels and sources
- Monthly expenses and budget categories
- Debt amounts and interest rates
- Savings and emergency funds
- Current investment portfolio and allocation
- Specific financial goals and timelines

This comprehensive profile allows for truly personalized financial advice that matches the user's exact financial situation, rather than generic recommendations.

## Example Usage

Users can ask questions like:
- "Given my current debt-to-income ratio, should I invest in Apple stock?"
- "With my student loan interest rate, would I be better off investing or paying down debt?"
- "Based on my current savings rate, what investment strategy would help me reach my retirement goals?"
- "Considering my emergency fund status, what level of investment risk is appropriate?"

## Future Enhancements

- Automated budget analysis based on spending patterns
- Debt repayment optimization strategies
- Tax-efficient investment recommendations
- Life event financial planning (education, home purchase, retirement)
- Portfolio rebalancing recommendations based on financial profile changes

## License

[License information]

## Contributors

[List of contributors]
