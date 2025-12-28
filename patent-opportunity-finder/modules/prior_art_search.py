"""
Prior Art Search Module
=======================
Search USPTO PatentsView API for prior art related to invention ideas.
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Patent:
    """Represents a patent from search results"""
    patent_number: str
    title: str
    abstract: str
    date: str
    assignee: str
    citations: int
    cpc_codes: List[str]
    url: str
    relevance_score: float = 0.0


@dataclass
class PriorArtReport:
    """Complete prior art search report"""
    query: str
    technology_area: str
    search_date: str
    total_found: int
    patents: List[Patent]
    summary: str


class PriorArtSearcher:
    """Search USPTO PatentsView API for prior art"""

    BASE_URL = "https://search.patentsview.org/api/v1/patent/"

    # CPC Code mapping for common technology areas
    CPC_CODES = {
        "ai": "G06N",
        "machine_learning": "G06N20",
        "neural_networks": "G06N3",
        "nlp": "G06F40",
        "computer_vision": "G06V",
        "software": "G06F",
        "networking": "H04L",
        "security": "G06F21",
        "blockchain": "G06Q20",
        "robotics": "B25J",
        "iot": "H04W4",
        "cloud": "G06F9",
        "database": "G06F16"
    }

    def __init__(self):
        self.session = requests.Session()

    def search_by_keywords(
        self,
        keywords: str,
        technology_area: str = "ai",
        since_date: str = None,
        max_results: int = 50
    ) -> PriorArtReport:
        """
        Search for patents by keywords in abstract

        Args:
            keywords: Search terms (space-separated)
            technology_area: One of CPC_CODES keys
            since_date: YYYY-MM-DD format, defaults to 5 years ago
            max_results: Maximum patents to return
        """
        if since_date is None:
            since_date = (datetime.now() - timedelta(days=365*5)).strftime("%Y-%m-%d")

        cpc_code = self.CPC_CODES.get(technology_area.lower(), "G06N")

        query = {
            "_and": [
                {"_text_any": {"patent_abstract": keywords}},
                {"cpc_current.cpc_subgroup_id": {"_begins": cpc_code}},
                {"_gte": {"patent_date": since_date}}
            ]
        }

        return self._execute_search(query, keywords, technology_area, max_results)

    def search_by_cpc(
        self,
        cpc_code: str,
        keywords: str = None,
        since_date: str = None,
        max_results: int = 50
    ) -> PriorArtReport:
        """
        Search by CPC classification code with optional keywords
        """
        if since_date is None:
            since_date = (datetime.now() - timedelta(days=365*5)).strftime("%Y-%m-%d")

        conditions = [
            {"cpc_current.cpc_subgroup_id": {"_begins": cpc_code}},
            {"_gte": {"patent_date": since_date}}
        ]

        if keywords:
            conditions.append({"_text_any": {"patent_abstract": keywords}})

        query = {"_and": conditions}

        return self._execute_search(query, keywords or cpc_code, cpc_code, max_results)

    def search_expiring_patents(
        self,
        technology_area: str = "ai",
        min_citations: int = 10,
        years_until_expiry: float = 2.0
    ) -> PriorArtReport:
        """
        Find high-value patents expiring soon (white space opportunities)
        """
        cpc_code = self.CPC_CODES.get(technology_area.lower(), "G06N")

        # Patents filed 18-20 years ago are expiring
        filing_start = (datetime.now() - timedelta(days=365*20)).strftime("%Y-%m-%d")
        filing_end = (datetime.now() - timedelta(days=365*(20-years_until_expiry))).strftime("%Y-%m-%d")

        query = {
            "_and": [
                {"_gte": {"application.filing_date": filing_start}},
                {"_lte": {"application.filing_date": filing_end}},
                {"_gte": {"citedby_patent_count": min_citations}},
                {"cpc_current.cpc_subgroup_id": {"_begins": cpc_code}}
            ]
        }

        return self._execute_search(
            query,
            f"Expiring {technology_area} patents",
            technology_area,
            100,
            sort_by_citations=True
        )

    def search_competitor(
        self,
        company_name: str,
        technology_area: str = None,
        max_results: int = 100
    ) -> PriorArtReport:
        """
        Find all patents owned by a specific company
        """
        conditions = [
            {"assignees_at_grant.assignee_organization": {"_contains": company_name}}
        ]

        if technology_area:
            cpc_code = self.CPC_CODES.get(technology_area.lower(), "G06N")
            conditions.append({"cpc_current.cpc_subgroup_id": {"_begins": cpc_code}})

        query = {"_and": conditions} if len(conditions) > 1 else conditions[0]

        return self._execute_search(
            query,
            f"{company_name} patents",
            technology_area or "all",
            max_results,
            sort_by_citations=True
        )

    def _execute_search(
        self,
        query: Dict,
        search_terms: str,
        technology_area: str,
        max_results: int,
        sort_by_citations: bool = False
    ) -> PriorArtReport:
        """Execute the search query and return formatted results"""

        fields = [
            "patent_number",
            "patent_title",
            "patent_abstract",
            "patent_date",
            "application.filing_date",
            "assignees_at_grant.assignee_organization",
            "citedby_patent_count",
            "cpc_current.cpc_subgroup_id",
            "cpc_current.cpc_subgroup_title"
        ]

        options = {"size": min(max_results, 1000)}

        sort_order = [{"citedby_patent_count": "desc"}] if sort_by_citations else [{"patent_date": "desc"}]

        params = {
            "q": json.dumps(query),
            "f": json.dumps(fields),
            "o": json.dumps(options),
            "s": json.dumps(sort_order)
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return PriorArtReport(
                query=search_terms,
                technology_area=technology_area,
                search_date=datetime.now().isoformat(),
                total_found=0,
                patents=[],
                summary=f"Search failed: {str(e)}"
            )

        patents = []
        for p in data.get('patents', []):
            # Extract assignee
            assignees = p.get('assignees_at_grant', [])
            assignee = assignees[0].get('assignee_organization', 'Individual') if assignees else 'Individual'

            # Extract CPC codes
            cpc_list = p.get('cpc_current', [])
            cpc_codes = [c.get('cpc_subgroup_id', '') for c in cpc_list[:5]]

            patent = Patent(
                patent_number=p.get('patent_number', ''),
                title=p.get('patent_title', ''),
                abstract=p.get('patent_abstract', '')[:500],
                date=p.get('patent_date', ''),
                assignee=assignee,
                citations=p.get('citedby_patent_count', 0),
                cpc_codes=cpc_codes,
                url=f"https://patents.google.com/patent/US{p.get('patent_number', '')}"
            )
            patents.append(patent)

        # Generate summary
        total = data.get('total_hits', len(patents))
        top_assignees = self._get_top_assignees(patents)

        summary = f"Found {total} patents matching '{search_terms}' in {technology_area}. "
        if top_assignees:
            summary += f"Top assignees: {', '.join(top_assignees[:3])}. "
        if patents:
            avg_citations = sum(p.citations for p in patents) / len(patents)
            summary += f"Average citations: {avg_citations:.1f}."

        return PriorArtReport(
            query=search_terms,
            technology_area=technology_area,
            search_date=datetime.now().isoformat(),
            total_found=total,
            patents=patents,
            summary=summary
        )

    def _get_top_assignees(self, patents: List[Patent]) -> List[str]:
        """Get most common assignees from patent list"""
        assignee_counts = {}
        for p in patents:
            if p.assignee != 'Individual':
                assignee_counts[p.assignee] = assignee_counts.get(p.assignee, 0) + 1

        sorted_assignees = sorted(assignee_counts.items(), key=lambda x: x[1], reverse=True)
        return [a[0] for a in sorted_assignees[:5]]


def search_prior_art(keywords: str, technology: str = "ai") -> PriorArtReport:
    """Convenience function for quick prior art search"""
    searcher = PriorArtSearcher()
    return searcher.search_by_keywords(keywords, technology)


def find_white_space(technology: str = "ai", min_citations: int = 10) -> PriorArtReport:
    """Convenience function to find expiring patent opportunities"""
    searcher = PriorArtSearcher()
    return searcher.search_expiring_patents(technology, min_citations)


if __name__ == "__main__":
    # Test the module
    print("Testing Prior Art Search...")

    result = search_prior_art("transformer attention mechanism", "neural_networks")
    print(f"\n{result.summary}")
    print(f"\nTop 5 patents:")
    for p in result.patents[:5]:
        print(f"  US{p.patent_number}: {p.title[:60]}... ({p.citations} citations)")
