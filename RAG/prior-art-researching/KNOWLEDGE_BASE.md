# Prior Art Researching RAG Knowledge Base
## Comprehensive Prior Art Search for AI/Software Inventions

---

## Purpose

This skill searches for existing patents, publications, and technical disclosures that may affect the novelty or obviousness of an invention. It uses multiple APIs and databases to build a comprehensive prior art landscape.

---

## APIs Available

### 1. PatentsView API (FREE - No Key Required)

**Base URL:** `https://search.patentsview.org/api/v1/patent/`

**Capabilities:**
- Search 12+ million US patents (1976-present)
- Full abstracts, titles, claims info
- Inventor and assignee information
- Citation counts
- CPC classification codes
- No rate limits for normal use

**Example Queries:**

```python
import requests
import json

# Search by keywords in abstract
query = {
    "_text_any": {
        "patent_abstract": "neural network fraud detection"
    }
}

fields = [
    "patent_number",
    "patent_title",
    "patent_abstract",
    "patent_date",
    "assignees_at_grant.assignee_organization",
    "citedby_patent_count"
]

params = {
    "q": json.dumps(query),
    "f": json.dumps(fields),
    "o": json.dumps({"size": 50})
}

response = requests.get(
    "https://search.patentsview.org/api/v1/patent/",
    params=params
)
```

**Search by CPC Code (Technology Classification):**

| CPC Code | Technology Area |
|----------|-----------------|
| G06F | Computer science, general |
| G06N | AI/Machine Learning |
| G06N3 | Neural networks |
| G06N5 | Knowledge processing |
| G06N20 | Machine learning general |
| H04L | Networking/Transmission |
| G06Q | Business methods |
| G06V | Image/Video analysis |

```python
# Search by CPC code + keywords
query = {
    "_and": [
        {"cpc_current.cpc_subgroup_id": {"_begins": "G06N"}},
        {"_text_any": {"patent_abstract": "transformer attention mechanism"}},
        {"_gte": {"patent_date": "2020-01-01"}}
    ]
}
```

### 2. Perplexity API (Requires Key)

**Use For:** Natural language prior art discovery beyond patents

```python
API_KEY = "pplx-your-key"
API_URL = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "sonar",
    "messages": [
        {
            "role": "user",
            "content": f"""Find prior art for this invention:

{invention_description}

Search for:
1. Related US patents with numbers
2. Academic papers (arxiv, conferences)
3. Technical blogs or publications
4. Open source implementations
5. Key differentiators the invention might need"""
        }
    ]
}
```

### 3. USPTO Bulk Data (FREE - Full Patent Text)

**Use For:** Getting complete patent documents including claims

```python
# Download weekly patent grants
grant_url = f"https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/{year}/"
```

---

## Search Strategy

### Phase 1: Keyword Search

1. **Extract Keywords from Invention**
   - Core technical terms
   - Method names
   - Algorithm names
   - Problem domain terms

2. **Expand Keywords**
   - Synonyms
   - Related terms
   - Industry jargon variations
   - Acronyms and full forms

3. **Build Search Queries**
   - Start broad, then narrow
   - Use Boolean operators
   - Combine keywords with CPC codes

### Phase 2: Classification Search

1. **Identify Relevant CPC Codes**
   ```python
   # Find CPC codes for "machine learning"
   query = {
       "_text_any": {
           "cpc_current.cpc_subgroup_title": "machine learning"
       }
   }
   ```

2. **Search Within Classification**
   - All patents in relevant class
   - Subclass refinement
   - Cross-class combinations

### Phase 3: Citation Analysis

1. **Forward Citations**
   - Who cited the most relevant prior art?
   - What improvements were made?

2. **Backward Citations**
   - What did relevant patents cite?
   - Trace the technology lineage

3. **Citation Mapping**
   ```python
   # Get patents cited by a reference
   query = {
       "patent_number": "10000000"
   }
   fields = [
       "cited_patents.patent_number",
       "cited_patents.patent_title"
   ]
   ```

### Phase 4: Assignee Analysis

1. **Competitor Patents**
   ```python
   query = {
       "assignees_at_grant.assignee_organization": {
           "_contains": "Google"
       }
   }
   ```

2. **Acquisition Targets**
   - Small companies with key patents
   - University research groups

---

## Prior Art Categories

### Patents

| Source | What to Find |
|--------|--------------|
| US Patents (PatentsView) | Granted patents, published applications |
| USPTO Public Search | Full text, file wrapper |
| Google Patents | Global patents, translations |
| Espacenet | European patents |

### Non-Patent Literature

| Source | What to Find |
|--------|--------------|
| arXiv | Pre-prints, ML papers |
| IEEE Xplore | Published conference papers |
| ACM Digital Library | Computer science papers |
| Google Scholar | Academic citations |
| GitHub | Open source implementations |
| Technical blogs | Industry implementations |
| Stack Overflow | Known solutions |

---

## Output Format: Prior Art Report

### Section 1: Executive Summary
- Number of relevant references found
- Key blocking references (if any)
- Recommended claim scope adjustments
- Overall freedom-to-operate assessment

### Section 2: Most Relevant Patents

For each patent:
```markdown
### US [Patent Number]
**Title:** [Title]
**Assignee:** [Company/Inventor]
**Date:** [Grant Date]
**Relevance:** [High/Medium/Low]

**Abstract:** [Abstract text]

**Relevant Claims:**
- Claim 1: [Summary]
- Claim 5: [Summary]

**Overlap with Invention:**
- [Overlapping element 1]
- [Overlapping element 2]

**Differentiation Opportunities:**
- [How invention differs]
- [Potential claim around]
```

### Section 3: Academic Literature

For each paper:
```markdown
### [Paper Title]
**Authors:** [Authors]
**Publication:** [Journal/Conference]
**Date:** [Publication Date]
**Link:** [URL]

**Relevance:** [Description of overlap]
**Key Teachings:** [What it discloses]
```

### Section 4: Analysis

```markdown
## Novelty Assessment

### Elements Found in Prior Art:
- [Element 1] - Found in [Reference]
- [Element 2] - Found in [Reference]

### Potentially Novel Elements:
- [Element 3] - Not found in search
- [Element 4] - Not found in search

### Obviousness Considerations:
- Combination of [Ref 1] and [Ref 2] could suggest [Feature]
- [Feature X] appears to be non-obvious because [reason]

## Recommended Claim Strategy

### Independent Claim Focus:
- Focus on [Novel Element 1] + [Novel Element 2]
- Avoid claiming [Common Element] alone

### Dependent Claim Opportunities:
- [Specific implementation detail 1]
- [Specific implementation detail 2]
```

---

## Search Quality Checklist

Before completing prior art search:

- [ ] Searched US patent database (PatentsView)
- [ ] Searched by keywords (multiple variations)
- [ ] Searched by CPC classification
- [ ] Analyzed citation networks
- [ ] Checked competitor portfolios
- [ ] Searched academic literature (arXiv, IEEE)
- [ ] Checked open source repositories
- [ ] Searched technical blogs
- [ ] Documented all references with dates
- [ ] Assessed relevance of each reference
- [ ] Identified blocking vs. design-around references
- [ ] Mapped claim elements to prior art

---

## Expert Guidance

### From Patent Drafting Best Practices
> "You must know your point of difference compared to everything else out there. You're going to overcome those arguments with investors, potential licensees, but really with that patent examiner."

### From Dylan Adams
> "The non-obviousness standard is: would it be obvious to one of ordinary skill in the art to come to your invention knowing about all the prior art that exists? The examiner will find pieces of your invention and say it would be obvious to combine them."

### From Steve Key
> "Do a Google image search, a Google shopping search, and look for prior patents. What you're really trying to do is look at the roadblocks out ahead because your product will hit those roadblocks if you don't know what's out there."

---

## Integration

After prior art research, proceed to:
1. **patent-comparing** - Deep dive on closest references
2. **patentability-scoring** - Score based on prior art landscape
3. **provisional-patent-drafting** - Draft with differentiation in mind
