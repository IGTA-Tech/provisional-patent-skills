"""
Configuration for Patent Opportunity Finder
============================================
Store API keys and settings here.

SECURITY NOTE: Set API keys via environment variables or create a local .env file.
Copy config.example.py to config.py and add your keys there (config.py is gitignored).
"""

import os

# =============================================================================
# API KEYS (set via environment variables)
# =============================================================================

# Claude (Anthropic) API - For AI-powered analysis and drafting
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# OpenAI API - Alternative AI provider
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Perplexity API - For research with citations
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")

# Krea AI API - For diagram/artwork generation
KREA_API_KEY = os.getenv("KREA_API_KEY", "")

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
        "diagram_key": KREA_API_KEY
    }

def get_available_providers():
    """Check which providers are configured"""
    providers = []
    if ANTHROPIC_API_KEY:
        providers.append("claude")
    if OPENAI_API_KEY:
        providers.append("openai")
    if PERPLEXITY_API_KEY:
        providers.append("perplexity")
    return providers
