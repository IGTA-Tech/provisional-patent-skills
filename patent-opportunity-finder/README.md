# Patent Opportunity Finder

AI-powered tool for finding prior art, identifying patent opportunities, and drafting provisional patent applications.

## Features

- **Prior Art Search**: Search USPTO PatentsView API for relevant patents
- **Opportunity Finder**: Analyze prior art to identify patentable white space
- **Patent Drafter**: AI-powered provisional patent application drafting
- **Analysis Dashboard**: Visualize patent landscape and opportunities
- **Research Videos**: Access expert patent strategy knowledge

## Quick Start

```bash
# Navigate to the tool directory
cd patent-opportunity-finder

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Configuration

API keys are configured in `config.py`. The tool supports:

- **Claude (Anthropic)**: Primary AI for drafting and analysis
- **OpenAI (GPT-4)**: Alternative AI provider
- **Perplexity**: Research with citations
- **Krea AI**: Diagram/artwork generation

You can also set API keys via environment variables:
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `PERPLEXITY_API_KEY`
- `KREA_API_KEY`

## Modules

| Module | Purpose |
|--------|---------|
| `prior_art_search.py` | USPTO PatentsView API integration |
| `ai_providers.py` | Unified AI provider interface |
| `opportunity_finder.py` | Patent opportunity analysis |
| `patent_drafter.py` | Provisional patent generation |

## Usage Workflow

1. **Search Prior Art**: Enter technology keywords and search for existing patents
2. **Find Opportunities**: Analyze results to identify patent white space
3. **Draft Patent**: Use AI to generate complete provisional applications
4. **Review & Export**: Download drafts in various formats

## RAG Knowledge Bases

The tool references skill documents in the `../RAG/` folder:
- `invention-analyzing/` - Invention disclosure analysis
- `prior-art-researching/` - Prior art search strategies
- `patent-comparing/` - Comparative analysis methods
- `patentability-scoring/` - 100-point scoring rubric
- `provisional-patent-drafting/` - Drafting best practices
- `white-space-finder/` - Opportunity identification
- `patent-diagram-creating/` - Technical illustration guidance

## API Endpoints Used

- **USPTO PatentsView**: `https://search.patentsview.org/api/v1/patent/`
- **Claude API**: `https://api.anthropic.com/v1/messages`
- **OpenAI API**: `https://api.openai.com/v1/chat/completions`
- **Perplexity API**: `https://api.perplexity.ai/chat/completions`

## License

Proprietary - IGTA Tech
