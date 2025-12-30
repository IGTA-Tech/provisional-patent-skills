---
description: Generate a complete 98% transaction-ready provisional patent application with .docx output
---

# Patent Drafting Skill

Generate complete provisional patent applications for AI/software inventions that score 90+ on the 100-point rubric.

## Usage

```
/draft-patent <source_path>
```

Where `<source_path>` is one of:
- **Local folder**: `C:/path/to/project`
- **GitHub repo**: `https://github.com/owner/repo`
- **Google Drive**: `https://drive.google.com/drive/folders/...`

## What This Skill Does

1. **Loads Source Context** - Scans and analyzes the codebase
2. **Identifies Innovations** - Finds patentable technical improvements
3. **Researches Prior Art** - Uses Perplexity to find related patents
4. **Drafts Patent Sections** - Creates all 9 required sections
5. **Generates Figures** - 5-10 diagrams and screenshots
6. **Creates .docx** - Complete document with embedded images
7. **Scores Quality** - Evaluates against 100-point rubric

## Output

Creates a folder with:
```
patent_output_YYYYMMDD_HHMMSS/
├── provisional_patent.docx      # Complete patent application
├── patent_figures/              # All generated figures
│   ├── FIG_1_System_Architecture.png
│   ├── FIG_2_Hardware_Block_Diagram.png
│   ├── FIG_3_Method_Flowchart.png
│   └── ...
└── score_report.json            # Quality evaluation
```

## Instructions for Claude

When this skill is invoked:

1. First, determine the source type from the path:
   - Contains `github.com` → GitHub repo
   - Contains `drive.google.com` → Google Drive
   - Otherwise → Local folder path

2. Run the unified patent pipeline:

```python
import sys
sys.path.insert(0, "C:/Users/IGTA/provisional-patent-skills/patent-opportunity-finder")

from modules.unified_pipeline import UnifiedPatentPipeline
from modules.config import (
    ANTHROPIC_API_KEY,
    OPENAI_API_KEY,
    PERPLEXITY_API_KEY,
    KREA_API_KEY
)

# Initialize pipeline
pipeline = UnifiedPatentPipeline(
    claude_key=ANTHROPIC_API_KEY,
    openai_key=OPENAI_API_KEY,
    perplexity_key=PERPLEXITY_API_KEY,
    krea_key=KREA_API_KEY
)

# Run the pipeline
result = pipeline.run(
    source_path="<USER_PROVIDED_PATH>",
    inventor_name="<ASK_USER>",
    inventor_address="<ASK_USER>",
    inventor_city="<ASK_USER>",
    inventor_state="<ASK_USER>",
    inventor_zip="<ASK_USER>",
    inventor_country="United States",
    entity_type="Micro Entity",  # or Small Entity, Large Entity
    technical_field="artificial intelligence"
)

# Report results
print(f"Patent generated: {result['docx_path']}")
print(f"Score: {result['score']}/100 - {result['grade']}")
```

3. Before running, ask the user for inventor information:
   - Inventor name
   - Address (street, city, state, zip)
   - Entity type (Micro/Small/Large Entity)
   - Technical field (default: artificial intelligence)

4. After completion, report:
   - Location of generated .docx file
   - Number of figures generated
   - Rubric score and grade
   - Any recommendations for improvement if score < 90

## Patent Sections Generated

1. **Cover Sheet** - Filing information
2. **Title of Invention** - Descriptive technical title
3. **Field of Invention** - Technical area
4. **Background** - Problem statement (<200 words)
5. **Summary** - Solution overview with embodiments
6. **Brief Description of Drawings** - Figure list
7. **Detailed Description** - Comprehensive technical disclosure (2000+ words)
8. **Claims** - Method, system, and CRM claims
9. **Abstract** - 150 words max

## Figure Generation

Uses Krea AI (NanoBanana Pro) for:
- FIG. 1: System Architecture Diagram
- FIG. 2: Hardware Block Diagram
- FIG. 3: Method Flowchart
- FIG. 4: Data Flow Diagram
- FIG. 5: Alternative Embodiment

Uses Playwright for:
- Code screenshots with syntax highlighting
- UI mockups (if applicable)

## Quality Target

**Target Score: 90+** (Transaction Ready)

Scoring breakdown:
- Technical Disclosure Quality: 30 points
- Drawings & Figures: 20 points
- Novelty & Differentiation: 15 points
- Scope & Protection: 15 points
- Implementation Details: 10 points
- AI-Specific Requirements: 10 points
- Bonus Points: up to +10

## Example

```
User: /draft-patent C:/Users/IGTA/my-ai-project

Claude: I'll generate a provisional patent application for your project.

First, let me gather some information:
- Inventor name?
- Address (street, city, state, zip)?
- Entity type? (Micro Entity, Small Entity, or Large Entity)

[After user provides info, runs pipeline]

Patent generated successfully!

Location: C:/Users/IGTA/patent_output_20251230_123456/provisional_patent.docx
Figures: 7 (5 diagrams + 2 code screenshots)
Score: 92/100 - Transaction Ready (95th Percentile)

The patent application is ready for review and USPTO filing.
```
