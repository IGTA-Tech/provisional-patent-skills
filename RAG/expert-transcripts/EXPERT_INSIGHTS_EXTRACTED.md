# Expert Insights for AI/Software Provisional Patents
## Extracted from 15 Videos (365,000+ words analyzed)

---

## Source Summary

| Category | Videos | Characters | Key Experts |
|----------|--------|------------|-------------|
| Original Core Videos | 3 | 105K | Steve Key, Dylan Adams, Patent Attorney |
| Dylan Adams Additional | 3 | 83K | Dylan Adams (Patents Demystified) |
| Steve Key/inventRight | 4 | 30K | Steve Key (inventRight) |
| AI/Software Patent Specialists | 5 | 146K | Justia, Multiple Patent Attorneys |
| **TOTAL** | **15** | **365K** | **~73,000 words** |

---

## TOP 10 ACTIONABLE INSIGHTS: Patent Drafting Best Practices

### 1. Problem-Solution Storytelling
**Advice:** Clearly identify and explicitly state the core invention, problem solved, and technical improvement using a "problem-solution" storytelling approach.

**Why It Matters:** Post-Alice and post-Enfish, examiners and courts demand a defined improvement to overcome §101 rejections.

**How to Implement:** In the provisional, dedicate 1-2 paragraphs early in the spec to outline the technical problem (e.g., "AI model inefficiency") and your solution's measurable improvement (e.g., "30% faster inference via novel transformer optimization").

---

### 2. Concise Background Section
**Advice:** Include a concise 1-2 paragraph background section to provide context without admitting prior art.

**Why It Matters:** Sets the stage for examiners to understand novelty while avoiding traps.

**How to Implement:** Frame generically (e.g., "Conventional AI systems suffer from high latency in edge computing") then pivot to your improvement. Keep under 200 words, avoiding citations.

---

### 3. Measurable Technical Improvements
**Advice:** Tie the invention to specific, measurable technical improvements (performance gains, reduced complexity, resource efficiency).

**Why It Matters:** USPTO 2025 guidance emphasizes these for §101 eligibility in AI/software. Generic "apply it on a computer" claims fail.

**How to Implement:** Quantify in the spec (e.g., "reduces computational load by 40% via streamlined neural network pruning"). Link to claims and flowcharts.

---

### 4. Broad Initial Claims + Multiple Embodiments
**Advice:** Draft broad initial claims in provisionals while disclosing varied embodiments and technical implementations.

**Why It Matters:** US continuation practice allows refining post-Alice based on feedback. Narrow provisionals limit family expansion.

**How to Implement:** Include 5-10 broad independent claims plus dependent narrowing ones. Spec must enable 3+ embodiments for priority support.

---

### 5. Reverse-Engineer KSR Rationales
**Advice:** Use KSR rationales in reverse during drafting to ensure your combination is non-obvious.

**Why It Matters:** Prevents examiners using your own words for §103 rejections. Critical for software where "obvious-to-try" dominates.

**How to Implement:** For each embodiment, note why prior elements aren't combined routinely (e.g., "Unlike known CNNs, this integrates RL unexpectedly to achieve X").

---

### 6. Drawings First
**Advice:** Incorporate detailed drawings first (flowcharts, diagrams) with annotations to visualize AI/software structure.

**Why It Matters:** Clarifies complex inventions for non-software-savvy examiners. Anchors spec to concrete implementations.

**How to Implement:** Start provisional with 5-10 figures (AI pipeline flowchart showing novel data flow). Label elements precisely and reference in text.

---

### 7. Hardware-Software Integration
**Advice:** Emphasize hardware-software integration and avoid purely functional language. Detail specific AI techniques.

**Why It Matters:** USPTO memos and EPO require technical effects over abstract ideas. Vague "AI doing X" gets rejected.

**How to Implement:** Describe algorithms with pseudocode/flow (e.g., "Transformer layer modifies attention via custom mask"). Note hardware ties (e.g., "executed on GPU with optimized memory").

---

### 8. Strong Invention Disclosure First
**Advice:** Start with a strong invention disclosure capturing novelty, prior art awareness, technical problems, and use cases.

**Why It Matters:** Ensures spec focuses on patentable aspects. Poor disclosures lead to thin applications vulnerable to Alice/IPR.

**How to Implement:** Use inventor questionnaire (e.g., "What measurable edge over prior AI? Benchmarks?"). Build spec around it.

---

### 9. IPR-Proof with Enabling Details
**Advice:** Overload spec with enabling details, alternatives, and data while avoiding over-disclosure.

**Why It Matters:** Post-AIA, patents face PTAB scrutiny. Robust specs withstand challenges.

**How to Implement:** Provide 20+ embodiments, fallback claims, and performance data tables. Balance with "preferred" qualifiers.

---

### 10. AI Drafting Tools (With Review)
**Advice:** Leverage AI drafting tools for efficiency but review for security and customization.

**Why It Matters:** Handles volume/budgets efficiently. Boosts accuracy on trends like 2025 USPTO AI guidance.

**How to Implement:** Input disclosure into secure tool (ISO 27001-compliant). Generate claims/spec variants. Attorney-edit for voice, adding Alice-proof language.

---

## AI PATENT DRAFTING: 5 Techniques

1. **Generate first drafts from invention disclosures** - Upload technical papers to AI tools for initial draft conversion
2. **Claims-first approach** - Input core claims to AI to anchor specification and ensure consistency
3. **Drawings-first method** - Upload annotated diagrams for automatic text generation
4. **Iterate via AI feedback** - Draft claims, run AI prior art searches, refine scopes
5. **Collaborative version control** - Involve inventors for real-time edits with contribution tracking

---

## AI PATENT DRAFTING: 5 Critical Warnings

1. **AI hallucinations** - Outputs may include inaccuracies, mismatched references. ALWAYS human review.
2. **Confidentiality breaches** - Free AI versions may use inputs for training. Use paid APIs with contracts.
3. **Inventorship risks** - AI cannot be co-inventor. Limit AI to describing human-written claims.
4. **Over-reliance** - Do not let AI draft autonomously. It lacks strategic judgment.
5. **Lack of paper trail** - Use tools with audit logs to track human vs AI input.

---

## Claim Language Patterns That Work

| Pattern | Description | Example |
|---------|-------------|---------|
| Human-drafted anchor | Write claims manually first, AI generates supporting spec | Independent claim by human → AI expands description |
| Functional + technical effects | Frame claims highlighting technical novelty | "...wherein the neural network reduces latency by 40%" |
| Dependent claim sets | Generate dependents from independents with full discussion | Input 3 independents → AI generates 17 dependents |
| Jurisdiction-tuned phrasing | AI suggests claim structures based on prior art analysis | US vs EPO claim format optimization |

---

## Transaction-Ready Provisional Checklist (From Steve Key)

A "Transaction-Ready" provisional overcomes THREE future arguments:

### Argument 1: "Why should we pay you?" (Licensees/Investors)
- [ ] Clear prior art differentiation documented
- [ ] Point of difference explicitly stated
- [ ] Workarounds and variations covered

### Argument 2: "This is obvious" (Patent Examiner)
- [ ] Detailed technical disclosure (HOW not WHAT)
- [ ] Measurable improvements quantified
- [ ] Hardware context for software

### Argument 3: "We can design around this" (Copycats)
- [ ] Multiple embodiments described
- [ ] Alternative implementations covered
- [ ] Broad-to-narrow language progression

---

## Software Provisional Specifics (From Dylan Adams)

### Focus 95% of Effort on Detailed Description

**DO:**
- Write in plain engineer language (not patent attorney style)
- Describe HOW the system works (methods, data flows, processing)
- Include system diagrams, flowcharts, UI mockups
- Explain method steps that create functionality
- Describe all variations and alternatives

**DON'T:**
- Write marketing language
- Only describe WHAT it does (outcomes/benefits)
- Spend time on title, field of invention
- Agonize over perfect CAD drawings (sketches work)
- Write formal claims (optional in provisionals)

### The Implementation Test
> "Could you outsource development using ONLY this document as the specification?"

If a developer would need to ask questions, add more detail.

---

## 2025 USPTO AI Guidance Key Points

1. **Practical Application Required** - AI invention must show tangible technical improvement
2. **Not Mere Data Processing** - Must go beyond routine computation
3. **Hardware Integration** - Software must be tied to specific hardware context
4. **Inventorship Documentation** - Human contribution to AI-assisted inventions must be documented
5. **Avoid Abstract Ideas** - Focus on technical features, not mathematical algorithms

---

## Quick Reference: What Examiners Want to See

| Element | What They Want | How to Provide |
|---------|----------------|----------------|
| Technical Problem | Clear articulation | 1-2 paragraphs in background |
| Solution | Specific improvement | Quantified benefits (30% faster, 40% less memory) |
| Novelty | Point of difference | Comparison to prior approaches |
| Enablement | How to implement | Detailed method steps, pseudocode |
| Hardware Tie | Not abstract | CPU, memory, network components |
| Variations | Broad protection | Multiple embodiments, alternatives |

---

## Sources

### Original Videos (Already Captured)
- Steve Key: Transaction-Ready Provisionals
- Dylan Adams: Software Provisional Drafting
- Dylan Adams: Patent & Inventing Playbook

### Additional Dylan Adams
- Intro to Patents for Inventors/Startups
- How the Law Will Handle AI
- How to Keep Up With AI in 2025

### Steve Key/inventRight
- 4 additional videos on patent strategy and licensing

### AI/Software Patent Specialists
- Patent Drafting Best Practices: Latest Trends
- Generative AI in Patent Drafting (Justia Webinar)
- AI Patent Drafting Tips
- AI-Assisted Patent Drafting: How I Do It
- Essential AI Tools for Patent Attorneys 2024
