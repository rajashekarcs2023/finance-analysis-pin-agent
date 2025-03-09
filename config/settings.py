"""
Configuration settings for the financial advisor agent.
"""

# API Keys (replace with your actual keys or use environment variables)
OPENAI_API_KEY = "your-openai-api-key"
SERP_API_KEY = "your-serp-api-key"
SEC_API_KEY = "your-sec-api-key"

# File paths
DATA_DIR = "data"
RAW_DATA_DIR = f"{DATA_DIR}/raw"
PROCESSED_DATA_DIR = f"{DATA_DIR}/processed"

# Model settings
DEFAULT_MODEL = "gpt-4"
EMBEDDING_MODEL = "text-embedding-ada-002"

# Search settings
MAX_SEARCH_RESULTS = 5 