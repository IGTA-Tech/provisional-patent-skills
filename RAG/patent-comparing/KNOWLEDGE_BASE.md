# Patent Comparing RAG Knowledge Base
## Deep Comparison Analysis Against USPTO Database

---

## Purpose

This skill performs detailed element-by-element comparison between an invention and specific patents from the USPTO database. It identifies exact overlaps, differentiation opportunities, and potential design-arounds.

---

## Comparison Methodology

### Step 1: Claim Deconstruction

Break down each patent claim into elements:

```markdown
## Claim 1 of US 10,000,000

Original Claim Text:
"A method for detecting fraud comprising:
receiving transaction data from a plurality of sources;
applying a neural network model to the transaction data;
generating a fraud probability score; and
transmitting an alert when the score exceeds a threshold."

### Deconstructed Elements:

| Element | Description | Type |
|---------|-------------|------|
| 1A | Receiving transaction data | Data input |
| 1B | From plurality of sources | Data scope |
| 1C | Applying neural network model | Processing method |
| 1D | Generating fraud probability score | Output generation |
| 1E | Transmitting alert | Action step |
| 1F | When score exceeds threshold | Condition |
```

### Step 2: Element Mapping

Map invention elements to claim elements:

```markdown
## Element Mapping: Invention vs US 10,000,000

| Claim Element | Invention Element | Match? | Notes |
|---------------|-------------------|--------|-------|
| 1A - Receiving transaction data | We receive transaction data | YES | Identical |
| 1B - From plurality of sources | We use single API | NO | Our invention differs |
| 1C - Neural network model | We use transformer | PARTIAL | Both are neural, but architecture differs |
| 1D - Fraud probability score | We output risk category | PARTIAL | Different output format |
| 1E - Transmitting alert | We log to database | NO | Different action |
| 1F - Score exceeds threshold | We use multi-class decision | NO | Different logic |

### Infringement Analysis:
- Would need ALL elements to literally infringe
- Elements 1B, 1E, 1F are different
- Low infringement risk for this claim
```

### Step 3: Design-Around Identification

```markdown
## Design-Around Opportunities

### Patent Limitation: "from plurality of sources"
**Our Approach:** Single unified API endpoint
**Why This Works:** Claim requires multiple sources; single source doesn't infringe

### Patent Limitation: "neural network model"
**Our Approach:** Transformer with custom attention
**Consideration:** Still a neural network; may need to distinguish architecture

### Patent Limitation: "transmitting alert"
**Our Approach:** Asynchronous logging
**Why This Works:** Logging is not transmitting alert
```

---

## Comparison Templates

### Template 1: Claim Chart

```markdown
# Claim Chart: [Our Invention] vs US [Patent Number]

## Patent Information
- **Number:** US [X]
- **Title:** [Title]
- **Assignee:** [Company]
- **Priority Date:** [Date]
- **Expiration:** [Date]

## Independent Claim 1

| Claim Language | Corresponding Feature in Our Invention | Analysis |
|----------------|---------------------------------------|----------|
| "A method comprising:" | Our method includes: | Preamble - typically non-limiting |
| "[Element A]" | [Our feature A] | [Match/Differ/Absent] |
| "[Element B]" | [Our feature B] | [Match/Differ/Absent] |
| "[Element C]" | [Our feature C] | [Match/Differ/Absent] |

## Conclusion
- **Literal Infringement:** [Yes/No/Possible]
- **Doctrine of Equivalents:** [Risk level]
- **Recommended Actions:** [Design around / License / Challenge]
```

### Template 2: Feature Comparison Matrix

```markdown
# Feature Comparison Matrix

| Feature | Our Invention | Patent A | Patent B | Patent C |
|---------|--------------|----------|----------|----------|
| Data Input | REST API | Multiple sources | Batch files | Streaming |
| Model Type | Transformer | CNN | RNN | Random Forest |
| Output | Categories | Score | Binary | Score |
| Speed | Real-time | Batch | Near-real-time | Batch |
| Accuracy | 95% | 90% | 88% | 85% |

## Differentiation Summary
- Our unique combination: [X + Y + Z]
- Not found in any prior patent: [Feature W]
```

### Template 3: Prior Art Invalidation Analysis

```markdown
# Invalidation Analysis for US [Patent Number]

## Target Claim: Claim 1

### Prior Art Reference 1: [Paper/Patent Title]
**Date:** [Publication Date]
**Elements Disclosed:**
- Element 1A: YES - See page 5, paragraph 2
- Element 1B: YES - See Figure 3
- Element 1C: NO - Uses different method
- Element 1D: YES - See claims section

### Prior Art Reference 2: [Paper/Patent Title]
**Date:** [Publication Date]
**Elements Disclosed:**
- Element 1C: YES - Describes exact method

### Combined Analysis
- Reference 1 + Reference 2 disclose ALL elements
- Motivation to combine: Both address fraud detection
- Potential 102/103 invalidity argument

## Recommendation
This patent may be vulnerable to invalidity challenge based on:
- [Reference 1] as primary reference
- [Reference 2] for teaching Element 1C
```

---

## API Integration

### Fetching Full Patent Claims

```python
import requests
import json

def get_patent_claims(patent_number):
    """
    Note: PatentsView doesn't include full claims.
    Use Google Patents or USPTO Full Text for claims.
    """

    # PatentsView for basic info
    base_url = "https://search.patentsview.org/api/v1/patent/"
    query = {"patent_number": patent_number}
    fields = [
        "patent_number",
        "patent_title",
        "patent_abstract",
        "patent_date",
        "assignees_at_grant.assignee_organization",
        "cpc_current.cpc_subgroup_id"
    ]

    params = {
        "q": json.dumps(query),
        "f": json.dumps(fields)
    }

    response = requests.get(base_url, params=params)
    return response.json()

# For full claims, use Google Patents URL:
# https://patents.google.com/patent/US{patent_number}
```

### Batch Comparison

```python
def compare_multiple_patents(invention_elements, patent_numbers):
    """
    Compare invention against multiple patents
    Returns comparison matrix
    """
    results = []

    for patent in patent_numbers:
        patent_info = get_patent_claims(patent)
        comparison = {
            'patent': patent,
            'overlap_score': 0,
            'blocking_elements': [],
            'design_around_opportunities': []
        }
        # Analysis logic here
        results.append(comparison)

    return results
```

---

## Comparison Criteria

### Literal Infringement Analysis

| Criterion | Test | Result |
|-----------|------|--------|
| All elements present? | Does invention include every claim element? | Must have ALL |
| Identical or equivalent? | Are elements functionally identical? | Either can infringe |
| Preamble limiting? | Does preamble add limitations? | Context-dependent |

### Doctrine of Equivalents

| Factor | Question |
|--------|----------|
| Function | Does it perform substantially same function? |
| Way | Does it work in substantially same way? |
| Result | Does it achieve substantially same result? |

If YES to all three, may infringe under DoE even if not literal.

### Obviousness Comparison

When comparing for obviousness rejection defense:

| KSR Rationale | Question to Answer |
|---------------|-------------------|
| Combining prior art | Why wouldn't skilled person combine these references? |
| Simple substitution | Is this a non-obvious substitution? |
| Known methods | Is applying this method to this problem non-obvious? |
| Predictable results | Were results unpredictable or surprising? |
| Obvious to try | Why isn't this an obvious choice among finite options? |
| Design incentives | What makes this combination non-routine? |
| Teaching away | Does prior art teach away from this combination? |

---

## Output: Comparison Report

```markdown
# Patent Comparison Report

## Executive Summary
- **Invention:** [Invention Title]
- **Patents Analyzed:** [Count]
- **Blocking Patents Found:** [Count]
- **Design-Around Opportunities:** [Count]
- **Overall Risk Level:** [Low/Medium/High]

## Detailed Comparisons

### US [Patent 1]
- Relevance: [High/Medium/Low]
- Overlap: [X of Y elements]
- Blocking: [Yes/No]
- Expiration: [Date]
[Detailed analysis]

### US [Patent 2]
[...]

## Recommendations

### Claim Strategy
1. Avoid claiming [Element X] - covered by [Patent]
2. Focus claims on [Novel Element Y]
3. Include dependent claims for [Specific Feature]

### Design-Around Options
1. [Modification 1] - Avoids [Patent] Claim [X]
2. [Modification 2] - Avoids [Patent] Claim [Y]

### Freedom to Operate
- [Green] Can proceed with [Features A, B, C]
- [Yellow] Caution with [Feature D] - similar to [Patent]
- [Red] Avoid [Feature E] - directly covered by [Patent]
```

---

## Expert Guidance

### From Patent Attorney
> "When you compare against prior art, you need to break down each claim element by element. A claim is only infringed if every single element is present. Missing even one element means no literal infringement."

### From Dylan Adams
> "The examiner is going to find a bunch of prior art, pull elements from each, and say it would be obvious to combine them. You need to know WHY your combination is non-obvious and not 'the next logical step.'"

### From Steve Key
> "Know your point of difference compared to everything else out there. If you do this correctly, you're going to overcome that patent examiner when he tries to reject your claims."

---

## Integration

After patent comparison:
1. **patentability-scoring** - Final score with comparison data
2. **provisional-patent-drafting** - Draft claims around prior art
3. **white-space-finder** - Identify unexplored areas
