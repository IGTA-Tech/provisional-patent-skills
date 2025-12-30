"""
Configuration for Patent Opportunity Finder
============================================
Copy this file to config.py and add your API keys.
"""

import os

# =============================================================================
# API KEYS - Add your keys here
# =============================================================================

# Claude (Anthropic) API - For AI-powered analysis and drafting
ANTHROPIC_API_KEY = "your-anthropic-key-here"

# OpenAI API - Alternative AI provider
OPENAI_API_KEY = "your-openai-key-here"

# Perplexity API - For research with citations
PERPLEXITY_API_KEY = "your-perplexity-key-here"

# Krea AI API - For diagram/artwork generation
KREA_API_KEY = "your-krea-key-here"

# SendGrid API - For emailing patent results
SENDGRID_API_KEY = "your-sendgrid-key-here"
SENDGRID_FROM_EMAIL = "your-verified-sender@domain.com"

# =============================================================================
# PATENT API ENDPOINTS (No Auth Required)
# =============================================================================

# PatentsView API - USPTO Patent Database (12M+ patents)
PATENTSVIEW_API_URL = "https://search.patentsview.org/api/v1/patent/"
PATENTSVIEW_CPC_URL = "https://patentsview.org/apis/api-endpoints/cpc"

# PQAI API - AI-Powered Semantic Patent Search (Free for research)
PQAI_API_URL = "https://api.projectpq.ai"

# USPTO CPC Classification
USPTO_CPC_URL = "https://www.uspto.gov/web/patents/classification/"

# WIPO IPC Classification
WIPO_IPC_URL = "https://www.wipo.int/classifications/ipc/"

# Espacenet (EPO) - Global Patents
ESPACENET_URL = "https://worldwide.espacenet.com/"

# =============================================================================
# SETTINGS
# =============================================================================

# Default AI provider for drafting
DEFAULT_AI_PROVIDER = "claude"

# Default model for Claude
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# Default model for OpenAI
OPENAI_MODEL = "gpt-4o"

# Maximum tokens for patent drafting
MAX_DRAFT_TOKENS = 8000

# Default technology area for searches
DEFAULT_TECHNOLOGY = "ai"

# =============================================================================
# PATHS
# =============================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAG_DIR = os.path.join(BASE_DIR, "RAG")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_api_keys():
    """Get all configured API keys"""
    return {
        "claude_key": ANTHROPIC_API_KEY,
        "openai_key": OPENAI_API_KEY,
        "perplexity_key": PERPLEXITY_API_KEY,
        "diagram_key": KREA_API_KEY,
        "sendgrid_key": SENDGRID_API_KEY
    }

def get_available_providers():
    """Check which providers are configured"""
    providers = []
    if ANTHROPIC_API_KEY and not ANTHROPIC_API_KEY.startswith("your-"):
        providers.append("claude")
    if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("your-"):
        providers.append("openai")
    if PERPLEXITY_API_KEY and not PERPLEXITY_API_KEY.startswith("your-"):
        providers.append("perplexity")
    return providers

def get_patent_api_endpoints():
    """Get all patent API endpoints"""
    return {
        "patentsview": PATENTSVIEW_API_URL,
        "patentsview_cpc": PATENTSVIEW_CPC_URL,
        "pqai": PQAI_API_URL,
        "uspto_cpc": USPTO_CPC_URL,
        "wipo_ipc": WIPO_IPC_URL,
        "espacenet": ESPACENET_URL
    }
