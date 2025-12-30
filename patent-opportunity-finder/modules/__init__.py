"""
Patent Opportunity Finder Modules
=================================
"""

from .prior_art_search import PriorArtSearcher, search_prior_art, find_white_space
from .ai_providers import (
    AIOrchestrator,
    ClaudeProvider,
    OpenAIProvider,
    PerplexityProvider,
    DiagramProvider,
    YouTubeTranscriptProvider
)
from .opportunity_finder import OpportunityFinder, find_opportunities
from .patent_drafter import PatentDrafter, draft_patent
from .source_integrations import (
    SourceManager,
    SourceContext,
    SourceFile,
    LocalFolderScanner,
    GitHubIntegration,
    GoogleDriveIntegration,
    scan_local_folder,
    fetch_github_repo,
    fetch_gdrive_folder
)
from .image_generator import (
    PatentImageManager,
    KreaAIGenerator,
    PlaywrightCapture,
    GeneratedImage,
    generate_patent_figures
)
from .docx_generator import (
    DocxPatentGenerator,
    PatentDocument,
    PatentFigure,
    InventorInfo,
    generate_patent_docx
)
from .rubric_scorer import (
    RubricScorer,
    ScoringResult,
    score_patent
)
from .unified_pipeline import (
    UnifiedPatentPipeline,
    PipelineResult,
    run_patent_pipeline
)

__all__ = [
    'PriorArtSearcher',
    'search_prior_art',
    'find_white_space',
    'AIOrchestrator',
    'ClaudeProvider',
    'OpenAIProvider',
    'PerplexityProvider',
    'DiagramProvider',
    'YouTubeTranscriptProvider',
    'OpportunityFinder',
    'find_opportunities',
    'PatentDrafter',
    'draft_patent',
    'SourceManager',
    'SourceContext',
    'SourceFile',
    'LocalFolderScanner',
    'GitHubIntegration',
    'GoogleDriveIntegration',
    'scan_local_folder',
    'fetch_github_repo',
    'fetch_gdrive_folder',
    'PatentImageManager',
    'KreaAIGenerator',
    'PlaywrightCapture',
    'GeneratedImage',
    'generate_patent_figures',
    'DocxPatentGenerator',
    'PatentDocument',
    'PatentFigure',
    'InventorInfo',
    'generate_patent_docx',
    'RubricScorer',
    'ScoringResult',
    'score_patent',
    'UnifiedPatentPipeline',
    'PipelineResult',
    'run_patent_pipeline'
]
