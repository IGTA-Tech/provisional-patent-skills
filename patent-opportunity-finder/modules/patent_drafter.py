"""
Patent Drafter Module
=====================
Generate complete provisional patent application drafts.
"""

import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from .ai_providers import AIOrchestrator, AIResponse
from .opportunity_finder import PatentOpportunity


@dataclass
class PatentSection:
    """A section of the patent application"""
    name: str
    content: str
    word_count: int


@dataclass
class ProvisionalPatent:
    """Complete provisional patent application"""
    title: str
    field: str
    background: str
    summary: str
    brief_description_drawings: str
    detailed_description: str
    claims: List[str]
    abstract: str
    figures: List[Dict]  # ASCII placeholders or image references
    metadata: Dict


class PatentDrafter:
    """
    Generates complete provisional patent application drafts
    Based on 95th percentile quality rubric
    """

    # Load RAG knowledge for drafting guidance
    RAG_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "RAG", "provisional-patent-drafting", "KNOWLEDGE_BASE.md"
    )

    SYSTEM_PROMPT = """You are an expert patent drafter specializing in AI and software patents.

CRITICAL REQUIREMENTS:
1. Focus on HOW the invention works, not just WHAT it does
2. Include specific hardware context (CPU, memory, storage)
3. Describe method steps in detail with data flows
4. Include multiple embodiments and variations
5. Write in plain engineering language, not legal jargon
6. Reference figure numbers (FIG. 1, FIG. 2, etc.)
7. Use reference numerals (101, 102, 103) for components

STRUCTURE:
- Background: Brief (under 200 words), don't cite specific prior art
- Summary: High-level solution with embodiments
- Detailed Description: 95% of effort here, very comprehensive
- Claims: Method claim, system claim, CRM claim

AVOID:
- Marketing language
- Absolute statements (always, never, must)
- Vague "uses AI/ML" without specifics
- Pure functional claims without implementation
"""

    def __init__(self, ai_orchestrator: AIOrchestrator = None):
        self.ai = ai_orchestrator
        self._load_rag_knowledge()

    def _load_rag_knowledge(self):
        """Load RAG knowledge base if available"""
        self.rag_knowledge = ""
        try:
            if os.path.exists(self.RAG_PATH):
                with open(self.RAG_PATH, 'r') as f:
                    self.rag_knowledge = f.read()
        except:
            pass

    def draft_from_opportunity(
        self,
        opportunity: PatentOpportunity,
        invention_details: str = ""
    ) -> ProvisionalPatent:
        """
        Draft a provisional patent from an identified opportunity

        Args:
            opportunity: Patent opportunity to develop
            invention_details: Additional technical details about the invention
        """
        # Generate each section
        title = self._generate_title(opportunity)
        field = self._generate_field(opportunity)
        background = self._generate_background(opportunity)
        summary = self._generate_summary(opportunity, invention_details)
        figures = self._generate_figure_descriptions(opportunity)
        detailed = self._generate_detailed_description(opportunity, invention_details, figures)
        claims = self._generate_claims(opportunity, invention_details)
        abstract = self._generate_abstract(opportunity, invention_details)

        return ProvisionalPatent(
            title=title,
            field=field,
            background=background,
            summary=summary,
            brief_description_drawings=self._format_figure_brief(figures),
            detailed_description=detailed,
            claims=claims,
            abstract=abstract,
            figures=figures,
            metadata={
                "generated_date": datetime.now().isoformat(),
                "opportunity_type": opportunity.opportunity_type,
                "related_patents": opportunity.related_patents,
                "patentability_score": opportunity.patentability_score
            }
        )

    def draft_from_description(
        self,
        invention_title: str,
        invention_description: str,
        technical_field: str = "artificial intelligence"
    ) -> ProvisionalPatent:
        """
        Draft a provisional patent from a free-form invention description

        Args:
            invention_title: Title for the invention
            invention_description: Detailed description of the invention
            technical_field: The technical field
        """
        if not self.ai or not self.ai.get_available_providers():
            return self._generate_template_patent(invention_title, invention_description, technical_field)

        # Use AI to generate comprehensive draft
        prompt = f"""Generate a complete provisional patent application for:

TITLE: {invention_title}
FIELD: {technical_field}

INVENTION DESCRIPTION:
{invention_description}

Generate ALL sections with full detail:
1. Background (under 200 words)
2. Summary of Invention
3. Brief Description of Drawings (for 5 figures)
4. Detailed Description (comprehensive, 2000+ words)
5. Claims (1 method, 1 system, 1 CRM, plus dependents)
6. Abstract (150 words max)

Remember: Focus on HOW it works with specific technical details."""

        response = self.ai.generate(
            prompt,
            system_prompt=self.SYSTEM_PROMPT,
            max_tokens=8000
        )

        if response.success:
            return self._parse_ai_response(response.content, invention_title, technical_field)
        else:
            return self._generate_template_patent(invention_title, invention_description, technical_field)

    def _generate_title(self, opportunity: PatentOpportunity) -> str:
        """Generate descriptive technical title"""
        # Clean up opportunity title
        base = opportunity.title.replace("Improvement on:", "").replace("Enhancement to:", "").strip()
        if len(base) < 20:
            base = f"System and Method for {base}"
        return base[:100]

    def _generate_field(self, opportunity: PatentOpportunity) -> str:
        """Generate field of invention"""
        return """The present invention relates generally to artificial intelligence and machine learning systems, and more particularly to methods and systems for improved computational processing. Aspects of the invention relate to neural network architectures and optimization techniques."""

    def _generate_background(self, opportunity: PatentOpportunity) -> str:
        """Generate brief background section"""
        return f"""Conventional approaches in this field face limitations including computational overhead, accuracy constraints, and scalability challenges. Existing systems often require significant resources while providing suboptimal results.

There is a need for improved methods and systems that address these limitations while providing enhanced performance and efficiency.

{opportunity.description[:200]}"""

    def _generate_summary(self, opportunity: PatentOpportunity, details: str) -> str:
        """Generate invention summary"""
        return f"""The present invention provides improved methods and systems for addressing the limitations of conventional approaches.

In one embodiment, a method comprises:
receiving input data from one or more sources;
processing the input data using a novel computational approach;
generating enhanced output based on the processing; and
providing the output for use by downstream systems.

In another embodiment, a system comprises:
a processor configured to execute instructions;
a memory storing the instructions; and
one or more modules implementing the novel approach.

The invention provides advantages including improved accuracy, reduced computational requirements, and enhanced scalability.

{opportunity.technical_approach}"""

    def _generate_figure_descriptions(self, opportunity: PatentOpportunity) -> List[Dict]:
        """Generate figure placeholders and descriptions"""
        return [
            {
                "number": 1,
                "title": "System Architecture",
                "description": "FIG. 1 illustrates a system 100 according to various embodiments.",
                "type": "system_diagram"
            },
            {
                "number": 2,
                "title": "Hardware Block Diagram",
                "description": "FIG. 2 illustrates a computing device 200 according to various embodiments.",
                "type": "block_diagram"
            },
            {
                "number": 3,
                "title": "Method Flowchart",
                "description": "FIG. 3 is a flowchart illustrating a method 300 according to various embodiments.",
                "type": "flowchart"
            },
            {
                "number": 4,
                "title": "Data Flow Diagram",
                "description": "FIG. 4 illustrates data processing flow 400 according to various embodiments.",
                "type": "data_flow"
            },
            {
                "number": 5,
                "title": "Alternative Embodiment",
                "description": "FIG. 5 illustrates an alternative implementation 500 according to various embodiments.",
                "type": "system_diagram"
            }
        ]

    def _format_figure_brief(self, figures: List[Dict]) -> str:
        """Format brief description of drawings"""
        lines = ["The following drawings illustrate various embodiments of the invention:\n"]
        for fig in figures:
            lines.append(fig["description"])
        return "\n\n".join(lines)

    def _generate_detailed_description(
        self,
        opportunity: PatentOpportunity,
        details: str,
        figures: List[Dict]
    ) -> str:
        """Generate comprehensive detailed description"""

        sections = []

        # Overview
        sections.append("""## Detailed Description

### Overview

The following detailed description provides specific embodiments of the invention. It should be understood that numerous variations and modifications can be made without departing from the scope of the invention. The described embodiments are illustrative only and are not intended to limit the scope of the claims.
""")

        # System Architecture (FIG. 1)
        sections.append("""### System Architecture (Reference to FIG. 1)

Referring now to FIG. 1, a system 100 for implementing the invention is illustrated. The system 100 includes a client device 101, a network interface 102, an application server 104, a processing engine 106, and a data store 108.

The client device 101 may comprise any computing device capable of network communication, including but not limited to smartphones, tablets, desktop computers, laptop computers, and IoT devices. The client device 101 is configured to transmit requests and receive responses via the network interface 102.

The network interface 102 facilitates communication between the client device 101 and the application server 104. The network interface 102 may utilize various protocols including HTTP, HTTPS, WebSocket, or proprietary protocols. In various embodiments, the communication is encrypted using TLS 1.3 or similar security protocols.

The application server 104 receives requests from client devices and coordinates processing operations. The application server 104 may be implemented as one or more physical servers, virtual machines, containerized applications, or serverless functions. In some embodiments, the application server 104 implements load balancing across multiple processing nodes.

The processing engine 106 implements the core innovation of the present invention. The processing engine 106 receives data from the application server 104, performs computational operations, and returns results. In various embodiments, the processing engine 106 comprises specialized hardware such as GPUs, TPUs, or custom ASICs optimized for the specific computational requirements.

The data store 108 provides persistent storage for the system 100. The data store 108 may comprise relational databases, NoSQL databases, object storage, or combinations thereof. In various embodiments, the data store 108 implements caching layers for improved performance.
""")

        # Hardware (FIG. 2)
        sections.append("""### Hardware Implementation (Reference to FIG. 2)

Referring to FIG. 2, a computing device 200 suitable for implementing aspects of the invention is shown. The computing device 200 includes a processor 202, memory 204, storage 206, network interface 208, and bus 210.

The processor 202 may comprise one or more central processing units (CPUs), graphics processing units (GPUs), tensor processing units (TPUs), or other processing circuitry. In various embodiments, the processor 202 includes multiple cores configured for parallel processing. The processor 202 executes instructions stored in memory 204 to perform the methods described herein.

The memory 204 comprises volatile memory such as DRAM or SRAM. The memory 204 stores instructions and data for active processing. In various embodiments, the memory 204 comprises 16GB to 512GB or more depending on application requirements.

The storage 206 comprises non-volatile storage such as solid-state drives (SSDs), hard disk drives (HDDs), or non-volatile memory (NVMe). The storage 206 stores the operating system, application code, and persistent data.

The network interface 208 enables communication with external systems. The network interface 208 may support Ethernet, WiFi, cellular, or other communication standards. In various embodiments, the network interface 208 supports speeds of 1Gbps to 100Gbps or higher.

The bus 210 interconnects the components of computing device 200. The bus 210 may comprise PCIe, NVLink, or other high-speed interconnects suitable for the processing requirements.
""")

        # Method (FIG. 3)
        sections.append(f"""### Method of Operation (Reference to FIG. 3)

Referring to FIG. 3, a method 300 for implementing the invention is illustrated. The method 300 may be performed by the system 100 of FIG. 1 or the computing device 200 of FIG. 2.

At step 302, input data is received. The input data may comprise structured data, unstructured data, or combinations thereof. In various embodiments, the input data is received via API calls, file uploads, streaming interfaces, or direct database connections. The input data is validated for format and content before processing.

At step 304, the input data is preprocessed. Preprocessing includes normalization, feature extraction, and transformation operations. In various embodiments, preprocessing includes tokenization, embedding generation, or numerical scaling depending on the data type. The preprocessing step produces a standardized representation suitable for downstream processing.

At step 306, the preprocessed data is processed using the novel technique of the present invention. {opportunity.technical_approach}

At decision block 308, the processing results are evaluated. If the results meet quality thresholds, the method proceeds to step 310. Otherwise, the method may return to step 306 with adjusted parameters or proceed to error handling at step 312.

At step 310, the output is generated and formatted. The output is prepared for transmission to requesting systems. In various embodiments, the output includes confidence scores, metadata, and explanatory information.

At step 314, the output is transmitted to the requesting client. The transmission may use synchronous or asynchronous patterns depending on the use case. The method 300 then ends at step 316.
""")

        # Data Flow (FIG. 4)
        sections.append("""### Data Processing (Reference to FIG. 4)

Referring to FIG. 4, data flow 400 through the system is illustrated.

Raw input data 402 is received from external sources. The raw data 402 may include various formats and encodings. The raw data 402 is passed to the preprocessing module 404.

The preprocessing module 404 transforms raw data 402 into processed data 406. The preprocessing includes:
- Format normalization to standard representations
- Missing value handling and imputation
- Feature extraction and engineering
- Dimensionality reduction where appropriate

The processed data 406 is passed to the core processing module 408. The core processing module 408 implements the novel techniques of the present invention to generate intermediate results 410.

The intermediate results 410 are refined by the post-processing module 412 to produce final output 414. Post-processing includes:
- Confidence scoring and thresholding
- Output formatting and serialization
- Quality validation and verification
""")

        # Variations
        sections.append(f"""### Alternative Embodiments and Variations

The invention contemplates various modifications and alternative implementations.

**Alternative 1 - Distributed Processing:** In some embodiments, the processing is distributed across multiple computing nodes. A load balancer distributes incoming requests, and results are aggregated from multiple processors. This embodiment provides improved scalability and fault tolerance.

**Alternative 2 - Edge Deployment:** In some embodiments, the processing is performed on edge devices close to data sources. This reduces latency and bandwidth requirements. The edge devices may have limited resources, and the algorithms are optimized accordingly.

**Alternative 3 - Hybrid Architecture:** In some embodiments, initial processing is performed on edge devices, with complex operations offloaded to cloud infrastructure. This provides a balance of latency, capability, and cost.

**Variation A:** The processing may use different algorithm variants depending on input characteristics. For example, time-sensitive data may use streaming algorithms while batch data uses more thorough analysis.

**Variation B:** The system may be configured with different quality/speed tradeoffs. Higher quality settings use more computational resources but provide better results. Lower quality settings prioritize speed for time-critical applications.

{opportunity.risks[0] if opportunity.risks else ''}
""")

        return "\n".join(sections)

    def _generate_claims(self, opportunity: PatentOpportunity, details: str) -> List[str]:
        """Generate patent claims"""
        return [
            # Independent method claim
            """1. A method performed by a computing device, the method comprising:
   receiving, by a processor of the computing device, input data from one or more data sources;
   preprocessing, by the processor, the input data to generate processed data;
   applying, by the processor, a computational technique to the processed data to generate intermediate results;
   refining, by the processor, the intermediate results to generate output data; and
   transmitting, by the processor via a network interface, the output data to a requesting system.""",

            # Dependent claims
            """2. The method of claim 1, wherein the input data comprises structured data, unstructured data, or combinations thereof.""",

            """3. The method of claim 1, wherein preprocessing comprises normalization, feature extraction, and dimensionality reduction.""",

            """4. The method of claim 1, wherein the computational technique comprises machine learning inference using a trained model.""",

            """5. The method of claim 4, wherein the trained model comprises a neural network architecture.""",

            # Independent system claim
            """6. A system comprising:
   a processor;
   a memory storing instructions that, when executed by the processor, cause the system to perform operations comprising:
      receiving input data via a network interface;
      processing the input data using a computational engine to generate results;
      validating the results against quality thresholds; and
      transmitting the results to requesting clients.""",

            """7. The system of claim 6, wherein the processor comprises a graphics processing unit (GPU) optimized for parallel computation.""",

            """8. The system of claim 6, wherein the computational engine implements a trained machine learning model.""",

            # Independent CRM claim
            """9. A non-transitory computer-readable medium storing instructions that, when executed by a processor, cause the processor to perform operations comprising:
   receiving data from one or more sources;
   applying a preprocessing pipeline to the data;
   processing the preprocessed data to generate output; and
   providing the output for downstream use.""",

            """10. The non-transitory computer-readable medium of claim 9, wherein the operations further comprise caching intermediate results for improved performance."""
        ]

    def _generate_abstract(self, opportunity: PatentOpportunity, details: str) -> str:
        """Generate abstract (max 150 words)"""
        return f"""A system and method for improved computational processing is disclosed. The system receives input data from various sources, preprocesses the data using normalization and feature extraction techniques, and applies novel computational methods to generate enhanced output. The system includes a processor, memory, and network interfaces configured to implement the disclosed methods. Various embodiments provide improved accuracy, reduced computational requirements, and enhanced scalability compared to conventional approaches. The system may be deployed in cloud, edge, or hybrid configurations depending on application requirements. {opportunity.title[:50]}"""[:700]

    def _generate_template_patent(
        self,
        title: str,
        description: str,
        field: str
    ) -> ProvisionalPatent:
        """Generate template-based patent without AI"""

        figures = self._generate_figure_descriptions(
            PatentOpportunity(
                title=title,
                description=description,
                opportunity_type="manual",
                related_patents=[],
                technical_approach=description,
                patentability_score=0,
                market_value="medium",
                difficulty="medium",
                priority_score=0,
                recommended_claims=[],
                risks=[]
            )
        )

        return ProvisionalPatent(
            title=title,
            field=f"The present invention relates to {field}.",
            background="[Background section to be completed with specific prior art context]",
            summary=f"The present invention provides: {description[:500]}",
            brief_description_drawings=self._format_figure_brief(figures),
            detailed_description="[Detailed description to be completed with full technical disclosure]",
            claims=["[Claims to be drafted based on novel aspects]"],
            abstract=description[:150],
            figures=figures,
            metadata={
                "generated_date": datetime.now().isoformat(),
                "template_based": True
            }
        )

    def _parse_ai_response(self, content: str, title: str, field: str) -> ProvisionalPatent:
        """Parse AI-generated content into structured patent"""
        # Simplified parsing - production would be more robust
        figures = self._generate_figure_descriptions(
            PatentOpportunity(
                title=title,
                description="",
                opportunity_type="ai_generated",
                related_patents=[],
                technical_approach="",
                patentability_score=0,
                market_value="medium",
                difficulty="medium",
                priority_score=0,
                recommended_claims=[],
                risks=[]
            )
        )

        return ProvisionalPatent(
            title=title,
            field=f"The present invention relates to {field}.",
            background=self._extract_section(content, "Background", "Summary"),
            summary=self._extract_section(content, "Summary", "Brief"),
            brief_description_drawings=self._format_figure_brief(figures),
            detailed_description=self._extract_section(content, "Detailed", "Claims"),
            claims=self._extract_claims(content),
            abstract=self._extract_section(content, "Abstract", None)[:700],
            figures=figures,
            metadata={
                "generated_date": datetime.now().isoformat(),
                "ai_generated": True
            }
        )

    def _extract_section(self, content: str, start: str, end: Optional[str]) -> str:
        """Extract section from AI response"""
        try:
            start_idx = content.lower().find(start.lower())
            if start_idx == -1:
                return ""
            if end:
                end_idx = content.lower().find(end.lower(), start_idx + len(start))
                if end_idx == -1:
                    return content[start_idx:]
                return content[start_idx:end_idx]
            return content[start_idx:]
        except:
            return ""

    def _extract_claims(self, content: str) -> List[str]:
        """Extract claims from AI response"""
        claims_section = self._extract_section(content, "Claims", "Abstract")
        if not claims_section:
            return ["[Claims to be drafted]"]

        # Split by claim numbers
        claims = []
        lines = claims_section.split('\n')
        current_claim = []

        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
                if current_claim:
                    claims.append('\n'.join(current_claim))
                current_claim = [line]
            elif current_claim:
                current_claim.append(line)

        if current_claim:
            claims.append('\n'.join(current_claim))

        return claims if claims else ["[Claims to be drafted]"]


def draft_patent(title: str, description: str, ai_keys: Dict = None) -> ProvisionalPatent:
    """
    Convenience function to draft a provisional patent

    Args:
        title: Invention title
        description: Technical description
        ai_keys: Dict with API keys

    Returns:
        ProvisionalPatent object
    """
    ai = None
    if ai_keys:
        ai = AIOrchestrator(**ai_keys)

    drafter = PatentDrafter(ai)
    return drafter.draft_from_description(title, description)


if __name__ == "__main__":
    print("Testing Patent Drafter...")

    patent = draft_patent(
        "Memory-Efficient Attention Mechanism",
        "A novel attention mechanism that reduces memory usage by 40% through sparse computation patterns."
    )

    print(f"\nTitle: {patent.title}")
    print(f"Abstract: {patent.abstract[:200]}...")
    print(f"Claims: {len(patent.claims)}")
    print(f"Figures: {len(patent.figures)}")
