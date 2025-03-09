"""
Configuration settings for the financial advisor agent.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys from environment variables
PINAI_API_KEY = os.getenv("PINAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")
SEC_API_KEY = os.getenv("SEC_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# PIN.AI Agent settings
AGENT_ID = os.getenv("AGENT_ID", "177")  # Default to 177 if not specified
BASE_URL = os.getenv("PINAI_BASE_URL", "https://api.pin-ai.com/v1")
POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", "1"))

# File paths
DATA_DIR = "data"
RAW_DATA_DIR = f"{DATA_DIR}/raw"
PROCESSED_DATA_DIR = f"{DATA_DIR}/processed"

# Model settings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4-turbo-preview")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Search settings
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5")) 