# Patentability Scoring RAG Knowledge Base
## 100-Point Scoring System for AI/Software Provisional Patents

---

## Purpose

This skill scores provisional patent applications against a comprehensive rubric to determine if they meet the 95th percentile quality standard for AI/software inventions.

---

## Scoring Overview

| Score | Grade | Description |
|-------|-------|-------------|
| 95-100 | **Transaction Ready** | Ready for licensing/investment/filing |
| 85-94 | Excellent | Minor gaps to address |
| 75-84 | Good (Passing) | Solid foundation, needs work |
| 65-74 | Needs Improvement | Significant gaps |
| 50-64 | Insufficient | Unlikely to support strong claims |
| <50 | Worthless | Marketing fluff, no protection |

**Target: 90+ points (Top 5%)**

---

## Category 1: Technical Disclosure Quality (30 Points)

### 1.1 HOW not WHAT (8 points)

| Score | Criteria |
|-------|----------|
| 8 | Method steps, data flows, processing logic all clearly articulated |
| 6 | Most methods described, some vague areas |
| 4 | General description of function, limited HOW |
| 2 | Mostly describes outcomes/benefits, not implementation |
| 0 | Pure marketing language, no technical substance |

**Evaluation Questions:**
- Does it explain step-by-step how the system works?
- Are data flows and transformations described?
- Is the processing logic clear?
- Could a developer implement this?

### 1.2 Hardware Context (6 points)

| Score | Criteria |
|-------|----------|
| 6 | Processor, memory, storage, network all specified with alternatives |
| 4 | Basic hardware mentioned (CPU, memory) |
| 2 | Vague "computer" or "server" references |
| 0 | No hardware context, pure abstract software |

**Required Elements:**
- Processor type (CPU, GPU, TPU)
- Memory/storage components
- Network interfaces if applicable
- Generalized + specific examples

### 1.3 Algorithm Disclosure (8 points)

| Score | Criteria |
|-------|----------|
| 8 | Detailed algorithm steps, pseudocode, input/output specs |
| 6 | Algorithm described with most steps clear |
| 4 | General algorithm description, missing details |
| 2 | Vague "AI/ML processes data" language |
| 0 | No algorithm disclosure |

**For AI/ML Inventions Check:**
- [ ] Training methodology described (if novel)
- [ ] Model architecture detailed (if novel)
- [ ] Data preprocessing steps
- [ ] Inference process explained

### 1.4 Enablement (8 points)

| Score | Criteria |
|-------|----------|
| 8 | Developer could implement without questions |
| 6 | Most implementation details present |
| 4 | Would need significant clarification |
| 2 | Major gaps in implementation details |
| 0 | Could not implement from description |

**The Test:** Could you outsource development using ONLY this document?

---

## Category 2: Drawings & Figures (20 Points)

### 2.1 System Diagram (5 points)

| Score | Criteria |
|-------|----------|
| 5 | Complete system with all components, connections, data flow |
| 3 | Basic system diagram, some components missing |
| 1 | Minimal diagram or sketch |
| 0 | No system diagram |

### 2.2 Hardware Block Diagram (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Processor, memory, I/O, interconnections shown |
| 2 | Basic hardware diagram |
| 0 | No hardware diagram |

### 2.3 Method Flowcharts (6 points)

| Score | Criteria |
|-------|----------|
| 6 | Multiple flowcharts with decision points, clear steps, reference numbers |
| 4 | At least one complete flowchart |
| 2 | Basic flowchart, missing elements |
| 0 | No flowcharts |

### 2.4 Interface Mockups (3 points)

| Score | Criteria |
|-------|----------|
| 3 | UI mockups showing inputs, outputs, user interaction |
| 1 | Basic interface sketch |
| 0 | No interface diagrams (OK if not applicable) |

### 2.5 Data Flow Diagram (2 points)

| Score | Criteria |
|-------|----------|
| 2 | Data movement between components clearly shown |
| 1 | Basic data flow |
| 0 | No data flow diagram |

---

## Category 3: Novelty & Differentiation (15 Points)

### 3.1 Prior Art Awareness (5 points)

| Score | Criteria |
|-------|----------|
| 5 | Clear evidence of prior art research, differentiation documented |
| 3 | Some awareness of existing solutions |
| 1 | Generic "improvement over existing" claims |
| 0 | No prior art awareness shown |

### 3.2 Point of Difference (5 points)

| Score | Criteria |
|-------|----------|
| 5 | Explicit, specific differentiation from prior approaches |
| 3 | General differentiation stated |
| 1 | Vague claims of being "better" |
| 0 | No differentiation articulated |

### 3.3 Problem-Solution Framework (5 points)

| Score | Criteria |
|-------|----------|
| 5 | Technical problem clearly stated, solution addresses it directly |
| 3 | Problem identified, solution somewhat connected |
| 1 | Vague problem statement |
| 0 | No problem-solution framework |

---

## Category 4: Scope & Protection (15 Points)

### 4.1 Workarounds & Variations (8 points)

| Score | Criteria |
|-------|----------|
| 8 | Multiple alternative implementations, broad-to-narrow language |
| 6 | Several variations described |
| 4 | Some alternatives mentioned |
| 2 | Minimal variation coverage |
| 0 | Only one implementation described |

**Check for:**
- "In some embodiments..." variations
- Alternative components/methods
- Generalized language ("any closing mechanism")
- Design-around prevention

### 4.2 Future Variations (4 points)

| Score | Criteria |
|-------|----------|
| 4 | 2nd/3rd generation improvements described |
| 2 | Some future possibilities mentioned |
| 0 | Only current implementation |

### 4.3 Broad-to-Narrow (3 points)

| Score | Criteria |
|-------|----------|
| 3 | General concepts → specific examples → flexibility |
| 2 | Some breadth in description |
| 0 | Only specific implementation |

---

## Category 5: Implementation Details (10 Points)

### 5.1 Manufacturing/Deployment (5 points)

| Score | Criteria |
|-------|----------|
| 5 | Clear deployment architecture, tech stack, infrastructure |
| 3 | Some implementation details |
| 1 | Vague references to deployment |
| 0 | No implementation guidance |

### 5.2 Technology Stack (3 points)

| Score | Criteria |
|-------|----------|
| 3 | Languages, frameworks, databases, cloud services specified |
| 2 | Some technology mentioned |
| 0 | No technology details |

### 5.3 Real-World Use Case (2 points)

| Score | Criteria |
|-------|----------|
| 2 | Complete walkthrough of actual use |
| 1 | Basic use case described |
| 0 | No use case walkthrough |

---

## Category 6: AI-Specific Requirements (10 Points)

### 6.1 Practical Application (4 points)

| Score | Criteria |
|-------|----------|
| 4 | Tangible technical improvement clearly shown |
| 2 | Some practical application evident |
| 0 | Mere data processing, no clear improvement |

### 6.2 Not Abstract (3 points)

| Score | Criteria |
|-------|----------|
| 3 | Technical features emphasized, avoids abstract characterization |
| 2 | Mostly concrete, some abstract elements |
| 0 | Reads as abstract idea, mathematical formula |

### 6.3 Inventorship Documentation (3 points)

| Score | Criteria |
|-------|----------|
| 3 | Human contribution clear, AI tool usage documented |
| 2 | Inventorship evident but not documented |
| 0 | Unclear human contribution |

---

## Red Flags (Automatic Deductions)

| Red Flag | Deduction |
|----------|-----------|
| Marketing language instead of technical | -10 |
| Only describes WHAT, not HOW | -15 |
| No drawings or figures | -10 |
| Vague "uses AI/ML" without specifics | -8 |
| No hardware context for software | -10 |
| Inconsistent terminology | -5 |
| Missing reference numerals | -3 |

---

## Bonus Points (Max +10)

| Bonus | Points |
|-------|--------|
| Informal claims included | +3 |
| Multiple embodiments detailed (5+) | +3 |
| Competitive workaround analysis | +2 |
| Performance benchmarks included | +2 |

---

## Scoring Template

```markdown
# Provisional Patent Scoring Report

## Application: [Title]
## Date Scored: [Date]

### Category Scores

| Category | Score | Max | Notes |
|----------|-------|-----|-------|
| Technical Disclosure | XX | 30 | [notes] |
| Drawings & Figures | XX | 20 | [notes] |
| Novelty & Differentiation | XX | 15 | [notes] |
| Scope & Protection | XX | 15 | [notes] |
| Implementation Details | XX | 10 | [notes] |
| AI-Specific Requirements | XX | 10 | [notes] |
| **Subtotal** | **XX** | **100** | |
| Red Flag Deductions | -XX | | [list] |
| Bonus Points | +XX | +10 | [list] |
| **FINAL SCORE** | **XX** | | |

### Grade: [Grade]

### Summary
[2-3 sentence summary of strengths and weaknesses]

### Critical Improvements Needed
1. [Improvement 1]
2. [Improvement 2]
3. [Improvement 3]

### Strengths
1. [Strength 1]
2. [Strength 2]

### Recommendation
[Proceed / Revise / Major Rework]
```

---

## Quick Assessment (5-Minute Check)

Answer these questions:

1. **Can I understand HOW it works?** (Not just what it does)
2. **Are there at least 3 figures?** (System, hardware, method)
3. **Is software tied to hardware?** (CPU, memory, etc.)
4. **What's different from existing solutions?** (Clear answer?)
5. **Are alternatives described?** (Variations, workarounds)

If NO to any: Score likely below 75.
If YES to all: Score likely 80+.

---

## Expert Calibration

### Score 95+ (Transaction Ready)
> "When you put this all together, now you can tell a story. It's a great selling tool that overcomes arguments, makes it clear for people to understand." - Steve Key

### Score 75-84 (Passing but Needs Work)
> "Good provisionals have lots of description, but make sure it's the RIGHT details - how it works, not just what it is." - Patent Attorney

### Score <50 (Worthless)
> "I've seen people with one paragraph abstracts. Yes they're patent pending, but it's absolutely worthless and gives them no protection." - Dylan Adams
