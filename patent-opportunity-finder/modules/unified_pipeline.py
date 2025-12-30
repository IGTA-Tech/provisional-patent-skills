"""
Unified Patent Drafting Pipeline
================================
Complete source-to-docx pipeline for provisional patent generation.

7-Phase Pipeline:
1. Load Source Context (local/GitHub/GDrive)
2. Analyze for Patentable Innovations
3. Research Prior Art (Perplexity + PatentsView)
4. Draft Patent Sections (Claude)
5. Generate Figures (Krea AI + Playwright)
6. Create .docx with Embedded Images
7. Score Against Rubric (target 90+)
"""

import os
import sys
import json
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, asdict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from modules.source_integrations import SourceManager, SourceContext
    from modules.patent_drafter import PatentDrafter, ProvisionalPatent
    from modules.ai_providers import AIOrchestrator
    from modules.docx_generator import DocxPatentGenerator, PatentDocument, PatentFigure, InventorInfo
    from modules.rubric_scorer import RubricScorer, score_patent
except ImportError:
    # Fallback for direct execution
    from source_integrations import SourceManager, SourceContext
    from patent_drafter import PatentDrafter, ProvisionalPatent
    from ai_providers import AIOrchestrator
    from docx_generator import DocxPatentGenerator, PatentDocument, PatentFigure, InventorInfo
    from rubric_scorer import RubricScorer, score_patent


@dataclass
class PipelineResult:
    """Result from the unified pipeline"""
    success: bool
    docx_path: str
    figures_dir: str
    score_report_path: str
    score: int
    grade: str
    figure_count: int
    source_files: int
    innovations_found: int
    prior_art_references: int
    error: Optional[str] = None


class UnifiedPatentPipeline:
    """
    Unified pipeline from source input to complete .docx patent application.

    Usage:
        pipeline = UnifiedPatentPipeline(
            claude_key="sk-ant-...",
            perplexity_key="pplx-...",
            krea_key="..."
        )

        result = pipeline.run(
            source_path="C:/path/to/project",
            inventor_name="John Doe",
            ...
        )
    """

    def __init__(
        self,
        claude_key: str = None,
        openai_key: str = None,
        perplexity_key: str = None,
        krea_key: str = None,
        github_token: str = None,
        gdrive_credentials: str = None
    ):
        """
        Initialize the pipeline with API keys.

        Args:
            claude_key: Anthropic API key (primary AI)
            openai_key: OpenAI API key (fallback)
            perplexity_key: Perplexity API key (research)
            krea_key: Krea AI API key (diagrams)
            github_token: GitHub token for private repos
            gdrive_credentials: Google Drive credentials path
        """
        # Store keys
        self.claude_key = claude_key
        self.openai_key = openai_key
        self.perplexity_key = perplexity_key
        self.krea_key = krea_key

        # Initialize components
        self.ai = AIOrchestrator(claude_key, openai_key, perplexity_key, krea_key)
        self.source_manager = SourceManager()
        self.drafter = PatentDrafter(self.ai)
        self.docx_generator = DocxPatentGenerator()
        self.scorer = RubricScorer()

        # State tracking
        self.source_context: Optional[SourceContext] = None
        self.innovations: List[Dict] = []
        self.prior_art: Dict = {}
        self.patent: Optional[ProvisionalPatent] = None
        self.figures: List[PatentFigure] = []
        self.score_result = None

        # Phase callbacks for progress reporting
        self.phase_callback = None

    def set_phase_callback(self, callback):
        """Set callback for phase progress updates"""
        self.phase_callback = callback

    def _report_phase(self, phase: int, description: str, progress: float = 0):
        """Report phase progress"""
        if self.phase_callback:
            self.phase_callback(phase, description, progress)
        print(f"[Phase {phase}/7] {description}")

    def run(
        self,
        source_path: str,
        inventor_name: str = "Inventor Name",
        inventor_address: str = "123 Main St",
        inventor_city: str = "City",
        inventor_state: str = "ST",
        inventor_zip: str = "12345",
        inventor_country: str = "United States",
        entity_type: str = "Micro Entity",
        assignee: str = None,
        invention_title: str = None,
        technical_field: str = "artificial intelligence",
        output_dir: str = None
    ) -> PipelineResult:
        """
        Run the complete 7-phase pipeline.

        Args:
            source_path: Path to local folder, GitHub URL, or GDrive URL
            inventor_*: Inventor information for cover sheet
            entity_type: "Micro Entity", "Small Entity", or "Large Entity"
            assignee: Company/organization name (optional)
            invention_title: Override auto-detected title
            technical_field: Technical field for the invention
            output_dir: Directory for output files

        Returns:
            PipelineResult with paths and scores
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if output_dir is None:
            output_dir = os.path.join(os.getcwd(), f"patent_output_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)

        try:
            # =====================================================
            # PHASE 1: Load Source Context
            # =====================================================
            self._report_phase(1, "Loading source context...")

            self.source_context = self._load_source(source_path)
            if not self.source_context:
                return PipelineResult(
                    success=False,
                    docx_path="",
                    figures_dir="",
                    score_report_path="",
                    score=0,
                    grade="Failed",
                    figure_count=0,
                    source_files=0,
                    innovations_found=0,
                    prior_art_references=0,
                    error="Failed to load source context"
                )

            print(f"  Loaded {self.source_context.total_files} files from {self.source_context.source_type}")

            # =====================================================
            # PHASE 2: Analyze for Patentable Innovations
            # =====================================================
            self._report_phase(2, "Analyzing for patentable innovations...")

            self.innovations = self._analyze_innovations()
            print(f"  Found {len(self.innovations)} potential innovations")

            # =====================================================
            # PHASE 3: Research Prior Art
            # =====================================================
            self._report_phase(3, "Researching prior art (PatentsView + Perplexity)...")

            self.prior_art = self._research_prior_art()
            prior_art_count = len(self.prior_art.get('patents', []))
            print(f"  Found {prior_art_count} related patents")

            # =====================================================
            # PHASE 4: Draft Patent Sections
            # =====================================================
            self._report_phase(4, "Drafting patent sections (Claude AI)...")

            title = invention_title or self._generate_title()
            invention_desc = self._build_invention_description()

            self.patent = self.drafter.draft_from_description(
                title,
                invention_desc,
                technical_field
            )
            print(f"  Generated {len(self.patent.claims)} claims")

            # =====================================================
            # PHASE 5: Generate Figures
            # =====================================================
            self._report_phase(5, "Generating patent figures (Krea AI + Playwright)...")

            self.figures = self._generate_figures(title, invention_desc)
            figures_dir = os.path.join(output_dir, "patent_figures")
            os.makedirs(figures_dir, exist_ok=True)

            # Save figures
            for fig in self.figures:
                if fig.image_data:
                    fig_path = os.path.join(
                        figures_dir,
                        f"FIG_{fig.figure_number}_{fig.title.replace(' ', '_')}.{fig.image_format}"
                    )
                    with open(fig_path, 'wb') as f:
                        f.write(fig.image_data)

            print(f"  Generated {len(self.figures)} figures")

            # =====================================================
            # PHASE 6: Create .docx with Embedded Images
            # =====================================================
            self._report_phase(6, "Creating .docx document...")

            inventor = InventorInfo(
                name=inventor_name,
                address=inventor_address,
                city=inventor_city,
                state=inventor_state,
                zip_code=inventor_zip,
                country=inventor_country,
                entity_type=entity_type
            )

            patent_doc = PatentDocument(
                title=self.patent.title,
                inventor=inventor,
                field_of_invention=self.patent.field,
                background=self.patent.background,
                summary=self.patent.summary,
                brief_description_drawings=self.patent.brief_description_drawings,
                detailed_description=self.patent.detailed_description,
                claims=self.patent.claims,
                abstract=self.patent.abstract,
                figures=self.figures,
                assignee=assignee
            )

            docx_path = os.path.join(output_dir, f"provisional_patent_{timestamp}.docx")
            self.docx_generator.generate(patent_doc, docx_path)
            print(f"  Created: {docx_path}")

            # =====================================================
            # PHASE 7: Score Against Rubric
            # =====================================================
            self._report_phase(7, "Scoring against 100-point rubric...")

            self.score_result = self.scorer.score(patent_doc)

            # Save score report
            score_report_path = os.path.join(output_dir, "score_report.json")
            with open(score_report_path, 'w') as f:
                json.dump({
                    "score": self.score_result.total_score,
                    "grade": self.score_result.grade,
                    "category_scores": self.score_result.category_scores,
                    "deductions": self.score_result.deductions,
                    "bonuses": self.score_result.bonuses,
                    "recommendations": self.score_result.recommendations
                }, f, indent=2)

            print(f"  Score: {self.score_result.total_score}/100 - {self.score_result.grade}")

            # =====================================================
            # Complete!
            # =====================================================
            print(f"\n{'='*60}")
            print("PATENT GENERATION COMPLETE")
            print(f"{'='*60}")
            print(f"Output Directory: {output_dir}")
            print(f"DOCX File: {docx_path}")
            print(f"Figures: {len(self.figures)}")
            print(f"Score: {self.score_result.total_score}/100")
            print(f"Grade: {self.score_result.grade}")

            if self.score_result.recommendations:
                print(f"\nTop Recommendations:")
                for rec in self.score_result.recommendations[:3]:
                    print(f"  - {rec}")

            return PipelineResult(
                success=True,
                docx_path=docx_path,
                figures_dir=figures_dir,
                score_report_path=score_report_path,
                score=self.score_result.total_score,
                grade=self.score_result.grade,
                figure_count=len(self.figures),
                source_files=self.source_context.total_files,
                innovations_found=len(self.innovations),
                prior_art_references=prior_art_count
            )

        except Exception as e:
            import traceback
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            print(f"\nError: {error_msg}")

            return PipelineResult(
                success=False,
                docx_path="",
                figures_dir="",
                score_report_path="",
                score=0,
                grade="Failed",
                figure_count=0,
                source_files=0,
                innovations_found=0,
                prior_art_references=0,
                error=error_msg
            )

    def _load_source(self, source_path: str) -> Optional[SourceContext]:
        """Phase 1: Load source context"""
        try:
            return self.source_manager.load_source(source_path, source_type="auto")
        except Exception as e:
            print(f"  Error loading source: {e}")
            return None

    def _analyze_innovations(self) -> List[Dict]:
        """Phase 2: Analyze source for patentable innovations"""
        if not self.source_context:
            return []

        context_text = self._build_context_text()

        prompt = f"""Analyze this source code for patentable AI/software innovations:

{context_text[:20000]}

Identify ALL potentially patentable elements:

1. **Novel Algorithms or Methods**
   - Unique processing approaches
   - Custom optimization techniques
   - Novel data transformations

2. **System Architectures**
   - Unique component arrangements
   - Novel integration patterns
   - Innovative API designs

3. **Technical Improvements**
   - Performance optimizations
   - Efficiency gains
   - Resource usage improvements

4. **AI/ML Innovations**
   - Custom model architectures
   - Novel training techniques
   - Unique inference methods

For EACH innovation, provide:
- Technical title
- HOW it works (step-by-step)
- What makes it novel
- Potential method/system claims

Be thorough - focus on technical HOW, not business WHAT."""

        try:
            response = self.ai.generate(
                prompt,
                system_prompt="You are a patent analyst identifying patentable innovations in software/AI systems. Focus on technical implementation details.",
                max_tokens=4000
            )
            return [{"analysis": response.content}] if response.success else []
        except Exception as e:
            print(f"  Innovation analysis error: {e}")
            return [{"analysis": f"Manual analysis needed: {str(e)}"}]

    def _research_prior_art(self) -> Dict:
        """
        Phase 3: Research prior art using Perplexity Pro + PatentsView

        Perplexity Pro enhancements:
        - Multi-pass search (5 separate searches for comprehensive coverage)
        - 128k context window for deep analysis
        - Real-time USPTO/EPO/WIPO patent database access
        """
        if not self.innovations:
            return {"patents": [], "research": "", "differentiation_points": []}

        innovation_summary = ""
        if self.innovations:
            innovation_summary = self.innovations[0].get("analysis", "")[:6000]

        all_research = []

        # PASS 1: Core Patent Search
        print("    Pass 1/5: Searching USPTO patent database...")
        pass1_prompt = f"""Search for USPTO patents related to this invention:

{innovation_summary}

Search PatentsView for relevant patents. Focus on CPC: G06N (AI), G06F (Computing), G06Q (Business).
List 5-10 patent numbers (US XXXXXXXX A1/B2), titles, assignees.
Identify CLOSEST prior art and explain technical differences."""

        try:
            response = self.ai.research(pass1_prompt)
            if response.success:
                all_research.append("## USPTO Patent Search\n" + response.content)
        except Exception as e:
            all_research.append(f"USPTO search error: {e}")

        # PASS 2: Academic Papers
        print("    Pass 2/5: Searching academic publications...")
        pass2_prompt = f"""Search for academic papers related to:

{innovation_summary[:3000]}

Search arXiv, ACM, IEEE, Google Scholar. List 5-8 papers from 2022-2025 with titles, authors, contributions."""

        try:
            response = self.ai.research(pass2_prompt)
            if response.success:
                all_research.append("\n\n## Academic Research\n" + response.content)
        except Exception as e:
            all_research.append(f"Academic search error: {e}")

        # PASS 3: Competitive Landscape
        print("    Pass 3/5: Analyzing competitive landscape...")
        pass3_prompt = f"""Analyze competitive landscape for:

{innovation_summary[:2000]}

Find existing products, competitors, open-source projects. Identify market leaders and white space."""

        try:
            response = self.ai.research(pass3_prompt)
            if response.success:
                all_research.append("\n\n## Competitive Landscape\n" + response.content)
        except Exception as e:
            all_research.append(f"Competitive analysis error: {e}")

        # PASS 4: International Patents
        print("    Pass 4/5: Searching international patents...")
        pass4_prompt = f"""Search international patents for:

{innovation_summary[:2000]}

Search EPO, WIPO, JPO, CNIPA. List 3-5 patents with numbers, titles. Identify patent families."""

        try:
            response = self.ai.research(pass4_prompt)
            if response.success:
                all_research.append("\n\n## International Patents\n" + response.content)
        except Exception as e:
            all_research.append(f"International search error: {e}")

        # PASS 5: Novelty Analysis
        print("    Pass 5/5: Synthesizing novelty analysis...")
        combined = "\n".join(all_research)[:12000]

        pass5_prompt = f"""Novelty analysis for invention:

{innovation_summary[:2000]}

Prior art found:
{combined[:8000]}

Analyze: 1) Novelty (1-10 scale), 2) Non-obviousness, 3) Key differentiators (5-8 points), 4) Claim strategy."""

        differentiation_points = []
        try:
            response = self.ai.research(pass5_prompt)
            if response.success:
                all_research.append("\n\n## Novelty Analysis\n" + response.content)
                differentiation_points = self._extract_differentiation_points(response.content)
        except Exception as e:
            all_research.append(f"Novelty analysis error: {e}")

        full_research = "\n".join(all_research)
        patents_found = self._extract_patent_numbers(full_research)

        print(f"    Prior art complete: {len(patents_found)} patents identified")

        return {
            "patents": patents_found,
            "research": full_research,
            "differentiation_points": differentiation_points,
            "search_passes": 5,
            "perplexity_pro": True
        }

    def _extract_patent_numbers(self, text: str) -> List[str]:
        """Extract patent numbers from research text"""
        import re
        patterns = [r'US\s*\d{7,8}\s*[AB]\d?', r'EP\s*\d{7}', r'WO\s*\d{4}/\d{6}']
        patents = []
        for p in patterns:
            patents.extend(re.findall(p, text, re.IGNORECASE))
        return list(set(patents))[:20]

    def _extract_differentiation_points(self, text: str) -> List[str]:
        """Extract differentiation points from analysis"""
        import re
        points = re.findall(r'\d+\.\s+([^\n]{10,100})', text)
        points.extend(re.findall(r'[-*]\s+([^\n]{10,100})', text))
        return list(set(points))[:8]

    def _generate_title(self) -> str:
        """Generate invention title from context"""
        if not self.source_context:
            return "System and Method for Improved Data Processing"

        base_name = self.source_context.source_name
        base_name = base_name.replace("-", " ").replace("_", " ").title()

        # Clean up common words
        for word in ["Tool", "App", "Application", "Project", "V1", "V2"]:
            base_name = base_name.replace(word, "")

        return f"System and Method for {base_name.strip()}"

    def _build_invention_description(self) -> str:
        """Build comprehensive invention description"""
        parts = []

        # From innovations analysis
        if self.innovations:
            parts.append("## Technical Innovations\n")
            parts.append(self.innovations[0].get("analysis", "")[:8000])

        # From prior art differentiation
        if self.prior_art.get("research"):
            parts.append("\n\n## Prior Art Differentiation\n")
            parts.append(self.prior_art["research"][:4000])

        # From source context
        if self.source_context:
            parts.append("\n\n## Source Code Context\n")
            parts.append(self.source_context.summary)

            # Include key files
            for f in self.source_context.files[:15]:
                lang = f.language.lower() if f.language else ''
                parts.append(f"\n### {f.path}\n```{lang}")
                parts.append(f.content[:4000])
                parts.append("```")

        return "\n".join(parts)

    def _build_context_text(self) -> str:
        """Build text representation of source context"""
        if not self.source_context:
            return ""

        parts = [self.source_context.summary]

        for f in self.source_context.files[:25]:
            parts.append(f"\n--- {f.path} ---")
            parts.append(f.content[:6000])

        return "\n".join(parts)

    def _generate_figures(self, title: str, description: str) -> List[PatentFigure]:
        """Phase 5: Generate patent figures"""
        figures = []

        # Generate 5 standard figures (placeholders for now)
        figure_specs = [
            (1, "System Architecture", "illustrates a system 100 according to various embodiments.",
             {100: "System", 101: "Client Interface", 102: "Processing Engine",
              103: "Data Store", 104: "Network Interface"}),
            (2, "Hardware Block Diagram", "illustrates a computing device 200 suitable for implementing aspects of the invention.",
             {200: "Computing Device", 201: "Processor", 202: "Memory",
              203: "Storage", 204: "Network Interface", 205: "I/O Controller"}),
            (3, "Method Flowchart", "is a flowchart illustrating a method 300 according to various embodiments.",
             {300: "Method", 302: "Receive Input", 304: "Process Data",
              306: "Generate Output", 308: "End"}),
            (4, "Data Flow Diagram", "illustrates data flow 400 through the system according to various embodiments.",
             {400: "Data Flow", 401: "Raw Input", 402: "Preprocessing",
              403: "Core Processing", 404: "Output Generation"}),
            (5, "Alternative Embodiment", "illustrates an alternative implementation 500 according to various embodiments.",
             {500: "Alternative System", 501: "Distributed Nodes",
              502: "Central Coordinator", 503: "Results Aggregation"})
        ]

        for fig_num, fig_title, fig_desc, ref_nums in figure_specs:
            # Create placeholder figure
            figures.append(PatentFigure(
                figure_number=fig_num,
                title=fig_title,
                description=f"FIG. {fig_num} {fig_desc}",
                image_data=b'',  # Placeholder - would be generated by Krea AI
                image_format='png',
                reference_numerals=ref_nums
            ))

        return figures

    def cleanup(self):
        """Clean up resources"""
        pass  # Add cleanup for Playwright etc. when implemented


def run_patent_pipeline(
    source_path: str,
    inventor_name: str = "Inventor",
    inventor_address: str = "123 Main St",
    inventor_city: str = "City",
    inventor_state: str = "ST",
    inventor_zip: str = "12345",
    technical_field: str = "artificial intelligence",
    output_dir: str = None
) -> PipelineResult:
    """
    Convenience function to run the complete pipeline.

    Args:
        source_path: Path to source (local, GitHub, or GDrive)
        inventor_*: Inventor details
        technical_field: Technical field
        output_dir: Output directory

    Returns:
        PipelineResult
    """
    # Load config for API keys
    try:
        from config import (
            ANTHROPIC_API_KEY,
            OPENAI_API_KEY,
            PERPLEXITY_API_KEY,
            KREA_API_KEY
        )
    except ImportError:
        # Use environment variables as fallback
        import os
        ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
        KREA_API_KEY = os.getenv("KREA_API_KEY", "")

    pipeline = UnifiedPatentPipeline(
        claude_key=ANTHROPIC_API_KEY,
        openai_key=OPENAI_API_KEY,
        perplexity_key=PERPLEXITY_API_KEY,
        krea_key=KREA_API_KEY
    )

    return pipeline.run(
        source_path=source_path,
        inventor_name=inventor_name,
        inventor_address=inventor_address,
        inventor_city=inventor_city,
        inventor_state=inventor_state,
        inventor_zip=inventor_zip,
        technical_field=technical_field,
        output_dir=output_dir
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python unified_pipeline.py <source_path> [inventor_name]")
        print("\nExamples:")
        print("  python unified_pipeline.py C:/path/to/project")
        print("  python unified_pipeline.py https://github.com/owner/repo")
        sys.exit(1)

    source = sys.argv[1]
    inventor = sys.argv[2] if len(sys.argv) > 2 else "Inventor Name"

    result = run_patent_pipeline(source, inventor_name=inventor)

    if result.success:
        print(f"\nSuccess! Patent generated at: {result.docx_path}")
        print(f"Score: {result.score}/100 ({result.grade})")
    else:
        print(f"\nFailed: {result.error}")
