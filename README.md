# Patent Opportunity Finder & Skills Toolkit

AI-powered tool for finding prior art, identifying patent opportunities, and drafting provisional patent applications.

## Quick Start

```bash
git clone https://github.com/IGTA-Tech/provisional-patent-skills.git
cd provisional-patent-skills/patent-opportunity-finder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config.example.py config.py
# Edit config.py with your API keys
streamlit run app.py
```

Opens at **http://localhost:8501**

---

## Deployment Guide

### Option 1: Streamlit Community Cloud (Recommended - Free)

1. Fork repo to your GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. New app → Select repo → Branch: `main` → File: `patent-opportunity-finder/app.py`
4. Add secrets in dashboard:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   OPENAI_API_KEY = "sk-proj-..."
   PERPLEXITY_API_KEY = "pplx-..."
   KREA_API_KEY = "..."
   ```
5. Deploy

### Option 2: VPS/Cloud Server

```bash
# On Ubuntu server
sudo apt update && sudo apt install python3.11 python3.11-venv git -y
git clone https://github.com/IGTA-Tech/provisional-patent-skills.git
cd provisional-patent-skills/patent-opportunity-finder
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp config.example.py config.py && nano config.py  # Add API keys

# Run in background
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
```

### Option 3: Docker

```dockerfile
# Add to patent-opportunity-finder/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t patent-finder patent-opportunity-finder/
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=... patent-finder
```

---

## API Keys Required

| Service | Purpose | Get Key |
|---------|---------|---------|
| **Anthropic (Claude)** | Primary AI | [console.anthropic.com](https://console.anthropic.com) |
| **OpenAI** | Alternative AI | [platform.openai.com](https://platform.openai.com) |
| **Perplexity** | Research | [perplexity.ai](https://www.perplexity.ai) |
| **Krea AI** | Diagrams | [krea.ai](https://krea.ai) |

---

## Application Features (6 Tabs)

| Tab | Function |
|-----|----------|
| **Sources** | Load local folders, GitHub repos, Google Drive for context |
| **Prior Art Search** | Search USPTO PatentsView API (12M+ patents) |
| **Find Opportunities** | AI identifies patentable white space |
| **Draft Patent** | Generate complete provisional applications |
| **Dashboard** | Visualize patent landscape |
| **Research Videos** | YouTube transcript extraction |

---

## Project Structure

```
provisional-patent-skills/
├── patent-opportunity-finder/      # MAIN APP
│   ├── app.py                      # Streamlit UI
│   ├── config.example.py           # API key template
│   ├── requirements.txt
│   └── modules/
│       ├── prior_art_search.py     # USPTO API
│       ├── ai_providers.py         # Claude/OpenAI/Perplexity
│       ├── opportunity_finder.py   # White space analysis
│       ├── patent_drafter.py       # Patent generation
│       └── source_integrations.py  # GitHub/local/GDrive
│
├── RAG/                            # KNOWLEDGE BASES
│   ├── invention-analyzing/KNOWLEDGE_BASE.md
│   ├── prior-art-researching/KNOWLEDGE_BASE.md
│   ├── patent-comparing/KNOWLEDGE_BASE.md
│   ├── patentability-scoring/
│   │   ├── KNOWLEDGE_BASE.md
│   │   └── AI_SOFTWARE_PROVISIONAL_PATENT_RUBRIC.json
│   ├── provisional-patent-drafting/KNOWLEDGE_BASE.md
│   ├── white-space-finder/KNOWLEDGE_BASE.md
│   ├── patent-diagram-creating/KNOWLEDGE_BASE.md
│   └── expert-transcripts/
│       ├── all_transcripts_consolidated.json (15 videos)
│       └── EXPERT_INSIGHTS_EXTRACTED.md
│
└── AI_SOFTWARE_PROVISIONAL_PATENT_RUBRIC.json  # 100-point scoring
```

---

## RAG Knowledge Bases

Built from 15 expert YouTube videos (~73,000 words):
- Steve Key (inventRight) - Transaction-ready provisionals
- Dylan Adams (Patents Demystified) - Software patent strategy
- Patent attorneys - AI/ML patent drafting

### 100-Point Scoring Rubric

| Category | Points |
|----------|--------|
| Technical Disclosure | 30 |
| Drawings & Figures | 20 |
| Novelty & Differentiation | 15 |
| Scope & Protection | 15 |
| Implementation Details | 10 |
| AI-Specific Requirements | 10 |
| **Total** | **100** |

Target: **90+ (Top 5%)**

---

## Environment Variables

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-proj-..."
export PERPLEXITY_API_KEY="pplx-..."
export KREA_API_KEY="..."
export GITHUB_TOKEN="ghp_..."  # Optional: private repos
```

---

## License

Proprietary - IGTA Tech
