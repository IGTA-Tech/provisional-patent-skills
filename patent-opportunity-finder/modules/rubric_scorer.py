"""
Patent Rubric Scorer Module
============================
Score provisional patents against 100-point rubric.
Target: 90+ for Transaction-Ready status.

Based on: RAG/patentability-scoring/KNOWLEDGE_BASE.md

Categories:
- Technical Disclosure Quality (30 pts)
- Drawings & Figures (20 pts)
- Novelty & Differentiation (15 pts)
- Scope & Protection (15 pts)
- Implementation Details (10 pts)
- AI-Specific Requirements (10 pts)
- Bonus Points (+10 max)
- Red Flag Deductions
"""

from typing import Tuple, Dict, List
from dataclasses import dataclass
import re


@dataclass
class ScoringResult:
    """Complete scoring result"""
    total_score: int
    grade: str
    category_scores: Dict[str, Dict]
    deductions: Dict[str, int]
    bonuses: Dict[str, int]
    recommendations: List[str]


class RubricScorer:
    """
    Score provisional patents against the 100-point rubric.

    Grading Scale:
    - 95-100: Transaction Ready (95th Percentile)
    - 85-94: Excellent
    - 75-84: Good (Passing)
    - 65-74: Needs Improvement
    - 50-64: Insufficient
    - <50: Major Rework Required
    """

    GRADE_THRESHOLDS = [
        (95, "Transaction Ready (95th Percentile)"),
        (85, "Excellent"),
        (75, "Good (Passing)"),
        (65, "Needs Improvement"),
        (50, "Insufficient"),
        (0, "Major Rework Required")
    ]

    def score(self, patent_doc) -> ScoringResult:
        """
        Score a patent document against the rubric.

        Args:
            patent_doc: PatentDocument or similar object with patent sections

        Returns:
            ScoringResult with total score, grade, and details
        """
        category_scores = {}
        deductions = {}
        bonuses = {}
        recommendations = []

        # Get text content for analysis
        detailed_desc = getattr(patent_doc, 'detailed_description', '') or ''
        summary = getattr(patent_doc, 'summary', '') or ''
        background = getattr(patent_doc, 'background', '') or ''
        claims = getattr(patent_doc, 'claims', []) or []
        figures = getattr(patent_doc, 'figures', []) or []
        abstract = getattr(patent_doc, 'abstract', '') or ''

        full_text = f"{detailed_desc} {summary} {background}".lower()

        # 1. Technical Disclosure Quality (30 pts max)
        tech_score, tech_details, tech_recs = self._score_technical_disclosure(
            detailed_desc, full_text
        )
        category_scores['technical_disclosure'] = {
            'score': tech_score,
            'max': 30,
            'details': tech_details
        }
        recommendations.extend(tech_recs)

        # 2. Drawings & Figures (20 pts max)
        fig_score, fig_details, fig_recs = self._score_drawings(figures)
        category_scores['drawings_figures'] = {
            'score': fig_score,
            'max': 20,
            'details': fig_details
        }
        recommendations.extend(fig_recs)

        # 3. Novelty & Differentiation (15 pts max)
        nov_score, nov_details, nov_recs = self._score_novelty(full_text, summary)
        category_scores['novelty_differentiation'] = {
            'score': nov_score,
            'max': 15,
            'details': nov_details
        }
        recommendations.extend(nov_recs)

        # 4. Scope & Protection (15 pts max)
        scope_score, scope_details, scope_recs = self._score_scope(detailed_desc)
        category_scores['scope_protection'] = {
            'score': scope_score,
            'max': 15,
            'details': scope_details
        }
        recommendations.extend(scope_recs)

        # 5. Implementation Details (10 pts max)
        impl_score, impl_details, impl_recs = self._score_implementation(detailed_desc)
        category_scores['implementation_details'] = {
            'score': impl_score,
            'max': 10,
            'details': impl_details
        }
        recommendations.extend(impl_recs)

        # 6. AI-Specific Requirements (10 pts max)
        ai_score, ai_details, ai_recs = self._score_ai_specific(detailed_desc, full_text)
        category_scores['ai_specific'] = {
            'score': ai_score,
            'max': 10,
            'details': ai_details
        }
        recommendations.extend(ai_recs)

        # Check for red flags
        deductions = self._check_red_flags(full_text, figures, detailed_desc)

        # Check for bonuses
        bonuses = self._check_bonuses(claims, detailed_desc, full_text)

        # Calculate totals
        base_score = sum(cat['score'] for cat in category_scores.values())
        deduction_total = sum(deductions.values())
        bonus_total = min(sum(bonuses.values()), 10)  # Cap at 10

        final_score = max(0, min(100, base_score + deduction_total + bonus_total))

        # Determine grade
        grade = "Major Rework Required"
        for threshold, grade_name in self.GRADE_THRESHOLDS:
            if final_score >= threshold:
                grade = grade_name
                break

        return ScoringResult(
            total_score=final_score,
            grade=grade,
            category_scores=category_scores,
            deductions=deductions,
            bonuses=bonuses,
            recommendations=recommendations[:10]  # Top 10 recommendations
        )

    def _score_technical_disclosure(self, detailed_desc: str, full_text: str) -> Tuple[int, Dict, List]:
        """Score technical disclosure quality (30 pts max)"""
        details = {}
        recommendations = []
        desc_lower = detailed_desc.lower()

        # HOW not WHAT (8 pts)
        how_keywords = ["step", "process", "method", "comprise", "perform", "execute",
                       "receive", "transmit", "generate", "transform", "calculate"]
        how_count = sum(desc_lower.count(kw) for kw in how_keywords)

        if how_count >= 25:
            details['how_not_what'] = 8
        elif how_count >= 15:
            details['how_not_what'] = 6
        elif how_count >= 8:
            details['how_not_what'] = 4
        else:
            details['how_not_what'] = 2
            recommendations.append("Add more HOW details - describe step-by-step processes, not just outcomes")

        # Hardware context (6 pts)
        hw_keywords = ["processor", "memory", "cpu", "gpu", "tpu", "storage",
                      "network interface", "computing device", "server", "client"]
        hw_count = sum(desc_lower.count(kw) for kw in hw_keywords)

        if hw_count >= 15:
            details['hardware_context'] = 6
        elif hw_count >= 8:
            details['hardware_context'] = 4
        elif hw_count >= 3:
            details['hardware_context'] = 2
        else:
            details['hardware_context'] = 0
            recommendations.append("Add hardware context - mention processor, memory, storage, network")

        # Algorithm disclosure (8 pts)
        algo_patterns = [r"step \d+", r"at step", r"block \d+", r"at block",
                        r"algorithm", r"pseudocode", r"input.*output"]
        algo_count = sum(len(re.findall(p, desc_lower)) for p in algo_patterns)

        if algo_count >= 12:
            details['algorithm_disclosure'] = 8
        elif algo_count >= 6:
            details['algorithm_disclosure'] = 6
        elif algo_count >= 3:
            details['algorithm_disclosure'] = 4
        else:
            details['algorithm_disclosure'] = 2
            recommendations.append("Add step-by-step algorithm descriptions with numbered steps")

        # Enablement (8 pts) - based on comprehensiveness
        word_count = len(detailed_desc.split())
        has_examples = "example" in desc_lower or "embodiment" in desc_lower
        has_figures = "fig." in desc_lower or "figure" in desc_lower

        enablement_score = 0
        if word_count >= 3000:
            enablement_score += 4
        elif word_count >= 2000:
            enablement_score += 3
        elif word_count >= 1000:
            enablement_score += 2
        else:
            enablement_score += 1
            recommendations.append("Expand detailed description to 2000+ words")

        if has_examples:
            enablement_score += 2
        else:
            recommendations.append("Add concrete examples to aid enablement")

        if has_figures:
            enablement_score += 2
        else:
            recommendations.append("Reference figures throughout detailed description")

        details['enablement'] = min(enablement_score, 8)

        total = sum(details.values())
        return min(total, 30), details, recommendations

    def _score_drawings(self, figures: List) -> Tuple[int, Dict, List]:
        """Score drawings & figures (20 pts max)"""
        details = {}
        recommendations = []
        fig_count = len(figures) if figures else 0

        if fig_count == 0:
            recommendations.append("CRITICAL: Add at least 3-5 figures (system, hardware, flowchart)")
            return 0, {'no_figures': True}, recommendations

        # Extract figure titles for analysis
        fig_titles = [getattr(f, 'title', '').lower() for f in figures]
        all_titles = ' '.join(fig_titles)

        # System diagram (5 pts)
        has_system = any(kw in all_titles for kw in ['system', 'architecture', 'network'])
        details['system_diagram'] = 5 if has_system else 0
        if not has_system:
            recommendations.append("Add system architecture diagram (FIG. 1)")

        # Hardware block diagram (4 pts)
        has_hardware = any(kw in all_titles for kw in ['hardware', 'block', 'computing'])
        details['hardware_block_diagram'] = 4 if has_hardware else 0
        if not has_hardware:
            recommendations.append("Add hardware block diagram showing processor, memory, etc.")

        # Method flowcharts (6 pts)
        flowchart_count = sum(1 for t in fig_titles
                             if 'flowchart' in t or 'method' in t or 'process' in t)
        if flowchart_count >= 2:
            details['method_flowcharts'] = 6
        elif flowchart_count >= 1:
            details['method_flowcharts'] = 4
        else:
            details['method_flowcharts'] = 0
            recommendations.append("Add method flowchart(s) showing process steps")

        # Interface mockups (3 pts)
        has_ui = any(kw in all_titles for kw in ['interface', 'ui', 'screen', 'mockup', 'display'])
        details['interface_mockups'] = 3 if has_ui else 1  # 1 point if N/A

        # Data flow diagram (2 pts)
        has_data_flow = any(kw in all_titles for kw in ['data flow', 'data', 'pipeline'])
        details['data_flow_diagram'] = 2 if has_data_flow else 0
        if not has_data_flow:
            recommendations.append("Consider adding data flow diagram")

        total = sum(details.values())
        return min(total, 20), details, recommendations

    def _score_novelty(self, full_text: str, summary: str) -> Tuple[int, Dict, List]:
        """Score novelty & differentiation (15 pts max)"""
        details = {}
        recommendations = []

        # Prior art awareness (5 pts)
        prior_indicators = ["conventional", "existing", "prior", "traditional",
                          "known", "previous", "current systems"]
        pa_count = sum(full_text.count(kw) for kw in prior_indicators)

        if pa_count >= 5:
            details['prior_art_awareness'] = 5
        elif pa_count >= 2:
            details['prior_art_awareness'] = 3
        else:
            details['prior_art_awareness'] = 1
            recommendations.append("Acknowledge prior art and existing approaches")

        # Point of difference (5 pts)
        diff_indicators = ["improvement", "novel", "unique", "different", "unlike",
                         "advantage", "better", "superior", "overcome"]
        diff_count = sum(full_text.count(kw) for kw in diff_indicators)

        if diff_count >= 8:
            details['point_of_difference'] = 5
        elif diff_count >= 4:
            details['point_of_difference'] = 3
        else:
            details['point_of_difference'] = 1
            recommendations.append("Clearly state what makes this invention different/better")

        # Problem-solution (5 pts)
        has_problem = any(kw in full_text for kw in ["problem", "challenge", "limitation", "need", "issue"])
        has_solution = any(kw in full_text for kw in ["solution", "address", "overcome", "provide", "solve"])

        if has_problem and has_solution:
            details['problem_solution'] = 5
        elif has_problem or has_solution:
            details['problem_solution'] = 3
        else:
            details['problem_solution'] = 1
            recommendations.append("Clearly frame the technical problem and how invention solves it")

        total = sum(details.values())
        return min(total, 15), details, recommendations

    def _score_scope(self, detailed_desc: str) -> Tuple[int, Dict, List]:
        """Score scope & protection (15 pts max)"""
        details = {}
        recommendations = []
        desc_lower = detailed_desc.lower()

        # Workarounds & variations (8 pts)
        variation_indicators = ["embodiment", "alternative", "variation", "optionally",
                               "in some", "in various", "in another", "additionally"]
        var_count = sum(desc_lower.count(kw) for kw in variation_indicators)

        if var_count >= 20:
            details['workarounds_variations'] = 8
        elif var_count >= 12:
            details['workarounds_variations'] = 6
        elif var_count >= 6:
            details['workarounds_variations'] = 4
        else:
            details['workarounds_variations'] = 2
            recommendations.append("Add more alternative embodiments and variations")

        # Future variations (4 pts)
        future_indicators = ["future", "extension", "enhancement", "further",
                            "additionally", "moreover", "second generation"]
        future_count = sum(desc_lower.count(kw) for kw in future_indicators)

        if future_count >= 4:
            details['future_variations'] = 4
        elif future_count >= 2:
            details['future_variations'] = 2
        else:
            details['future_variations'] = 0
            recommendations.append("Describe future improvements and extensions")

        # Broad-to-narrow (3 pts)
        has_broad = "various embodiments" in desc_lower or "in general" in desc_lower
        has_narrow = "specific embodiment" in desc_lower or "in particular" in desc_lower

        if has_broad and has_narrow:
            details['broad_to_narrow'] = 3
        elif has_broad or "some embodiments" in desc_lower:
            details['broad_to_narrow'] = 2
        else:
            details['broad_to_narrow'] = 0
            recommendations.append("Use broad-to-narrow language pattern")

        total = sum(details.values())
        return min(total, 15), details, recommendations

    def _score_implementation(self, detailed_desc: str) -> Tuple[int, Dict, List]:
        """Score implementation details (10 pts max)"""
        details = {}
        recommendations = []
        desc_lower = detailed_desc.lower()

        # Deployment architecture (5 pts)
        deploy_indicators = ["deploy", "server", "cloud", "infrastructure",
                            "architecture", "distributed", "hosted", "cluster"]
        deploy_count = sum(desc_lower.count(kw) for kw in deploy_indicators)

        if deploy_count >= 6:
            details['deployment_architecture'] = 5
        elif deploy_count >= 3:
            details['deployment_architecture'] = 3
        else:
            details['deployment_architecture'] = 1
            recommendations.append("Describe deployment architecture and infrastructure")

        # Technology stack (3 pts)
        tech_indicators = ["api", "database", "framework", "protocol", "json",
                         "http", "rest", "queue", "cache"]
        tech_count = sum(desc_lower.count(kw) for kw in tech_indicators)

        if tech_count >= 5:
            details['technology_stack'] = 3
        elif tech_count >= 2:
            details['technology_stack'] = 2
        else:
            details['technology_stack'] = 0
            recommendations.append("Mention technology stack components")

        # Real world use (2 pts)
        use_indicators = ["example", "use case", "walkthrough", "scenario", "user"]
        has_use = any(kw in desc_lower for kw in use_indicators)
        details['real_world_use'] = 2 if has_use else 1

        total = sum(details.values())
        return min(total, 10), details, recommendations

    def _score_ai_specific(self, detailed_desc: str, full_text: str) -> Tuple[int, Dict, List]:
        """Score AI-specific requirements (10 pts max)"""
        details = {}
        recommendations = []
        desc_lower = detailed_desc.lower()

        # Practical application (4 pts)
        practical_indicators = ["improvement", "reduce", "increase", "optimize",
                               "enhance", "faster", "more efficient", "less memory"]
        pract_count = sum(desc_lower.count(kw) for kw in practical_indicators)

        if pract_count >= 6:
            details['practical_application'] = 4
        elif pract_count >= 3:
            details['practical_application'] = 2
        else:
            details['practical_application'] = 0
            recommendations.append("Emphasize practical technical improvements")

        # Not abstract (3 pts) - hardware integration
        has_processor = "processor" in desc_lower
        has_memory = "memory" in desc_lower
        has_hw = has_processor and has_memory

        if has_hw:
            details['not_abstract'] = 3
        elif has_processor or "computing device" in desc_lower:
            details['not_abstract'] = 2
        else:
            details['not_abstract'] = 0
            recommendations.append("Tie software to hardware (processor, memory) to avoid abstract idea issues")

        # Inventorship documentation (3 pts)
        details['inventorship_documentation'] = 3  # Assume documented

        total = sum(details.values())
        return min(total, 10), details, recommendations

    def _check_red_flags(self, full_text: str, figures: List, detailed_desc: str) -> Dict[str, int]:
        """Check for red flag deductions"""
        deductions = {}

        # Marketing language (-10)
        marketing_words = ["revolutionary", "best", "amazing", "groundbreaking",
                         "world-class", "cutting-edge", "game-changing"]
        if any(word in full_text for word in marketing_words):
            deductions["marketing_language"] = -10

        # No drawings (-10)
        if not figures or len(figures) == 0:
            deductions["no_drawings"] = -10

        # Vague AI/ML (-8)
        vague_ai = ("uses ai" in full_text or "uses machine learning" in full_text or
                   "leverages ai" in full_text)
        specific_ai = any(kw in full_text for kw in
                         ["neural network", "transformer", "model", "training", "inference"])
        if vague_ai and not specific_ai:
            deductions["vague_ai_ml"] = -8

        # No hardware context (-10)
        has_hardware = any(kw in detailed_desc.lower() for kw in
                          ["processor", "memory", "cpu", "gpu", "computing device"])
        if not has_hardware:
            deductions["no_hardware_context"] = -10

        # Missing reference numerals (-3)
        has_numerals = bool(re.search(r'\b[1-9]\d{2}\b', detailed_desc))  # 3-digit numbers
        if not has_numerals:
            deductions["missing_reference_numerals"] = -3

        return deductions

    def _check_bonuses(self, claims: List, detailed_desc: str, full_text: str) -> Dict[str, int]:
        """Check for bonus points"""
        bonuses = {}
        desc_lower = detailed_desc.lower()

        # Informal claims included (+3)
        if claims and len(claims) >= 5:
            bonuses["informal_claims"] = 3

        # Multiple embodiments (+3)
        embodiment_count = desc_lower.count("embodiment")
        if embodiment_count >= 5:
            bonuses["multiple_embodiments"] = 3

        # Performance benchmarks (+2)
        has_metrics = "%" in detailed_desc or re.search(r'\d+x faster', desc_lower)
        if has_metrics:
            bonuses["performance_benchmarks"] = 2

        # Competitive workaround analysis (+2)
        if "workaround" in desc_lower or "design around" in desc_lower:
            bonuses["competitive_workaround"] = 2

        return bonuses


def score_patent(patent_doc) -> Dict:
    """
    Convenience function to score a patent document.

    Args:
        patent_doc: Patent document object

    Returns:
        Dictionary with score details
    """
    scorer = RubricScorer()
    result = scorer.score(patent_doc)

    return {
        "score": result.total_score,
        "grade": result.grade,
        "category_scores": result.category_scores,
        "deductions": result.deductions,
        "bonuses": result.bonuses,
        "recommendations": result.recommendations
    }


if __name__ == "__main__":
    # Test the scorer with sample data
    print("Testing Rubric Scorer...")

    class MockPatent:
        def __init__(self):
            self.detailed_description = """
            ## Overview

            The present invention provides a system 100 for processing data using
            machine learning techniques. In various embodiments, the system comprises
            a processor 101, memory 102, and storage 103.

            ## Method of Operation

            At step 302, the system receives input data via network interface 104.
            At step 304, the processor 101 preprocesses the data using neural network
            techniques. At step 306, the processed data is analyzed.

            In some embodiments, the system may alternatively use GPU acceleration.
            In another embodiment, distributed processing may be employed.
            """
            self.summary = "The invention provides improvements over conventional systems."
            self.background = "Existing systems have limitations in processing speed."
            self.claims = ["A method...", "A system...", "A CRM...", "The method of claim 1...", "The system of claim 2..."]
            self.figures = []
            self.abstract = "A system for data processing."

    mock = MockPatent()

    # Add mock figures
    class MockFigure:
        def __init__(self, title):
            self.title = title

    mock.figures = [
        MockFigure("System Architecture"),
        MockFigure("Hardware Block Diagram"),
        MockFigure("Method Flowchart")
    ]

    result = score_patent(mock)
    print(f"\nScore: {result['score']}/100")
    print(f"Grade: {result['grade']}")
    print(f"\nCategory Scores:")
    for cat, data in result['category_scores'].items():
        print(f"  {cat}: {data['score']}/{data['max']}")
    print(f"\nDeductions: {result['deductions']}")
    print(f"Bonuses: {result['bonuses']}")
    print(f"\nRecommendations:")
    for rec in result['recommendations'][:5]:
        print(f"  - {rec}")
