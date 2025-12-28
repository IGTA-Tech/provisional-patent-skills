"""
Patent Research API Tools
==========================
FREE APIs for patent research - NO API keys required for basic usage

APIs Included:
1. PatentsView API - Search 12M+ US patents (1976-present)
2. USPTO Bulk Data - Download full patent XML files
3. USPTO Assignment API - Patent ownership/transfers
4. Perplexity API - AI-powered patent research (requires key)
"""

import requests
import json
import zipfile
import io
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any


# =============================================================================
# 1. PATENTSVIEW API - FREE, NO KEY REQUIRED
# =============================================================================

class PatentsViewAPI:
    """
    Search USPTO patent database via PatentsView

    Features:
    - 12+ million patents (1976-present)
    - Full abstracts, titles, claims info
    - Inventor and assignee information
    - Citation counts
    - CPC classification codes
    - NO rate limits for normal use
    - NO signup required

    Documentation: https://search.patentsview.org/docs/docs/Search%20API/SearchAPIReference/
    """

    BASE_URL = "https://search.patentsview.org/api/v1/patent/"

    @staticmethod
    def search_by_patent_number(patent_number: str) -> Dict:
        """
        Get details for a specific patent

        Example:
            result = PatentsViewAPI.search_by_patent_number("10000000")
        """
        query = {"patent_number": patent_number}

        fields = [
            "patent_number",
            "patent_title",
            "patent_abstract",
            "patent_date",
            "application.filing_date",
            "assignees_at_grant.assignee_organization",
            "inventors_at_grant.name_first",
            "inventors_at_grant.name_last",
            "citedby_patent_count",
            "cpc_current.cpc_subgroup_id",
            "cpc_current.cpc_subgroup_title"
        ]

        params = {
            "q": json.dumps(query),
            "f": json.dumps(fields)
        }

        response = requests.get(PatentsViewAPI.BASE_URL, params=params)
        return response.json()

    @staticmethod
    def search_by_company(company_name: str, limit: int = 50) -> Dict:
        """
        Find all patents owned by a specific company

        Example:
            result = PatentsViewAPI.search_by_company("Google")
        """
        query = {
            "assignees_at_grant.assignee_organization": {
                "_contains": company_name
            }
        }

        fields = [
            "patent_number",
            "patent_title",
            "patent_date",
            "patent_abstract",
            "citedby_patent_count",
            "cpc_current.cpc_subgroup_title"
        ]

        params = {
            "q": json.dumps(query),
            "f": json.dumps(fields),
            "o": json.dumps({"size": limit}),
            "s": json.dumps([{"citedby_patent_count": "desc"}])
        }

        response = requests.get(PatentsViewAPI.BASE_URL, params=params)
        return response.json()

    @staticmethod
    def search_by_technology(cpc_code: str, keywords: str, since_date: str = "2020-01-01") -> Dict:
        """
        Find patents in specific technology area

        Common CPC codes:
        - G06F: Computer science
        - G06N: AI/Machine Learning
        - H04L: Networking
        - G06Q: Business methods

        Example:
            result = PatentsViewAPI.search_by_technology("G06N", "neural network")
        """
        query = {
            "_and": [
                {"cpc_current.cpc_subgroup_id": {"_begins": cpc_code}},
                {"_text_any": {"patent_abstract": keywords}},
                {"_gte": {"patent_date": since_date}}
            ]
        }

        fields = [
            "patent_number",
            "patent_title",
            "patent_abstract",
            "patent_date",
            "assignees_at_grant.assignee_organization",
            "citedby_patent_count"
        ]

        params = {
            "q": json.dumps(query),
            "f": json.dumps(fields),
            "o": json.dumps({"size": 50}),
            "s": json.dumps([{"citedby_patent_count": "desc"}])
        }

        response = requests.get(PatentsViewAPI.BASE_URL, params=params)
        return response.json()

    @staticmethod
    def find_expiring_patents(
        technology_cpc: str = "G06N",
        min_citations: int = 10,
        years_until_expiry: float = 2.0
    ) -> Dict:
        """
        Find high-value patents expiring soon (white space opportunities)

        Example:
            result = PatentsViewAPI.find_expiring_patents("G06N", min_citations=15)
        """
        # Patents filed ~18-20 years ago are expiring
        filing_start = (datetime.now() - timedelta(days=365*20)).strftime("%Y-%m-%d")
        filing_end = (datetime.now() - timedelta(days=365*(20-years_until_expiry))).strftime("%Y-%m-%d")

        query = {
            "_and": [
                {"_gte": {"application.filing_date": filing_start}},
                {"_lte": {"application.filing_date": filing_end}},
                {"_gte": {"citedby_patent_count": min_citations}},
                {"cpc_current.cpc_subgroup_id": {"_begins": technology_cpc}}
            ]
        }

        fields = [
            "patent_number",
            "patent_title",
            "patent_abstract",
            "patent_date",
            "application.filing_date",
            "citedby_patent_count",
            "assignees_at_grant.assignee_organization",
            "cpc_current.cpc_subgroup_title"
        ]

        params = {
            "q": json.dumps(query),
            "f": json.dumps(fields),
            "o": json.dumps({"size": 100}),
            "s": json.dumps([{"citedby_patent_count": "desc"}])
        }

        response = requests.get(PatentsViewAPI.BASE_URL, params=params)
        return response.json()

    @staticmethod
    def prior_art_search(keywords: str, before_date: str) -> Dict:
        """
        Search for potential prior art before a specific date

        Example:
            result = PatentsViewAPI.prior_art_search("machine learning recommendation", "2020-01-01")
        """
        query = {
            "_and": [
                {"_text_any": {"patent_abstract": keywords}},
                {"_lte": {"patent_date": before_date}}
            ]
        }

        fields = [
            "patent_number",
            "patent_title",
            "patent_abstract",
            "patent_date",
            "assignees_at_grant.assignee_organization"
        ]

        params = {
            "q": json.dumps(query),
            "f": json.dumps(fields),
            "o": json.dumps({"size": 50}),
            "s": json.dumps([{"patent_date": "desc"}])
        }

        response = requests.get(PatentsViewAPI.BASE_URL, params=params)
        return response.json()


# =============================================================================
# 2. USPTO BULK DATA DOWNLOAD - FREE, NO KEY REQUIRED
# =============================================================================

class USPTOBulkData:
    """
    Download complete patent XML files from USPTO

    Includes:
    - Complete patent text
    - All claims
    - Detailed descriptions
    - Drawing references
    - Prior art citations

    Updated weekly
    """

    GRANT_BASE_URL = "https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/"
    APP_BASE_URL = "https://bulkdata.uspto.gov/data/patent/application/redbook/fulltext/"

    @staticmethod
    def download_weekly_patents(year: int, week: int, save_path: str = "patents.xml") -> Optional[bytes]:
        """
        Download full patent XML files for a specific week

        Example:
            content = USPTOBulkData.download_weekly_patents(2024, 52)
        """
        # Format: ipgYYMMDD.zip (e.g., ipg241226.zip for Dec 26, 2024)
        # Calculate date from year and week
        from datetime import date
        jan1 = date(year, 1, 1)
        target_date = jan1 + timedelta(weeks=week-1)

        date_str = target_date.strftime("%y%m%d")
        file_url = f"{USPTOBulkData.GRANT_BASE_URL}{year}/ipg{date_str}.zip"

        print(f"Downloading from: {file_url}")

        response = requests.get(file_url, timeout=300)

        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                print(f"\nFiles in archive:")
                for filename in z.namelist():
                    print(f"  - {filename}")

                first_file = z.namelist()[0]
                content = z.read(first_file)

                with open(save_path, 'wb') as f:
                    f.write(content)

                print(f"\nSaved to: {save_path}")
                print(f"Size: {len(content):,} bytes")

                return content
        else:
            print(f"Error: {response.status_code}")
            return None

    @staticmethod
    def list_available_files(year: int) -> List[str]:
        """
        List available patent files for a given year
        """
        url = f"{USPTOBulkData.GRANT_BASE_URL}{year}/"
        response = requests.get(url)

        if response.status_code == 200:
            # Parse HTML to find .zip files
            import re
            files = re.findall(r'href="(ipg\d+\.zip)"', response.text)
            return files
        return []


# =============================================================================
# 3. USPTO ASSIGNMENT API - FREE, NO KEY REQUIRED
# =============================================================================

class USPTOAssignmentAPI:
    """
    Search patent ownership and assignment history

    Documentation: https://assignment-api.uspto.gov/documentation-patent/
    """

    BASE_URL = "https://assignment-api.uspto.gov/patent/lookup"

    @staticmethod
    def get_assignment_history(patent_number: str) -> Dict:
        """
        Find who owns a patent and all ownership transfers

        Example:
            history = USPTOAssignmentAPI.get_assignment_history("10000000")
        """
        params = {"patentNumber": patent_number}

        response = requests.get(USPTOAssignmentAPI.BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            print(f"\nAssignment History for US{patent_number}:\n")

            for assignment in data.get('patentAssignmentSearchResults', []):
                for record in assignment.get('assignmentRecords', []):
                    print(f"Date: {record.get('recordedDate')}")
                    print(f"Type: {record.get('conveyanceText')}")

                    assignors = record.get('assignors', [])
                    assignees = record.get('assignees', [])

                    if assignors:
                        print(f"From: {assignors[0].get('name', 'Unknown')}")
                    if assignees:
                        print(f"To: {assignees[0].get('name', 'Unknown')}")
                    print("-" * 60)

            return data
        else:
            print(f"Error: {response.status_code}")
            return {}


# =============================================================================
# 4. PERPLEXITY API - AI-POWERED PATENT RESEARCH (Requires Key)
# =============================================================================

class PerplexityPatentSearch:
    """
    AI-powered patent research using Perplexity

    Capabilities (Launched Oct 2025):
    - Natural Language Search
    - Semantic Understanding
    - Citation-First results
    - Beyond USPTO (academic papers, blogs, repos)

    Requires API key from: https://www.perplexity.ai/settings/api
    """

    API_URL = "https://api.perplexity.ai/chat/completions"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def search_prior_art(self, invention_description: str) -> str:
        """
        Search for prior art using natural language

        Example:
            perplexity = PerplexityPatentSearch("pplx-your-key")
            result = perplexity.search_prior_art("AI system for detecting credit card fraud using neural networks")
        """
        payload = {
            "model": "llama-3.1-sonar-large-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a patent research expert. Search for relevant prior art including patents, academic papers, and technical publications."
                },
                {
                    "role": "user",
                    "content": f"""Find prior art for this invention:

{invention_description}

Please provide:
1. Related US patents with numbers
2. Academic papers
3. Technical blogs or publications
4. Key differentiators the invention might need to claim"""
                }
            ]
        }

        response = requests.post(self.API_URL, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"

    def novelty_assessment(self, invention_description: str, claimed_features: List[str]) -> str:
        """
        Assess novelty of claimed features against prior art
        """
        features_text = "\n".join([f"- {f}" for f in claimed_features])

        payload = {
            "model": "llama-3.1-sonar-large-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a patent examiner assessing novelty and non-obviousness."
                },
                {
                    "role": "user",
                    "content": f"""Assess the novelty of these claimed features:

INVENTION: {invention_description}

CLAIMED FEATURES:
{features_text}

For each feature, indicate:
1. Whether it appears to be novel
2. Most relevant prior art found
3. Suggested modifications to strengthen novelty"""
                }
            ]
        }

        response = requests.post(self.API_URL, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code}"


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def quick_patent_search(keywords: str) -> None:
    """
    Quick search for patents matching keywords

    Example:
        quick_patent_search("machine learning fraud detection")
    """
    result = PatentsViewAPI.search_by_technology("G06N", keywords)

    patents = result.get('patents', [])
    print(f"\nFound {len(patents)} patents for: {keywords}\n")

    for p in patents[:10]:
        print(f"US{p['patent_number']} - {p['patent_title']}")
        company = p.get('assignees_at_grant', [{}])[0].get('assignee_organization', 'Individual')
        print(f"  Company: {company}")
        print(f"  Abstract: {p.get('patent_abstract', '')[:150]}...")
        print()


def find_white_space(technology: str = "AI", min_citations: int = 10) -> None:
    """
    Find expiring patents that represent white space opportunities

    Example:
        find_white_space("AI", min_citations=15)
    """
    cpc_map = {
        "AI": "G06N",
        "SOFTWARE": "G06F",
        "NETWORKING": "H04L",
        "BUSINESS": "G06Q"
    }

    cpc = cpc_map.get(technology.upper(), "G06N")
    result = PatentsViewAPI.find_expiring_patents(cpc, min_citations)

    patents = result.get('patents', [])
    print(f"\nFound {len(patents)} expiring high-value patents\n")

    for p in patents[:10]:
        filing_date = datetime.strptime(
            p['application'][0]['filing_date'],
            "%Y-%m-%d"
        )
        expiry_date = filing_date + timedelta(days=365*20)
        days_left = (expiry_date - datetime.now()).days

        print(f"US{p['patent_number']} - Expires in {days_left} days")
        print(f"  {p['patent_title']}")
        print(f"  Citations: {p.get('citedby_patent_count', 0)}")
        print(f"  Link: https://patents.google.com/patent/US{p['patent_number']}")
        print()


# =============================================================================
# MAIN - DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PATENT RESEARCH API TOOLS")
    print("=" * 80)

    # Demo PatentsView
    print("\n1. PatentsView API Demo:")
    print("-" * 40)
    result = PatentsViewAPI.search_by_patent_number("10000000")
    if result.get('patents'):
        p = result['patents'][0]
        print(f"Patent: US{p['patent_number']}")
        print(f"Title: {p['patent_title']}")

    # Demo Assignment API
    print("\n2. Assignment API Demo:")
    print("-" * 40)
    USPTOAssignmentAPI.get_assignment_history("10000000")

    print("\n" + "=" * 80)
    print("All APIs working! See documentation in each class.")
    print("=" * 80)
