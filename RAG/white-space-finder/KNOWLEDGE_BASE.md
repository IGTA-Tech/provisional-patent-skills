# White Space Finder RAG Knowledge Base
## Identify Patent Opportunities from Prior Art Analysis

---

## Purpose

This skill identifies "white space" - unexplored or under-protected areas in the patent landscape where new provisional applications could provide valuable protection. It finds expiring patents, gaps in existing coverage, and opportunities for improvement patents.

---

## White Space Categories

### 1. Expiring Patent Opportunities

Patents expire 20 years from filing date. High-citation expiring patents indicate valuable technology becoming public domain.

**Search Strategy:**
```python
from datetime import datetime, timedelta

# Find patents filed 18-20 years ago (expiring within 2 years)
filing_start = (datetime.now() - timedelta(days=365*20)).strftime("%Y-%m-%d")
filing_end = (datetime.now() - timedelta(days=365*18)).strftime("%Y-%m-%d")

query = {
    "_and": [
        {"_gte": {"application.filing_date": filing_start}},
        {"_lte": {"application.filing_date": filing_end}},
        {"_gte": {"citedby_patent_count": 15}},  # High-value indicator
        {"cpc_current.cpc_subgroup_id": {"_begins": "G06N"}}  # AI/ML
    ]
}
```

**Opportunity Types:**
| Type | Description | Action |
|------|-------------|--------|
| Direct Implementation | Core patent expiring, tech becomes free | Build product, file improvements |
| Improvement Patent | Base tech expires, improvements patentable | File improvement patents now |
| Combination Patent | Multiple expiring patents combinable | Novel combination application |

### 2. Gap Analysis in Patent Families

Find patents with narrow claims that leave gaps:

**Indicators of Gaps:**
- Few dependent claims (limited protection scope)
- No continuation applications
- Narrow independent claims
- Missing obvious variations

**Search for Narrow Patents:**
```python
# Find patents with few claims (indicator of gaps)
query = {
    "_and": [
        {"cpc_current.cpc_subgroup_id": {"_begins": "G06N"}},
        {"_gte": {"patent_date": "2020-01-01"}},
        {"_text_any": {"patent_abstract": "transformer attention"}}
    ]
}

# Then analyze claim counts and scope
```

### 3. Improvement Opportunities

Find patents that solve problems but have weaknesses:

**Weakness Categories:**
| Weakness | Opportunity |
|----------|-------------|
| Slow performance | Speed improvement patent |
| High resource usage | Efficiency improvement |
| Limited accuracy | Accuracy enhancement |
| Narrow application | Broader application patent |
| Complex implementation | Simplification patent |

### 4. Combination Opportunities

Find patents that could be combined for synergistic improvements:

```python
# Find highly-cited patents in same technology area
query = {
    "_and": [
        {"cpc_current.cpc_subgroup_id": {"_begins": "G06N3"}},
        {"_gte": {"citedby_patent_count": 20}},
        {"_gte": {"patent_date": "2018-01-01"}}
    ]
}

# Analyze for combination opportunities
```

---

## Analysis Framework

### Step 1: Technology Landscape Mapping

```markdown
## Technology: [AI Fraud Detection]

### Key Players
| Company | Patent Count | Focus Area |
|---------|-------------|------------|
| [Company A] | [XX] | [Focus] |
| [Company B] | [XX] | [Focus] |
| [Company C] | [XX] | [Focus] |

### Technology Clusters
1. [Cluster 1]: [XX] patents, [trend]
2. [Cluster 2]: [XX] patents, [trend]
3. [Cluster 3]: [XX] patents, [trend]

### Filing Trends
- Peak filing year: [Year]
- Recent trend: [Increasing/Decreasing]
- Hot areas: [List]
- Declining areas: [List]
```

### Step 2: Gap Identification

```markdown
## Identified Gaps

### Gap 1: [Description]
**Current State:** [What exists]
**Missing:** [What's not covered]
**Opportunity:** [Potential patent]
**Difficulty:** [Low/Medium/High]
**Value:** [Low/Medium/High]

### Gap 2: [Description]
[...]
```

### Step 3: Opportunity Ranking

| Opportunity | Technical Feasibility | Market Value | Competition | Priority |
|-------------|----------------------|--------------|-------------|----------|
| [Opp 1] | [1-5] | [1-5] | [Low/Med/High] | [Score] |
| [Opp 2] | [1-5] | [1-5] | [Low/Med/High] | [Score] |

**Priority Score = (Feasibility + Value) × Competition Factor**
- Low competition: 1.5x
- Medium competition: 1.0x
- High competition: 0.5x

---

## API-Based Discovery

### Finding Expiring High-Value Patents

```python
import requests
import json
from datetime import datetime, timedelta

def find_expiring_opportunities(technology_cpc="G06N", min_citations=10):
    """
    Find high-value patents expiring within 2 years
    """
    base_url = "https://search.patentsview.org/api/v1/patent/"

    # Calculate date range for patents filed 18-20 years ago
    filing_start = (datetime.now() - timedelta(days=365*20)).strftime("%Y-%m-%d")
    filing_end = (datetime.now() - timedelta(days=365*18)).strftime("%Y-%m-%d")

    query = {
        "_and": [
            {"_gte": {"application.filing_date": filing_start}},
            {"_lte": {"application.filing_date": filing_end}},
            {"_gte": {"citedby_patent_count": min_citations}},
            {"cpc_current.cpc_subgroup_id": {"_begins": technology_cpc}}
        ]
    }

    fields = [
        "patent_number",
        "patent_title",
        "patent_abstract",
        "application.filing_date",
        "citedby_patent_count",
        "assignees_at_grant.assignee_organization"
    ]

    params = {
        "q": json.dumps(query),
        "f": json.dumps(fields),
        "o": json.dumps({"size": 100}),
        "s": json.dumps([{"citedby_patent_count": "desc"}])
    }

    response = requests.get(base_url, params=params)
    return response.json()
```

### Finding Technology Gaps

```python
def find_technology_gaps(technology_keyword, recent_years=3):
    """
    Find areas with few recent patents (potential gaps)
    """
    base_url = "https://search.patentsview.org/api/v1/patent/"

    recent_date = (datetime.now() - timedelta(days=365*recent_years)).strftime("%Y-%m-%d")

    query = {
        "_and": [
            {"_text_any": {"patent_abstract": technology_keyword}},
            {"_gte": {"patent_date": recent_date}},
            {"cpc_current.cpc_subgroup_id": {"_begins": "G06N"}}
        ]
    }

    fields = [
        "patent_number",
        "patent_title",
        "cpc_current.cpc_subgroup_id",
        "cpc_current.cpc_subgroup_title"
    ]

    params = {
        "q": json.dumps(query),
        "f": json.dumps(fields),
        "o": json.dumps({"size": 200})
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Analyze CPC distribution to find underserved areas
    cpc_counts = {}
    for patent in data.get('patents', []):
        for cpc in patent.get('cpc_current', []):
            cpc_id = cpc['cpc_subgroup_id']
            cpc_counts[cpc_id] = cpc_counts.get(cpc_id, 0) + 1

    # Low counts = potential gaps
    return sorted(cpc_counts.items(), key=lambda x: x[1])
```

### Analyzing Competitor Portfolios

```python
def analyze_competitor(company_name):
    """
    Analyze a competitor's patent portfolio for gaps
    """
    base_url = "https://search.patentsview.org/api/v1/patent/"

    query = {
        "assignees_at_grant.assignee_organization": {
            "_contains": company_name
        }
    }

    fields = [
        "patent_number",
        "patent_title",
        "patent_date",
        "cpc_current.cpc_subgroup_id",
        "citedby_patent_count"
    ]

    params = {
        "q": json.dumps(query),
        "f": json.dumps(fields),
        "o": json.dumps({"size": 500})
    }

    response = requests.get(base_url, params=params)
    return response.json()
```

---

## Output: White Space Report

```markdown
# White Space Analysis Report

## Technology Area: [Area]
## Date: [Date]

## Executive Summary
- **Total Patents Analyzed:** [XX]
- **White Space Opportunities Found:** [XX]
- **High-Priority Opportunities:** [XX]
- **Recommended Immediate Action:** [Description]

## Expiring Patent Opportunities

### Opportunity 1: [Title]
**Patent:** US [Number]
**Expires:** [Date]
**Citations:** [Count] (indicates high value)
**Current Owner:** [Company]
**Technology:** [Description]

**Opportunity:** [What can be done when this expires]
**Recommended Action:** [Specific action]
**Priority:** [High/Medium/Low]

### Opportunity 2: [...]

## Technology Gaps

### Gap 1: [Area Name]
**Current Coverage:** [Description of existing patents]
**Gap Description:** [What's missing]
**Potential Patent:** [What could be filed]
**Technical Feasibility:** [Assessment]
**Market Value:** [Assessment]
**Recommendation:** [Action]

### Gap 2: [...]

## Improvement Opportunities

### Improvement 1: [Title]
**Base Patent:** US [Number] - [Title]
**Weakness:** [What could be improved]
**Proposed Improvement:** [Specific improvement]
**Technical Approach:** [How to implement]
**Patentability Assessment:** [Likelihood of grant]

### Improvement 2: [...]

## Combination Opportunities

### Combination 1: [Title]
**Patent A:** US [Number] - [Contribution]
**Patent B:** US [Number] - [Contribution]
**Novel Combination:** [What the combination achieves]
**Non-Obviousness Argument:** [Why not obvious to combine]

### Combination 2: [...]

## Priority Matrix

| # | Opportunity | Feasibility | Value | Competition | Priority |
|---|-------------|-------------|-------|-------------|----------|
| 1 | [Opp] | [1-5] | [1-5] | [L/M/H] | [Score] |
| 2 | [Opp] | [1-5] | [1-5] | [L/M/H] | [Score] |
| 3 | [Opp] | [1-5] | [1-5] | [L/M/H] | [Score] |

## Recommended Actions

### Immediate (30 Days)
1. [Action 1]
2. [Action 2]

### Short-Term (90 Days)
1. [Action 1]
2. [Action 2]

### Long-Term (1 Year)
1. [Action 1]
2. [Action 2]
```

---

## CPC Code Reference

| Code | Technology Area | White Space Potential |
|------|-----------------|----------------------|
| G06N3 | Neural Networks | Medium - crowded but specialized gaps |
| G06N5 | Knowledge Processing | High - less crowded |
| G06N7 | Probabilistic Models | High - emerging area |
| G06N20 | ML General | Low - very crowded |
| G06F18 | Pattern Recognition | Medium |
| G06V10 | Image Analysis | Medium |
| H04L41 | Network Management | High - AI applications |
| G06Q10 | Business Methods | High - but Alice risks |

---

## Expert Guidance

### From Patent Strategy Expert
> "The best way to identify white space is to map where the big players AREN'T filing. If Google has 100 patents in area A but only 2 in related area B, area B might be white space."

### From Patent Attorney
> "Expiring patents are gold mines. Find high-citation patents about to expire and file improvement patents that build on them. You get the benefit of the prior work plus your own improvement."

### Finding Real Opportunities
> "Look for patents with narrow claims - they leave room for design-arounds. Also look for areas where academic papers exist but patents don't - that's often white space."

---

## Integration

After finding white space:
1. **invention-analyzing** - Develop invention for opportunity
2. **prior-art-researching** - Validate the gap exists
3. **provisional-patent-drafting** - File on identified opportunity
