# Provisional Patent Skills

A comprehensive Claude Skills toolkit for drafting 95th percentile quality AI/software provisional patent applications.

## Overview

This repository contains RAG (Retrieval-Augmented Generation) knowledge bases and tools for building Claude Skills that assist with:

- **Invention Analysis** - Analyze code repos to identify patentable innovations
- **Prior Art Research** - Search USPTO and academic databases for existing art
- **Patent Comparison** - Element-by-element comparison against prior art
- **Patent Diagram Creation** - Generate USPTO-compliant diagrams
- **Provisional Patent Drafting** - Draft complete applications
- **Patentability Scoring** - 100-point quality assessment rubric
- **White Space Finding** - Identify patent opportunities in expiring/gap areas

## Knowledge Base Stats

| Metric | Value |
|--------|-------|
| Expert Video Transcripts | 15 |
| Total Transcript Words | ~73,000 |
| RAG Knowledge Bases | 7 |
| API Integrations | 4 |
| Scoring Rubric Points | 100 |

## Directory Structure

```
provisional-patent-skills/
├── RAG/
│   ├── invention-analyzing/
│   │   └── KNOWLEDGE_BASE.md
│   ├── prior-art-researching/
│   │   └── KNOWLEDGE_BASE.md
│   ├── patent-comparing/
│   │   └── KNOWLEDGE_BASE.md
│   ├── patent-diagram-creating/
│   │   └── KNOWLEDGE_BASE.md
│   ├── provisional-patent-drafting/
│   │   └── KNOWLEDGE_BASE.md
│   ├── patentability-scoring/
│   │   ├── KNOWLEDGE_BASE.md
│   │   ├── AI_SOFTWARE_PROVISIONAL_PATENT_RUBRIC.json
│   │   └── RUBRIC_SUMMARY.md
│   ├── white-space-finder/
│   │   └── KNOWLEDGE_BASE.md
│   ├── api-documentation/
│   │   └── api_tools.py
│   └── expert-transcripts/
│       ├── all_transcripts_consolidated.json
│       └── EXPERT_INSIGHTS_EXTRACTED.md
├── skills/
│   ├── invention-analyzing/
│   ├── prior-art-researching/
│   ├── patent-comparing/
│   ├── patent-diagram-creating/
│   ├── provisional-patent-drafting/
│   ├── patentability-scoring/
│   └── white-space-finder/
├── api_tools.py
├── AI_SOFTWARE_PROVISIONAL_PATENT_RUBRIC.json
├── RUBRIC_SUMMARY.md
├── EXPERT_INSIGHTS_EXTRACTED.md
├── youtube_transcripts.json
└── all_transcripts_consolidated.json
```

## APIs Integrated

### Free (No Key Required)
- **PatentsView API** - Search 12M+ US patents (1976-present)
- **USPTO Bulk Data** - Download full patent XML files
- **USPTO Assignment API** - Patent ownership history

### Premium (Key Required)
- **Perplexity API** - AI-powered prior art research

## Expert Sources

Knowledge extracted from:
- Steve Key (inventRight) - Transaction-ready provisionals
- Dylan Adams (Patents Demystified) - Software patent strategy
- Patent attorneys - AI/ML patent drafting
- Justia Webinars - Generative AI in prosecution

## 95th Percentile Scoring Rubric

| Category | Points |
|----------|--------|
| Technical Disclosure Quality | 30 |
| Drawings & Figures | 20 |
| Novelty & Differentiation | 15 |
| Scope & Protection | 15 |
| Implementation Details | 10 |
| AI-Specific Requirements | 10 |
| **Total** | **100** |

**Target Score: 90+ (Top 5%)**

## Key Concepts

### Transaction-Ready Standard

A provisional patent application that overcomes three future arguments:

1. **Licensees/Investors**: "Why should we pay you?" → Clear differentiation
2. **Patent Examiner**: "This is obvious" → Detailed technical disclosure
3. **Copycats**: "We can design around" → Workarounds already covered

### Critical Success Factors

- Describe **HOW** it works, not just WHAT
- Include hardware context for software
- Multiple drawings (system, flowchart, data flow)
- Workarounds and variations ("steal from yourself")
- Quantifiable technical improvements

## Usage

Each RAG folder contains a `KNOWLEDGE_BASE.md` that can be used as context for Claude when performing that skill. The skills can be chained:

```
invention-analyzing → prior-art-researching → patent-comparing →
patentability-scoring → provisional-patent-drafting
```

## License

MIT
