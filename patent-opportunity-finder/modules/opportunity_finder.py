"""
Opportunity Finder Module
=========================
Analyze prior art to identify patent opportunities.
"""

import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

from .prior_art_search import PriorArtSearcher, PriorArtReport, Patent
from .ai_providers import AIOrchestrator, AIResponse


@dataclass
class PatentOpportunity:
    """Represents a potential patent opportunity"""
    title: str
    description: str
    opportunity_type: str  # improvement, combination, white_space, design_around
    related_patents: List[str]
    technical_approach: str
    patentability_score: int  # 0-100
    market_value: str  # low, medium, high
    difficulty: str  # low, medium, high
    priority_score: float
    recommended_claims: List[str]
    risks: List[str]


@dataclass
class OpportunityReport:
    """Complete opportunity analysis report"""
    technology_area: str
    analysis_date: str
    prior_art_count: int
    opportunities: List[PatentOpportunity]
    executive_summary: str
    recommended_actions: List[str]


class OpportunityFinder:
    """
    Analyzes prior art to identify patent opportunities
    """

    SYSTEM_PROMPT = """You are an expert patent strategist with deep knowledge of AI/software patents.
Your role is to analyze prior art and identify valuable patent opportunities.

When analyzing, consider:
1. Gaps in existing patent coverage
2. Improvement opportunities on existing patents
3. Novel combinations of existing technologies
4. Design-around opportunities
5. Expiring patents that open white space

For each opportunity, assess:
- Technical feasibility (can it be built?)
- Market value (is it commercially valuable?)
- Patentability (is it novel and non-obvious?)
- Competition (who else might file?)
"""

    def __init__(self, ai_orchestrator: AIOrchestrator = None):
        self.searcher = PriorArtSearcher()
        self.ai = ai_orchestrator

    def analyze_technology_area(
        self,
        technology: str,
        keywords: str,
        deep_analysis: bool = True
    ) -> OpportunityReport:
        """
        Comprehensive analysis of a technology area for opportunities

        Args:
            technology: Technology area (ai, machine_learning, etc.)
            keywords: Specific keywords to focus on
            deep_analysis: Use AI for deeper analysis (requires API key)
        """
        # Step 1: Search recent patents
        recent_art = self.searcher.search_by_keywords(keywords, technology, max_results=50)

        # Step 2: Search expiring patents
        expiring = self.searcher.search_expiring_patents(technology, min_citations=5)

        # Step 3: Identify opportunities
        opportunities = []

        # 3a: White space from expiring patents
        for patent in expiring.patents[:10]:
            opp = self._create_white_space_opportunity(patent)
            opportunities.append(opp)

        # 3b: Improvement opportunities from recent patents
        for patent in recent_art.patents[:10]:
            if patent.citations > 5:  # Focus on influential patents
                opp = self._create_improvement_opportunity(patent)
                opportunities.append(opp)

        # Step 4: AI-powered deep analysis
        if deep_analysis and self.ai and self.ai.get_available_providers():
            opportunities = self._enhance_with_ai(opportunities, recent_art, expiring)

        # Step 5: Score and rank opportunities
        opportunities = self._score_opportunities(opportunities)
        opportunities.sort(key=lambda x: x.priority_score, reverse=True)

        # Step 6: Generate report
        summary = self._generate_summary(technology, keywords, opportunities)
        actions = self._generate_actions(opportunities[:5])

        return OpportunityReport(
            technology_area=technology,
            analysis_date=datetime.now().isoformat(),
            prior_art_count=recent_art.total_found + expiring.total_found,
            opportunities=opportunities[:20],  # Top 20
            executive_summary=summary,
            recommended_actions=actions
        )

    def _create_white_space_opportunity(self, patent: Patent) -> PatentOpportunity:
        """Create opportunity from expiring patent"""

        # Calculate expiry date
        try:
            filing_date = datetime.strptime(patent.date, "%Y-%m-%d")
            expiry_date = filing_date + timedelta(days=365*20)
            days_left = (expiry_date - datetime.now()).days
        except:
            days_left = 365

        return PatentOpportunity(
            title=f"Improvement on: {patent.title[:50]}...",
            description=f"Base patent US{patent.patent_number} expires in ~{days_left} days. "
                       f"High citation count ({patent.citations}) indicates valuable technology.",
            opportunity_type="white_space",
            related_patents=[patent.patent_number],
            technical_approach=f"Build upon or improve the technology in US{patent.patent_number}. "
                              f"Focus on modern implementations or efficiency improvements.",
            patentability_score=70,  # Base score, adjusted later
            market_value="high" if patent.citations > 20 else "medium",
            difficulty="medium",
            priority_score=0,  # Calculated later
            recommended_claims=[
                f"Method improving upon US{patent.patent_number} by [specific improvement]",
                "System implementing [improvement] for [technical benefit]"
            ],
            risks=[
                "Other companies may file similar improvements",
                "Need to ensure sufficient differentiation from original"
            ]
        )

    def _create_improvement_opportunity(self, patent: Patent) -> PatentOpportunity:
        """Create improvement opportunity from active patent"""

        return PatentOpportunity(
            title=f"Enhancement to: {patent.title[:50]}...",
            description=f"Highly-cited patent ({patent.citations} citations) by {patent.assignee}. "
                       f"Improvement patents can add significant value.",
            opportunity_type="improvement",
            related_patents=[patent.patent_number],
            technical_approach="Identify limitations in current implementation and propose improvements. "
                              "Focus on speed, accuracy, efficiency, or new applications.",
            patentability_score=65,
            market_value="medium" if patent.citations > 10 else "low",
            difficulty="medium",
            priority_score=0,
            recommended_claims=[
                f"Improved method for [function] achieving [benefit] over prior approaches",
                "System optimizing [aspect] through [novel technique]"
            ],
            risks=[
                f"Original assignee ({patent.assignee}) may have continuation applications",
                "Must ensure clear differentiation from original claims"
            ]
        )

    def _enhance_with_ai(
        self,
        opportunities: List[PatentOpportunity],
        recent_art: PriorArtReport,
        expiring: PriorArtReport
    ) -> List[PatentOpportunity]:
        """Use AI to enhance opportunity analysis"""

        # Create summary of prior art for AI
        art_summary = "Recent Patents:\n"
        for p in recent_art.patents[:10]:
            art_summary += f"- US{p.patent_number}: {p.title} ({p.citations} citations)\n"

        art_summary += "\nExpiring Patents:\n"
        for p in expiring.patents[:10]:
            art_summary += f"- US{p.patent_number}: {p.title} ({p.citations} citations)\n"

        prompt = f"""Analyze this patent landscape and identify the TOP 5 patent opportunities:

{art_summary}

For each opportunity, provide:
1. Specific technical approach
2. Why it's patentable (novel and non-obvious)
3. Estimated market value
4. Key risks

Format as JSON array with keys: title, approach, patentability_reason, market_value, risks"""

        response = self.ai.generate(prompt, system_prompt=self.SYSTEM_PROMPT)

        if response.success:
            try:
                # Try to parse AI response and enhance opportunities
                # This is a simplified version - production would parse more carefully
                ai_insights = response.content

                # Add AI insights to first few opportunities
                for i, opp in enumerate(opportunities[:5]):
                    opp.description += f"\n\nAI Analysis: {ai_insights[:500]}"
                    opp.patentability_score += 10  # Boost for AI-validated opportunities

            except Exception as e:
                pass  # Continue without AI enhancement if parsing fails

        return opportunities

    def _score_opportunities(self, opportunities: List[PatentOpportunity]) -> List[PatentOpportunity]:
        """Calculate priority score for each opportunity"""

        market_values = {"low": 1, "medium": 2, "high": 3}
        difficulty_values = {"low": 1.5, "medium": 1.0, "high": 0.5}
        type_values = {"white_space": 1.3, "improvement": 1.0, "combination": 1.2, "design_around": 0.8}

        for opp in opportunities:
            # Priority = (Patentability + Market) * Difficulty Factor * Type Factor
            market = market_values.get(opp.market_value, 1)
            difficulty = difficulty_values.get(opp.difficulty, 1)
            type_factor = type_values.get(opp.opportunity_type, 1)

            opp.priority_score = (opp.patentability_score + market * 20) * difficulty * type_factor

        return opportunities

    def _generate_summary(
        self,
        technology: str,
        keywords: str,
        opportunities: List[PatentOpportunity]
    ) -> str:
        """Generate executive summary"""

        white_space = sum(1 for o in opportunities if o.opportunity_type == "white_space")
        improvements = sum(1 for o in opportunities if o.opportunity_type == "improvement")
        high_value = sum(1 for o in opportunities if o.market_value == "high")

        return f"""Patent Opportunity Analysis for {technology.upper()} ({keywords})

Identified {len(opportunities)} total opportunities:
- {white_space} white space opportunities (from expiring patents)
- {improvements} improvement opportunities (on active patents)
- {high_value} high market value opportunities

Top opportunity: {opportunities[0].title if opportunities else 'None identified'}

Recommended focus: {'White space' if white_space > improvements else 'Improvement patents'}
"""

    def _generate_actions(self, top_opportunities: List[PatentOpportunity]) -> List[str]:
        """Generate recommended actions"""

        actions = []

        for i, opp in enumerate(top_opportunities[:3], 1):
            actions.append(f"{i}. Pursue {opp.opportunity_type} patent: {opp.title[:50]}...")

        actions.extend([
            "4. Conduct detailed prior art search on top opportunities",
            "5. Draft provisional applications for top 2-3 opportunities",
            "6. Set up monitoring for competitor filings in this space"
        ])

        return actions


def find_opportunities(technology: str, keywords: str, ai_keys: Dict = None) -> OpportunityReport:
    """
    Convenience function to find patent opportunities

    Args:
        technology: Technology area (ai, machine_learning, software, etc.)
        keywords: Specific search keywords
        ai_keys: Dict with claude_key, openai_key, perplexity_key

    Returns:
        OpportunityReport with ranked opportunities
    """
    ai = None
    if ai_keys:
        ai = AIOrchestrator(**ai_keys)

    finder = OpportunityFinder(ai)
    return finder.analyze_technology_area(technology, keywords, deep_analysis=bool(ai))


if __name__ == "__main__":
    print("Testing Opportunity Finder...")

    report = find_opportunities("ai", "transformer attention mechanism")

    print(f"\n{report.executive_summary}")
    print("\nTop 5 Opportunities:")
    for i, opp in enumerate(report.opportunities[:5], 1):
        print(f"\n{i}. {opp.title}")
        print(f"   Type: {opp.opportunity_type}")
        print(f"   Score: {opp.priority_score:.1f}")
        print(f"   Value: {opp.market_value}")
