# Provisional Patent Drafting RAG Knowledge Base
## Draft 95th Percentile Quality AI/Software Provisional Patent Applications

---

## Purpose

This skill drafts complete provisional patent applications for AI/software inventions that meet the "Transaction-Ready" standard - applications ready for licensing, investment, and USPTO filing.

---

## Transaction-Ready Standard

A Transaction-Ready provisional overcomes THREE future arguments:

| Audience | Their Argument | How We Overcome |
|----------|---------------|-----------------|
| Licensees/Investors | "Why should we pay you?" | Clear prior art differentiation |
| Patent Examiner | "This is obvious" | Detailed technical disclosure |
| Copycats/Infringers | "We can design around" | Workarounds already covered |

---

## Document Structure

### 1. Cover Sheet (Required)

```markdown
PROVISIONAL PATENT APPLICATION

Title: [Descriptive Technical Title]

Inventor(s):
- [Name], [City], [State], [Country]
- [Name], [City], [State], [Country]

Correspondence Address:
[Address]

Filing Fee: $320 (small entity) / $160 (micro entity)
```

### 2. Title of Invention

**DO:**
- Descriptive and technical
- Indicate the field
- Avoid marketing language

**Examples:**
- GOOD: "Memory-Efficient Attention Mechanism for Transformer Neural Networks"
- GOOD: "Real-Time Fraud Detection System Using Ensemble Machine Learning"
- BAD: "Revolutionary AI That Changes Everything"
- BAD: "Smart Fraud Stopper 3000"

### 3. Field of Invention (Optional but Helpful)

```markdown
## Field of Invention

The present invention relates generally to [broad field], and more particularly to [specific subfield]. Aspects of the invention relate to [specific technical area].
```

**Example:**
```markdown
## Field of Invention

The present invention relates generally to machine learning systems, and more particularly to transformer-based neural network architectures. Aspects of the invention relate to memory optimization techniques for large language model inference.
```

### 4. Background (Keep Brief - Under 200 Words)

```markdown
## Background

[Problem paragraph - What technical problem exists?]

Conventional approaches to [problem] suffer from [limitation 1], [limitation 2], and [limitation 3]. For example, existing systems require [resource/time/accuracy issue].

[Gap paragraph - What's missing?]

What is needed is [solution direction] that addresses these limitations while providing [desired benefit].
```

**WARNINGS:**
- Do NOT cite specific patents or papers (becomes admitted prior art)
- Do NOT overstate problems (can be used against you)
- Keep generic and brief

### 5. Summary of Invention

```markdown
## Summary

The present invention provides [solution type] for [problem addressed].

In one embodiment, a method comprises:
[High-level step 1];
[High-level step 2]; and
[High-level step 3].

In another embodiment, a system comprises:
[Component 1] configured to [function];
[Component 2] configured to [function]; and
[Component 3] configured to [function].

Advantages of the present invention include [advantage 1], [advantage 2], and [advantage 3].
```

### 6. Brief Description of Drawings

```markdown
## Brief Description of Drawings

FIG. 1 illustrates a system architecture according to various embodiments.

FIG. 2 illustrates a hardware block diagram of a computing device according to various embodiments.

FIG. 3 is a flowchart illustrating a method for [process] according to various embodiments.

FIG. 4 is a flowchart illustrating a method for [another process] according to various embodiments.

FIG. 5 illustrates a data flow diagram according to various embodiments.

FIG. 6 illustrates a user interface according to various embodiments.
```

### 7. Detailed Description (95% OF YOUR EFFORT)

This is the most critical section. Write in plain engineering language.

```markdown
## Detailed Description

### Overview

The following detailed description provides specific embodiments of the invention. It should be understood that numerous variations and modifications can be made without departing from the scope of the invention.

### System Architecture (Reference to FIG. 1)

Referring now to FIG. 1, a system 100 for [purpose] is illustrated. The system 100 includes [component 101], [component 102], and [component 103].

[Component 101] comprises [detailed description of what it is and how it works]. In various embodiments, [component 101] may be implemented as [variation 1], [variation 2], or [variation 3].

[Continue for each component...]

### Hardware Implementation (Reference to FIG. 2)

Referring to FIG. 2, a computing device 200 suitable for implementing aspects of the invention is shown. The computing device 200 includes a processor 202, memory 204, storage 206, and network interface 208.

The processor 202 may be one or more of: a central processing unit (CPU), a graphics processing unit (GPU), a tensor processing unit (TPU), or other processing circuitry. In some embodiments, the processor 202 includes [specific features relevant to invention].

[Continue with hardware details...]

### Method of Operation (Reference to FIG. 3)

Referring to FIG. 3, a method 300 for [process name] is illustrated. The method 300 may be performed by [what performs it].

At step 302, [detailed description of first step]. In various embodiments, step 302 includes [sub-steps or variations]. The input data may include [data types and sources].

At step 304, [detailed description of second step]. This step transforms [input] into [output] by [specific technique]. In some embodiments, [alternative approach].

At decision block 306, [condition is evaluated]. If [condition is true], the method proceeds to step 308. Otherwise, the method proceeds to step 310.

[Continue for all steps...]

### Data Processing (Reference to FIG. 5)

Referring to FIG. 5, data flow 500 illustrates how data is processed through the system.

Raw input data 502 is received from [source]. The raw data may include [data types].

The raw data 502 is processed by preprocessing module 504 to produce cleaned data 506. Preprocessing includes [specific operations]:
- [Operation 1]: [description]
- [Operation 2]: [description]
- [Operation 3]: [description]

[Continue with data flow...]

### Machine Learning Model (For AI Inventions)

In various embodiments, the machine learning model includes [architecture type].

The model architecture comprises:
- Input layer: [description]
- Hidden layers: [description with specifics]
- Output layer: [description]

Training is performed using [training method] with [loss function]. The training process includes:
1. [Training step 1]
2. [Training step 2]
3. [Training step 3]

Inference is performed by [inference process]. Optimization techniques include [specific techniques].

### Alternative Embodiments

In alternative embodiments, [component/method] may be implemented differently:

**Alternative 1:** [Description of alternative approach]

**Alternative 2:** [Description of another approach]

**Alternative 3:** [Description of yet another approach]

These alternatives provide [benefits] while maintaining [core functionality].

### Workarounds and Variations

The invention contemplates various modifications:

**Variation A:** Instead of [original element], the system may use [alternative]. This variation provides [benefit].

**Variation B:** The [method step] may alternatively be performed by [different approach].

**Variation C:** Multiple [components] may be combined into [unified component], or a single [component] may be distributed across [multiple elements].

### Performance Characteristics

In various embodiments, the invention achieves:
- [Performance metric 1]: [value or range]
- [Performance metric 2]: [value or range]
- [Performance metric 3]: [value or range]

Compared to conventional approaches, the invention provides:
- [Improvement 1]: [quantification]
- [Improvement 2]: [quantification]
```

### 8. Claims (Optional but Recommended)

Even though not required for provisionals, claims help define scope:

```markdown
## Claims

What is claimed is:

1. A method for [purpose], comprising:
   receiving [input] from [source];
   processing the [input] using [technique] to generate [intermediate result];
   applying [specific operation] to the [intermediate result]; and
   outputting [result].

2. The method of claim 1, wherein [additional limitation].

3. The method of claim 1, wherein [another limitation].

4. The method of claim 1, further comprising [additional step].

5. A system comprising:
   a processor; and
   a memory storing instructions that, when executed by the processor, cause the system to perform operations comprising:
   [operation 1];
   [operation 2]; and
   [operation 3].

6. The system of claim 5, wherein [limitation].

7. A non-transitory computer-readable medium storing instructions that, when executed by a processor, cause the processor to perform operations comprising:
   [operation 1];
   [operation 2]; and
   [operation 3].
```

### 9. Abstract

```markdown
## Abstract

A [system/method/apparatus] for [purpose] is disclosed. The [invention] includes [key component 1], [key component 2], and [key component 3]. The [invention] receives [input], processes it using [technique], and generates [output]. Advantages include [advantage 1], [advantage 2], and [advantage 3]. Various embodiments provide [benefit] while maintaining [characteristic].
```

**Requirements:**
- 150 words maximum
- Single paragraph
- No claims language
- Describe technical features

---

## Writing Style Guide

### DO:
- Write in plain engineering language
- Use "comprising" (open-ended) not "consisting of" (closed)
- Use "in some embodiments" or "in various embodiments"
- Reference figure numbers: "Referring to FIG. 3..."
- Use reference numerals consistently: "processor 202"
- Describe HOW things work, not just WHAT they do
- Include quantifiable improvements when possible
- Describe alternatives and variations

### DON'T:
- Use marketing language ("revolutionary", "best", "unique")
- Write like a patent attorney (avoid legalese)
- Make absolute statements ("always", "never", "must")
- Criticize prior art directly
- Include time estimates or schedules
- Use trademarks without proper notation

---

## AI/Software Specific Requirements

### 1. Hardware Context (REQUIRED)

Always describe software in context of hardware:

```markdown
The method is performed by a computing device comprising a processor and memory. The processor may be a CPU, GPU, TPU, or specialized inference accelerator. The memory stores instructions that, when executed by the processor, cause the computing device to perform the method.
```

### 2. Avoid Abstract Idea Characterization

Instead of:
> "A method for analyzing data to detect fraud"

Write:
> "A method performed by a computing device, comprising: receiving transaction data via a network interface; extracting feature vectors from the transaction data using a trained neural network; comparing the feature vectors against stored fraud signatures in a database; and transmitting, via the network interface, an alert signal when a match is detected."

### 3. Technical Improvement Language

Include statements like:
```markdown
The present invention provides a technical improvement over conventional systems by [specific technical improvement]. This improvement results in [quantifiable benefit such as reduced latency, improved accuracy, decreased memory usage].
```

### 4. Model Architecture Details

For ML inventions:
```markdown
The neural network comprises:
- An input layer configured to receive [input type] having dimensions [dimensions];
- A first hidden layer comprising [N] neurons with [activation function] activation;
- An attention mechanism configured to [specific function];
- An output layer configured to produce [output type].

The attention mechanism includes [specific novel features that distinguish from prior art].
```

---

## Checklist Before Submission

### Must Have:
- [ ] Descriptive technical title
- [ ] Brief background (under 200 words)
- [ ] Summary with embodiments
- [ ] Brief description of drawings
- [ ] Detailed description (comprehensive)
- [ ] At least 3 figures (system, hardware, method)
- [ ] Hardware context for software
- [ ] HOW it works, not just WHAT
- [ ] Alternative embodiments
- [ ] Workarounds and variations
- [ ] Reference numerals consistent

### Should Have:
- [ ] Performance metrics/improvements
- [ ] Multiple method flowcharts
- [ ] Data flow diagram
- [ ] UI mockup if applicable
- [ ] Informal claims
- [ ] Abstract (150 words max)

### Avoid:
- [ ] Marketing language
- [ ] Absolute statements
- [ ] Direct prior art criticism
- [ ] Unexplained jargon
- [ ] Missing figure references
- [ ] Inconsistent terminology

---

## Expert Quotes

### Steve Key (inventRight)
> "Write it in such a way that anybody could read it and understand it. Describe the problem so anyone can understand it. Your solution - make it very clearly stated. Don't make it complicated."

### Dylan Adams (Patent Attorney)
> "The detailed description should really be a walkthrough of the drawing. Start with each drawing and go into great detail about what it shows, what the pieces are, how they're interconnected."

### Software Patent Expert
> "The true standard is it just needs to be such that one of ordinary skill in the art can make and use the invention based on your description. Write in language that you would understand or that a software developer would understand."

---

## Integration

This skill uses outputs from:
1. **invention-analyzing** - Invention disclosure as input
2. **prior-art-researching** - Differentiation points
3. **patent-diagram-creating** - Figures to reference
4. **patentability-scoring** - Validate quality before output
