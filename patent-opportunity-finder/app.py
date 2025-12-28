"""
Patent Opportunity Finder - Streamlit UI
=========================================
A comprehensive tool for finding patent opportunities and drafting provisionals.

Run with: streamlit run app.py
"""

import streamlit as st
import json
import os
from datetime import datetime
from dataclasses import asdict

# Import our modules
from modules.prior_art_search import PriorArtSearcher, search_prior_art, find_white_space
from modules.ai_providers import AIOrchestrator, YouTubeTranscriptProvider
from modules.opportunity_finder import OpportunityFinder, find_opportunities
from modules.patent_drafter import PatentDrafter, draft_patent
import config

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Patent Opportunity Finder",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# STYLES
# =============================================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
    }
    .opportunity-card {
        border: 1px solid #E5E7EB;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        background: #F9FAFB;
    }
    .score-high { color: #059669; font-weight: bold; }
    .score-medium { color: #D97706; font-weight: bold; }
    .score-low { color: #DC2626; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE
# =============================================================================

if 'prior_art_results' not in st.session_state:
    st.session_state.prior_art_results = None
if 'opportunities' not in st.session_state:
    st.session_state.opportunities = None
if 'drafted_patent' not in st.session_state:
    st.session_state.drafted_patent = None
if 'ai_orchestrator' not in st.session_state:
    st.session_state.ai_orchestrator = AIOrchestrator(**config.get_api_keys())

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    # API Status
    st.markdown("### API Status")
    providers = config.get_available_providers()
    for provider in ["claude", "openai", "perplexity"]:
        if provider in providers:
            st.success(f"✓ {provider.title()} Connected")
        else:
            st.warning(f"✗ {provider.title()} Not Configured")

    st.markdown("---")

    # Technology Areas
    st.markdown("### Technology Areas")
    tech_options = {
        "AI/Machine Learning": "ai",
        "Neural Networks": "neural_networks",
        "NLP": "nlp",
        "Computer Vision": "computer_vision",
        "Software": "software",
        "Networking": "networking",
        "Security": "security",
        "Blockchain": "blockchain",
        "Robotics": "robotics",
        "IoT": "iot"
    }

    selected_tech = st.selectbox(
        "Select Technology",
        options=list(tech_options.keys()),
        index=0
    )
    technology = tech_options[selected_tech]

    st.markdown("---")

    # Settings
    st.markdown("### Settings")
    max_results = st.slider("Max Results", 10, 100, 50)
    min_citations = st.slider("Min Citations (for white space)", 5, 50, 10)

    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    **Patent Opportunity Finder** helps you:
    - Search prior art in USPTO database
    - Find expiring patent opportunities
    - Identify gaps and improvements
    - Draft provisional applications

    Built with Claude, OpenAI, and Perplexity APIs.
    """)

# =============================================================================
# MAIN CONTENT
# =============================================================================

st.markdown('<p class="main-header">🔬 Patent Opportunity Finder</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Find prior art, identify opportunities, and draft provisional patents</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Prior Art Search",
    "💡 Find Opportunities",
    "📝 Draft Patent",
    "📊 Analysis Dashboard",
    "🎬 Research Videos"
])

# =============================================================================
# TAB 1: PRIOR ART SEARCH
# =============================================================================

with tab1:
    st.markdown("### Search USPTO Patent Database")

    col1, col2 = st.columns([3, 1])

    with col1:
        search_keywords = st.text_input(
            "Enter search keywords",
            placeholder="e.g., transformer attention mechanism, fraud detection neural network"
        )

    with col2:
        search_type = st.selectbox(
            "Search Type",
            ["Keywords", "Expiring Patents", "Competitor"]
        )

    if search_type == "Competitor":
        company_name = st.text_input("Company Name", placeholder="e.g., Google, OpenAI")

    if st.button("🔍 Search Prior Art", type="primary"):
        with st.spinner("Searching USPTO database..."):
            searcher = PriorArtSearcher()

            if search_type == "Keywords" and search_keywords:
                results = searcher.search_by_keywords(
                    search_keywords,
                    technology,
                    max_results=max_results
                )
            elif search_type == "Expiring Patents":
                results = searcher.search_expiring_patents(
                    technology,
                    min_citations=min_citations
                )
            elif search_type == "Competitor" and company_name:
                results = searcher.search_competitor(
                    company_name,
                    technology,
                    max_results=max_results
                )
            else:
                st.warning("Please enter search criteria")
                results = None

            if results:
                st.session_state.prior_art_results = results

    # Display results
    if st.session_state.prior_art_results:
        results = st.session_state.prior_art_results

        st.markdown("---")
        st.markdown(f"### Results: {results.total_found} patents found")
        st.info(results.summary)

        for i, patent in enumerate(results.patents[:20]):
            with st.expander(f"US{patent.patent_number}: {patent.title[:60]}..."):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"**Assignee:** {patent.assignee}")
                    st.markdown(f"**Date:** {patent.date}")
                with col2:
                    st.metric("Citations", patent.citations)
                with col3:
                    st.markdown(f"[View Patent]({patent.url})")

                st.markdown("**Abstract:**")
                st.markdown(patent.abstract)

                if patent.cpc_codes:
                    st.markdown(f"**CPC Codes:** {', '.join(patent.cpc_codes[:3])}")

# =============================================================================
# TAB 2: FIND OPPORTUNITIES
# =============================================================================

with tab2:
    st.markdown("### Identify Patent Opportunities")

    opp_keywords = st.text_input(
        "Technology Focus",
        placeholder="e.g., efficient attention mechanism, real-time fraud detection",
        key="opp_keywords"
    )

    col1, col2 = st.columns(2)
    with col1:
        use_ai = st.checkbox("Use AI for deep analysis", value=True)
    with col2:
        include_expiring = st.checkbox("Include expiring patent opportunities", value=True)

    if st.button("💡 Find Opportunities", type="primary"):
        if not opp_keywords:
            st.warning("Please enter a technology focus")
        else:
            with st.spinner("Analyzing patent landscape..."):
                ai = st.session_state.ai_orchestrator if use_ai else None
                finder = OpportunityFinder(ai)
                report = finder.analyze_technology_area(
                    technology,
                    opp_keywords,
                    deep_analysis=use_ai
                )
                st.session_state.opportunities = report

    # Display opportunities
    if st.session_state.opportunities:
        report = st.session_state.opportunities

        st.markdown("---")
        st.markdown("### Opportunity Report")
        st.markdown(report.executive_summary)

        st.markdown("### Recommended Actions")
        for i, action in enumerate(report.recommended_actions, 1):
            st.markdown(f"{action}")

        st.markdown("---")
        st.markdown("### Top Opportunities")

        for i, opp in enumerate(report.opportunities[:10], 1):
            score_class = "score-high" if opp.priority_score > 100 else "score-medium" if opp.priority_score > 70 else "score-low"

            with st.expander(f"#{i} {opp.title[:60]}... (Score: {opp.priority_score:.0f})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Patentability", f"{opp.patentability_score}/100")
                with col2:
                    st.metric("Market Value", opp.market_value.title())
                with col3:
                    st.metric("Type", opp.opportunity_type.replace("_", " ").title())

                st.markdown("**Description:**")
                st.markdown(opp.description)

                st.markdown("**Technical Approach:**")
                st.markdown(opp.technical_approach)

                if opp.recommended_claims:
                    st.markdown("**Suggested Claims:**")
                    for claim in opp.recommended_claims:
                        st.markdown(f"- {claim}")

                if opp.risks:
                    st.warning("**Risks:** " + " | ".join(opp.risks))

                if st.button(f"📝 Draft Patent for This", key=f"draft_{i}"):
                    st.session_state.selected_opportunity = opp
                    st.info("Go to 'Draft Patent' tab to generate application")

# =============================================================================
# TAB 3: DRAFT PATENT
# =============================================================================

with tab3:
    st.markdown("### Draft Provisional Patent Application")

    draft_mode = st.radio(
        "Drafting Mode",
        ["From Description", "From Opportunity"],
        horizontal=True
    )

    if draft_mode == "From Description":
        inv_title = st.text_input(
            "Invention Title",
            placeholder="e.g., Memory-Efficient Attention Mechanism for Neural Networks"
        )

        inv_description = st.text_area(
            "Technical Description",
            placeholder="Describe your invention in detail. Focus on HOW it works, not just what it does...",
            height=200
        )

        inv_field = st.selectbox(
            "Technical Field",
            ["artificial intelligence", "machine learning", "software systems", "data processing", "networking"]
        )

        if st.button("📝 Generate Draft", type="primary"):
            if not inv_title or not inv_description:
                st.warning("Please provide title and description")
            else:
                with st.spinner("Generating patent application (this may take a minute)..."):
                    drafter = PatentDrafter(st.session_state.ai_orchestrator)
                    patent = drafter.draft_from_description(
                        inv_title,
                        inv_description,
                        inv_field
                    )
                    st.session_state.drafted_patent = patent

    else:  # From Opportunity
        if hasattr(st.session_state, 'selected_opportunity'):
            opp = st.session_state.selected_opportunity
            st.info(f"Selected: {opp.title}")

            additional_details = st.text_area(
                "Additional Technical Details",
                placeholder="Add any specific implementation details...",
                height=150
            )

            if st.button("📝 Generate from Opportunity", type="primary"):
                with st.spinner("Generating patent application..."):
                    drafter = PatentDrafter(st.session_state.ai_orchestrator)
                    patent = drafter.draft_from_opportunity(opp, additional_details)
                    st.session_state.drafted_patent = patent
        else:
            st.info("First find opportunities in the 'Find Opportunities' tab, then select one to draft.")

    # Display drafted patent
    if st.session_state.drafted_patent:
        patent = st.session_state.drafted_patent

        st.markdown("---")
        st.markdown("### Generated Provisional Patent Application")

        # Download button
        patent_dict = asdict(patent)
        patent_json = json.dumps(patent_dict, indent=2, default=str)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download as JSON",
                patent_json,
                f"provisional_patent_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                "application/json"
            )
        with col2:
            # Create markdown version
            md_content = f"""# {patent.title}

## Field of Invention
{patent.field}

## Background
{patent.background}

## Summary of Invention
{patent.summary}

## Brief Description of Drawings
{patent.brief_description_drawings}

## Detailed Description
{patent.detailed_description}

## Claims
{"\\n\\n".join(patent.claims)}

## Abstract
{patent.abstract}
"""
            st.download_button(
                "📥 Download as Markdown",
                md_content,
                f"provisional_patent_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                "text/markdown"
            )

        # Display sections
        with st.expander("📋 Title & Field"):
            st.markdown(f"**Title:** {patent.title}")
            st.markdown(f"**Field:** {patent.field}")

        with st.expander("📖 Background"):
            st.markdown(patent.background)

        with st.expander("📝 Summary"):
            st.markdown(patent.summary)

        with st.expander("🖼️ Figures"):
            st.markdown(patent.brief_description_drawings)
            for fig in patent.figures:
                st.markdown(f"**FIG. {fig['number']}:** {fig['title']}")

        with st.expander("📚 Detailed Description", expanded=True):
            st.markdown(patent.detailed_description)

        with st.expander("⚖️ Claims"):
            for i, claim in enumerate(patent.claims, 1):
                st.markdown(claim)
                st.markdown("---")

        with st.expander("📄 Abstract"):
            st.markdown(patent.abstract)

# =============================================================================
# TAB 4: ANALYSIS DASHBOARD
# =============================================================================

with tab4:
    st.markdown("### Patent Analysis Dashboard")

    if st.session_state.prior_art_results:
        results = st.session_state.prior_art_results

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Patents", results.total_found)
        with col2:
            if results.patents:
                avg_citations = sum(p.citations for p in results.patents) / len(results.patents)
                st.metric("Avg Citations", f"{avg_citations:.1f}")
        with col3:
            if results.patents:
                high_cite = sum(1 for p in results.patents if p.citations > 20)
                st.metric("High Citation", high_cite)
        with col4:
            st.metric("Technology", technology.upper())

        # Top assignees
        st.markdown("### Top Assignees")
        assignee_counts = {}
        for p in results.patents:
            if p.assignee != 'Individual':
                assignee_counts[p.assignee] = assignee_counts.get(p.assignee, 0) + 1

        sorted_assignees = sorted(assignee_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        if sorted_assignees:
            import pandas as pd
            df = pd.DataFrame(sorted_assignees, columns=["Assignee", "Patents"])
            st.bar_chart(df.set_index("Assignee"))
    else:
        st.info("Run a prior art search to see analysis")

    if st.session_state.opportunities:
        report = st.session_state.opportunities

        st.markdown("### Opportunity Distribution")
        opp_types = {}
        for opp in report.opportunities:
            opp_types[opp.opportunity_type] = opp_types.get(opp.opportunity_type, 0) + 1

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**By Type:**")
            for t, c in opp_types.items():
                st.markdown(f"- {t.replace('_', ' ').title()}: {c}")
        with col2:
            st.markdown("**By Value:**")
            high_value = sum(1 for o in report.opportunities if o.market_value == "high")
            med_value = sum(1 for o in report.opportunities if o.market_value == "medium")
            low_value = sum(1 for o in report.opportunities if o.market_value == "low")
            st.markdown(f"- High: {high_value}")
            st.markdown(f"- Medium: {med_value}")
            st.markdown(f"- Low: {low_value}")

# =============================================================================
# TAB 5: RESEARCH VIDEOS
# =============================================================================

with tab5:
    st.markdown("### Patent Research from YouTube")

    yt = YouTubeTranscriptProvider()

    video_url = st.text_input(
        "YouTube Video URL or ID",
        placeholder="e.g., https://youtube.com/watch?v=abc123 or abc123"
    )

    if st.button("🎬 Get Transcript"):
        if not video_url:
            st.warning("Please enter a video URL or ID")
        else:
            # Extract video ID
            if "youtube.com" in video_url or "youtu.be" in video_url:
                if "v=" in video_url:
                    video_id = video_url.split("v=")[1].split("&")[0]
                elif "youtu.be/" in video_url:
                    video_id = video_url.split("youtu.be/")[1].split("?")[0]
                else:
                    video_id = video_url
            else:
                video_id = video_url

            with st.spinner("Fetching transcript..."):
                result = yt.get_transcript(video_id)

                if result["success"]:
                    st.success(f"Transcript loaded: {result['length']:,} characters")

                    with st.expander("View Transcript"):
                        st.markdown(result["transcript"])

                    # Analyze with AI
                    if st.button("🤖 Extract Patent Insights"):
                        with st.spinner("Analyzing transcript..."):
                            prompt = f"""Extract patent-relevant insights from this transcript:

{result['transcript'][:10000]}

Provide:
1. Key technical concepts that could be patented
2. Novel methods or systems described
3. Potential patent claims
4. Prior art mentioned"""

                            response = st.session_state.ai_orchestrator.generate(
                                prompt,
                                system_prompt="You are a patent analyst extracting patentable concepts."
                            )

                            if response.success:
                                st.markdown("### Extracted Insights")
                                st.markdown(response.content)
                else:
                    st.error(f"Error: {result['error']}")

    st.markdown("---")
    st.markdown("### Pre-loaded Expert Transcripts")
    st.info("15 expert patent videos already transcribed (73,000+ words) - see RAG/expert-transcripts/")

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    Patent Opportunity Finder | Built with Streamlit, Claude, OpenAI, Perplexity<br>
    <a href="https://github.com/IGTA-Tech/provisional-patent-skills">GitHub Repository</a>
</div>
""", unsafe_allow_html=True)
