# Invention Analyzing RAG Knowledge Base
## Analyze Code Repositories to Identify Patentable AI/Software Innovations

---

## Purpose

This skill analyzes a code repository to identify patentable innovations in software and AI systems. It extracts novel methods, systems, and processes that could form the basis of provisional patent applications.

---

## Phase 1: Repository Scan

### What to Look For

1. **README Analysis**
   - Problem statement being solved
   - Unique approach or methodology
   - Performance claims or benchmarks
   - Technical architecture overview

2. **Code Structure Analysis**
   - Novel algorithms in core modules
   - Unique data processing pipelines
   - Custom ML model architectures
   - Innovative API designs

3. **Algorithm Identification**
   - Custom loss functions
   - Novel optimization techniques
   - Unique preprocessing methods
   - Innovative inference approaches

### Key Files to Examine

| File Pattern | What to Extract |
|--------------|-----------------|
| `model.py`, `network.py` | Neural network architectures, custom layers |
| `train.py`, `trainer.py` | Training methodologies, optimization tricks |
| `preprocess.py`, `data.py` | Data transformation pipelines |
| `inference.py`, `predict.py` | Inference optimizations, deployment methods |
| `utils.py`, `helpers.py` | Reusable novel utilities |
| `config.py`, `settings.py` | Configurable parameters that enable novelty |

---

## Phase 2: Innovation Extraction

### Identifying What's New vs Existing

**Questions to Answer:**
1. What problem does this solve that existing solutions don't?
2. How is the approach fundamentally different from prior art?
3. What technical advantages does this provide (speed, accuracy, efficiency)?
4. What would a competitor need to replicate this?

### Technical Advantage Categories

| Category | Examples | Patentability Signal |
|----------|----------|---------------------|
| **Performance** | 2x faster inference, 30% less memory | Strong - quantifiable improvement |
| **Accuracy** | 5% better precision, novel metric | Strong - measurable outcome |
| **Efficiency** | Fewer training steps, less data needed | Strong - resource optimization |
| **Architecture** | New layer type, novel attention mechanism | Very Strong - structural innovation |
| **Integration** | Unique combination of existing methods | Medium - depends on non-obviousness |
| **Application** | New use case for known technique | Weak - may face Alice issues |

### Innovation Extraction Template

```markdown
## Innovation Disclosure

### Problem Solved
[Describe the technical problem in 2-3 sentences]

### Prior Approaches
[What did existing solutions do? What were their limitations?]

### Technical Solution
[How does this code solve the problem differently?]

### Novel Aspects
1. [First novel element]
2. [Second novel element]
3. [Third novel element]

### Key Algorithms/Methods
- Algorithm 1: [Name and brief description]
- Algorithm 2: [Name and brief description]

### Technical Advantages
- [Advantage 1 with quantification if possible]
- [Advantage 2 with quantification if possible]

### Hardware Requirements
- [What hardware does this run on?]
- [Any specific GPU/TPU/CPU requirements?]
```

---

## Phase 3: Patentability Pre-Assessment

### Red Flags (Likely NOT Patentable)

1. **Pure Business Method**
   - "We use AI to match buyers and sellers"
   - No technical improvement, just applying AI to business

2. **Obvious Combination**
   - "We combined ResNet with BERT"
   - Unless the combination produces unexpected results

3. **Abstract Idea**
   - "We analyze data to find patterns"
   - No specific technical implementation

4. **Mathematical Formula Only**
   - "We use this equation to calculate X"
   - Needs hardware/software implementation context

### Green Flags (Likely Patentable)

1. **Novel Architecture**
   - "Custom attention mechanism that reduces memory by 40%"
   - Specific structural innovation with measurable benefit

2. **Technical Improvement**
   - "Training converges in 50% fewer epochs due to novel loss function"
   - Quantifiable improvement over prior methods

3. **New Method**
   - "Three-phase preprocessing pipeline that enables real-time inference"
   - Specific steps that achieve technical result

4. **Hardware-Software Integration**
   - "GPU kernel optimization for sparse matrix operations"
   - Tied to specific hardware implementation

---

## Output: Invention Disclosure Document

### Required Sections

1. **Title of Invention**
   - Descriptive, technical (not marketing)
   - Example: "Memory-Efficient Attention Mechanism for Large Language Models"

2. **Field of Invention**
   - Broad technical area
   - Example: "Machine learning, specifically transformer architectures"

3. **Background/Problem Statement**
   - What problem exists?
   - Why is current solution inadequate?
   - Keep brief (100-200 words)

4. **Summary of Invention**
   - High-level description of solution
   - Key differentiators from prior art

5. **Detailed Technical Description**
   - How the invention works (HOW, not just WHAT)
   - Specific algorithms, data flows, processing steps
   - Reference to code modules where implemented

6. **Advantages Over Prior Art**
   - Measurable improvements
   - Technical benefits

7. **Alternative Embodiments**
   - Other ways to implement the core idea
   - Variations and extensions

8. **Claims Preview**
   - What specific elements would be claimed?
   - Independent claim scope
   - Dependent claim details

---

## Code Analysis Prompts

### For README Analysis
```
Analyze this README and extract:
1. The core problem being solved
2. The unique technical approach
3. Any performance claims or benchmarks
4. Potential patentable innovations

README Content:
[paste README]
```

### For Code Analysis
```
Analyze this code module and identify:
1. Novel algorithms or methods
2. Custom implementations vs library calls
3. Performance optimizations
4. Unique data processing approaches

Code:
[paste code]
```

### For Architecture Analysis
```
Analyze this model architecture and identify:
1. Novel layer types or configurations
2. Unique attention mechanisms
3. Custom loss functions
4. Training innovations

Architecture Code:
[paste model code]
```

---

## Integration with Other Skills

After invention analysis, proceed to:
1. **prior-art-researching** - Validate novelty against existing patents
2. **patent-comparing** - Deep comparison with USPTO database
3. **patentability-scoring** - Score the invention against rubric

---

## Expert Guidance

### From Dylan Adams (Patent Attorney)
> "Ideas can totally be patentable... it's only things that are abstract ideas or just a formula without any details that can't be patented. Something that is maybe just sketches on paper can totally be patentable assuming those ideas can be filled in."

### From Steve Key (inventRight)
> "You need to know your point of difference... do a Google image search, Google shopping search, look for prior patents. What you're really trying to do is look at the roadblocks out ahead."

### From Software Patent Expert
> "Focus on HOW the system works, not just WHAT it does. This is the biggest mistake I see folks make. They say 'this thing is so much better and has this functionality' but that's kind of worthless. It's not about what the system does, it's about HOW it does that."
