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
from modules.source_integrations import (
    SourceManager, SourceContext, LocalFolderScanner,
    GitHubIntegration, GoogleDriveIntegration
)
from modules.image_generator import (
    PatentImageManager, KreaAIGenerator, PlaywrightCapture, generate_patent_figures
)
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
if 'loaded_sources' not in st.session_state:
    st.session_state.loaded_sources = []  # List of SourceContext objects
if 'source_manager' not in st.session_state:
    st.session_state.source_manager = SourceManager(
        github_token=os.getenv("GITHUB_TOKEN"),
        gdrive_credentials=os.getenv("GOOGLE_CREDENTIALS_PATH")
    )

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
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📁 Sources",
    "🔍 Prior Art Search",
    "💡 Find Opportunities",
    "📝 Draft Patent",
    "🖼️ Images & Diagrams",
    "📊 Analysis Dashboard",
    "🎬 Research Videos"
])

# =============================================================================
# TAB 1: SOURCES (Local Folders, GitHub, Google Drive)
# =============================================================================

with tab1:
    st.markdown("### 📁 Load Source Context")
    st.markdown("Load code repositories, local folders, or Google Drive folders to provide context for patent analysis and drafting.")

    # Source type selection
    source_type = st.selectbox(
        "Source Type",
        ["Local Folder", "GitHub Repository", "Google Drive Folder"],
        key="source_type_select"
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        if source_type == "Local Folder":
            source_path = st.text_input(
                "Folder Path",
                placeholder="/path/to/your/project or ~/my-project",
                key="local_folder_path"
            )
            st.caption("Enter the full path to a local folder containing your code or documents.")

        elif source_type == "GitHub Repository":
            source_path = st.text_input(
                "GitHub URL or owner/repo",
                placeholder="https://github.com/owner/repo or owner/repo",
                key="github_url"
            )
            st.caption("Enter a GitHub repository URL or owner/repo format.")

        elif source_type == "Google Drive Folder":
            source_path = st.text_input(
                "Google Drive Folder URL or ID",
                placeholder="https://drive.google.com/drive/folders/... or folder ID",
                key="gdrive_url"
            )
            st.caption("Enter a Google Drive folder URL or folder ID. Requires configured credentials.")

    with col2:
        max_files = st.number_input("Max Files", min_value=10, max_value=200, value=50, key="max_files_input")

    # Load button
    if st.button("📥 Load Source", type="primary", key="load_source_btn"):
        if source_path:
            with st.spinner(f"Loading {source_type}..."):
                try:
                    # Map source type
                    type_map = {
                        "Local Folder": "local",
                        "GitHub Repository": "github",
                        "Google Drive Folder": "gdrive"
                    }

                    ctx = st.session_state.source_manager.load_source(
                        source_path,
                        source_type=type_map[source_type],
                        max_files=max_files
                    )

                    # Add to loaded sources
                    st.session_state.loaded_sources.append(ctx)
                    st.success(f"Loaded {ctx.total_files} files from {ctx.source_name}")

                except Exception as e:
                    st.error(f"Error loading source: {str(e)}")
        else:
            st.warning("Please enter a source path or URL")

    st.markdown("---")

    # Show loaded sources
    st.markdown("### 📚 Loaded Sources")

    if st.session_state.loaded_sources:
        for i, ctx in enumerate(st.session_state.loaded_sources):
            with st.expander(f"**{ctx.source_type.upper()}**: {ctx.source_name} ({ctx.total_files} files)", expanded=False):
                st.markdown(f"**Summary:**\n```\n{ctx.summary}\n```")

                st.markdown("**Structure:**")
                if ctx.structure.get("folders"):
                    st.markdown(f"- Folders: {len(ctx.structure['folders'])}")
                st.markdown(f"- Files: {len(ctx.structure.get('files', []))}")

                # Show file list
                st.markdown("**Files loaded:**")
                file_list = [f.path for f in ctx.files[:30]]
                for f in file_list:
                    st.text(f"  • {f}")
                if len(ctx.files) > 30:
                    st.text(f"  ... and {len(ctx.files) - 30} more")

                # Remove button
                if st.button(f"🗑️ Remove", key=f"remove_source_{i}"):
                    st.session_state.loaded_sources.pop(i)
                    st.rerun()

        # Export combined context
        st.markdown("---")
        if st.button("📋 Copy Combined Context to Clipboard", key="copy_context_btn"):
            combined = ""
            for ctx in st.session_state.loaded_sources:
                combined += f"\n\n## {ctx.source_type.upper()}: {ctx.source_name}\n\n"
                combined += ctx.summary + "\n\n"
                for f in ctx.files[:20]:
                    combined += f"### {f.path}\n```\n{f.content[:3000]}\n```\n\n"
            st.code(combined[:50000], language="markdown")
            st.success("Context displayed above - copy as needed")

        # Show total stats
        total_files = sum(ctx.total_files for ctx in st.session_state.loaded_sources)
        total_size = sum(ctx.total_size for ctx in st.session_state.loaded_sources)
        st.info(f"**Total:** {len(st.session_state.loaded_sources)} sources, {total_files} files, {total_size / 1024:.1f} KB")

    else:
        st.info("No sources loaded yet. Add a local folder, GitHub repo, or Google Drive folder above.")

    # Quick tips
    st.markdown("---")
    st.markdown("""
    **Tips:**
    - **Local Folders**: Great for your own projects. Scans .py, .js, .ts, .md, .json and more.
    - **GitHub Repos**: Fetches public repos directly. For private repos, set GITHUB_TOKEN env var.
    - **Google Drive**: Requires Google API credentials. Set GOOGLE_CREDENTIALS_PATH env var.
    - Sources are used in **Draft Patent** tab to provide technical context for AI drafting.
    """)

# =============================================================================
# TAB 2: PRIOR ART SEARCH
# =============================================================================

with tab2:
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
# TAB 3: FIND OPPORTUNITIES
# =============================================================================

with tab3:
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
# TAB 4: DRAFT PATENT
# =============================================================================

with tab4:
    st.markdown("### Draft Provisional Patent Application")

    draft_mode = st.radio(
        "Drafting Mode",
        ["From Description", "From Opportunity"],
        horizontal=True
    )

    # Source context section
    if st.session_state.loaded_sources:
        st.markdown("#### 📁 Source Context Available")
        use_sources = st.checkbox(
            f"Include context from {len(st.session_state.loaded_sources)} loaded source(s)",
            value=True,
            key="use_sources_for_draft"
        )
        if use_sources:
            source_names = [ctx.source_name for ctx in st.session_state.loaded_sources]
            st.caption(f"Sources: {', '.join(source_names)}")
    else:
        use_sources = False
        st.info("💡 Tip: Load source files in the 'Sources' tab to provide code context for better patent drafts.")

    st.markdown("---")

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
                # Build source context if enabled
                source_context = ""
                if use_sources and st.session_state.loaded_sources:
                    source_context = "\n\n--- SOURCE CODE CONTEXT ---\n"
                    for ctx in st.session_state.loaded_sources:
                        source_context += f"\n## {ctx.source_type.upper()}: {ctx.source_name}\n"
                        source_context += f"{ctx.summary}\n\n"
                        for f in ctx.files[:15]:  # Limit files per source
                            source_context += f"### File: {f.path}\n```{f.language.lower() if f.language else ''}\n"
                            source_context += f.content[:5000]  # Truncate long files
                            source_context += "\n```\n\n"

                with st.spinner("Generating patent application (this may take a minute)..."):
                    drafter = PatentDrafter(st.session_state.ai_orchestrator)
                    # Append source context to description
                    full_description = inv_description
                    if source_context:
                        full_description += source_context
                    patent = drafter.draft_from_description(
                        inv_title,
                        full_description,
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
            claims_text = "\n\n".join(patent.claims)
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
{claims_text}

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
# TAB 5: IMAGES & DIAGRAMS
# =============================================================================

with tab5:
    st.markdown("### Generate Patent Figures & Diagrams")
    st.markdown("Create USPTO-style diagrams and capture screenshots for your patent application.")

    # Initialize image manager in session state
    if 'image_manager' not in st.session_state:
        st.session_state.image_manager = PatentImageManager(config.KREA_API_KEY)
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = []

    # Three columns for different image types
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### AI-Generated Diagrams")
        diagram_type = st.selectbox(
            "Diagram Type",
            ["System Architecture", "Flowchart", "Block Diagram", "Data Flow", "UI Wireframe"],
            key="diagram_type_select"
        )

        diagram_desc = st.text_area(
            "Describe the diagram",
            placeholder="e.g., Machine learning inference pipeline with preprocessing, model, and postprocessing stages",
            height=100,
            key="diagram_description"
        )

        if st.button("🎨 Generate Diagram", type="primary", key="gen_diagram_btn"):
            if diagram_desc:
                with st.spinner("Generating diagram..."):
                    type_map = {
                        "System Architecture": "system_architecture",
                        "Flowchart": "flowchart",
                        "Block Diagram": "block_diagram",
                        "Data Flow": "data_flow",
                        "UI Wireframe": "ui_wireframe"
                    }
                    krea = KreaAIGenerator(config.KREA_API_KEY)
                    img = krea.generate_patent_diagram(
                        diagram_desc,
                        diagram_type=type_map[diagram_type]
                    )
                    st.session_state.generated_images.append(img)
                    st.success(f"Generated {diagram_type} diagram!")
            else:
                st.warning("Please enter a description")

    with col2:
        st.markdown("#### Webpage Screenshots")
        screenshot_url = st.text_input(
            "URL to capture",
            placeholder="https://github.com/owner/repo",
            key="screenshot_url"
        )

        full_page = st.checkbox("Capture full page", value=False, key="full_page_check")

        if st.button("📸 Capture Screenshot", key="capture_screenshot_btn"):
            if screenshot_url:
                with st.spinner("Capturing webpage..."):
                    try:
                        pw = PlaywrightCapture()
                        img = pw.capture_webpage(screenshot_url, full_page=full_page)
                        if img:
                            st.session_state.generated_images.append(img)
                            st.success("Screenshot captured!")
                        else:
                            st.error("Failed to capture. Is Playwright installed?")
                        pw.close()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.info("Run: pip install playwright && playwright install chromium")
            else:
                st.warning("Please enter a URL")

    with col3:
        st.markdown("#### Code Screenshots")
        code_input = st.text_area(
            "Paste code to render",
            placeholder="def my_invention():\n    # Your code here\n    pass",
            height=150,
            key="code_input"
        )

        code_lang = st.selectbox(
            "Language",
            ["python", "javascript", "typescript", "java", "cpp", "go", "rust"],
            key="code_lang_select"
        )

        if st.button("📷 Render Code", key="render_code_btn"):
            if code_input:
                with st.spinner("Rendering code..."):
                    try:
                        pw = PlaywrightCapture()
                        img = pw.capture_code_as_image(code_input, code_lang)
                        if img:
                            st.session_state.generated_images.append(img)
                            st.success("Code rendered!")
                        else:
                            st.error("Failed to render. Is Playwright installed?")
                        pw.close()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please paste some code")

    st.markdown("---")

    # Display generated images
    st.markdown("### Generated Figures")

    if st.session_state.generated_images:
        for i, img in enumerate(st.session_state.generated_images):
            with st.expander(f"**FIG. {i+1}** - {img.description[:50]}...", expanded=True):
                col_img, col_info = st.columns([3, 1])

                with col_img:
                    if img.format == "svg":
                        st.markdown(img.image_data.decode('utf-8'), unsafe_allow_html=True)
                    else:
                        st.image(img.image_data, caption=f"FIG. {i+1}")

                with col_info:
                    st.markdown(f"**Source:** {img.source}")
                    st.markdown(f"**Format:** {img.format}")
                    st.markdown(f"**Size:** {img.width}x{img.height}")

                    # Download button
                    st.download_button(
                        f"📥 Download FIG. {i+1}",
                        img.image_data,
                        file_name=f"FIG_{i+1}_{img.filename}",
                        mime=f"image/{img.format}" if img.format != "svg" else "image/svg+xml",
                        key=f"download_fig_{i}"
                    )

                    # Remove button
                    if st.button(f"🗑️ Remove", key=f"remove_fig_{i}"):
                        st.session_state.generated_images.pop(i)
                        st.rerun()

        st.markdown("---")

        # Bulk actions
        col_bulk1, col_bulk2 = st.columns(2)

        with col_bulk1:
            if st.button("📦 Download All as ZIP", key="download_all_zip"):
                import io
                import zipfile

                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for i, img in enumerate(st.session_state.generated_images):
                        zf.writestr(f"FIG_{i+1}_{img.filename}", img.image_data)

                st.download_button(
                    "💾 Save ZIP File",
                    zip_buffer.getvalue(),
                    file_name=f"patent_figures_{datetime.now().strftime('%Y%m%d')}.zip",
                    mime="application/zip",
                    key="save_zip"
                )

        with col_bulk2:
            if st.button("🗑️ Clear All Figures", key="clear_all_figs"):
                st.session_state.generated_images = []
                st.rerun()

        # Generate Brief Description of Drawings
        st.markdown("### Brief Description of Drawings")
        descriptions = []
        for i, img in enumerate(st.session_state.generated_images, 1):
            descriptions.append(f"FIG. {i} is a {img.source} showing {img.description}.")

        st.text_area(
            "Copy this to your patent application:",
            value="\n\n".join(descriptions),
            height=150,
            key="brief_desc_output"
        )

    else:
        st.info("No figures generated yet. Use the tools above to create diagrams and screenshots.")

    # Tips
    st.markdown("---")
    st.markdown("""
    **Tips for Patent Figures:**
    - USPTO requires clear, black and white line drawings
    - Number each element (100, 101, 102...) and reference in description
    - Include: System overview, flowcharts, block diagrams, UI mockups
    - Minimum 3-5 figures for a strong provisional application
    - Screenshots of prior art can help show differentiation
    """)

# =============================================================================
# TAB 6: ANALYSIS DASHBOARD
# =============================================================================

with tab6:
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
# TAB 7: RESEARCH VIDEOS
# =============================================================================

with tab7:
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
