"""
Source Integrations Module
==========================
Connect to local folders, GitHub repositories, and Google Drive folders
to gather context for patent analysis and drafting.
"""

import os
import json
import requests
import subprocess
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import tempfile
import shutil


@dataclass
class SourceFile:
    """Represents a file from any source"""
    path: str
    name: str
    content: str
    source_type: str  # local, github, gdrive
    size: int
    language: Optional[str] = None


@dataclass
class SourceContext:
    """Complete context gathered from sources"""
    source_name: str
    source_type: str
    files: List[SourceFile]
    total_files: int
    total_size: int
    summary: str
    structure: Dict


# =============================================================================
# LOCAL FOLDER INTEGRATION
# =============================================================================

class LocalFolderScanner:
    """Scan local folders for relevant files"""

    # File extensions to include
    CODE_EXTENSIONS = {
        '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c', '.h',
        '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala',
        '.r', '.R', '.m', '.mm', '.sql', '.sh', '.bash', '.ps1'
    }

    DOC_EXTENSIONS = {
        '.md', '.txt', '.rst', '.doc', '.docx', '.pdf', '.tex', '.rtf'
    }

    CONFIG_EXTENSIONS = {
        '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.xml'
    }

    # Folders to skip
    SKIP_FOLDERS = {
        'node_modules', '__pycache__', '.git', '.svn', 'venv', 'env',
        '.env', 'dist', 'build', '.next', '.cache', 'coverage',
        '.idea', '.vscode', 'vendor', 'target', 'bin', 'obj'
    }

    # Max file size to read (500KB)
    MAX_FILE_SIZE = 500 * 1024

    def __init__(self, include_code: bool = True, include_docs: bool = True,
                 include_config: bool = True):
        self.extensions = set()
        if include_code:
            self.extensions.update(self.CODE_EXTENSIONS)
        if include_docs:
            self.extensions.update(self.DOC_EXTENSIONS)
        if include_config:
            self.extensions.update(self.CONFIG_EXTENSIONS)

    def scan_folder(self, folder_path: str, max_files: int = 100) -> SourceContext:
        """Scan a local folder and return context"""
        folder_path = os.path.expanduser(folder_path)

        if not os.path.exists(folder_path):
            raise ValueError(f"Folder does not exist: {folder_path}")

        files = []
        structure = {"folders": [], "files": []}
        total_size = 0

        for root, dirs, filenames in os.walk(folder_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.SKIP_FOLDERS]

            rel_root = os.path.relpath(root, folder_path)
            if rel_root != '.':
                structure["folders"].append(rel_root)

            for filename in filenames:
                if len(files) >= max_files:
                    break

                ext = os.path.splitext(filename)[1].lower()
                if ext not in self.extensions:
                    continue

                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, folder_path)

                try:
                    size = os.path.getsize(filepath)
                    if size > self.MAX_FILE_SIZE:
                        continue

                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    files.append(SourceFile(
                        path=rel_path,
                        name=filename,
                        content=content,
                        source_type="local",
                        size=size,
                        language=self._detect_language(ext)
                    ))

                    structure["files"].append(rel_path)
                    total_size += size

                except Exception as e:
                    continue

        summary = self._generate_summary(folder_path, files, structure)

        return SourceContext(
            source_name=os.path.basename(folder_path),
            source_type="local",
            files=files,
            total_files=len(files),
            total_size=total_size,
            summary=summary,
            structure=structure
        )

    def _detect_language(self, ext: str) -> str:
        """Detect programming language from extension"""
        lang_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.tsx': 'TypeScript/React', '.jsx': 'JavaScript/React',
            '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.h': 'C/C++ Header',
            '.cs': 'C#', '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby',
            '.php': 'PHP', '.swift': 'Swift', '.kt': 'Kotlin',
            '.scala': 'Scala', '.r': 'R', '.R': 'R', '.sql': 'SQL',
            '.sh': 'Shell', '.bash': 'Bash', '.ps1': 'PowerShell',
            '.md': 'Markdown', '.json': 'JSON', '.yaml': 'YAML',
            '.yml': 'YAML', '.xml': 'XML', '.toml': 'TOML'
        }
        return lang_map.get(ext, 'Unknown')

    def _generate_summary(self, folder_path: str, files: List[SourceFile],
                          structure: Dict) -> str:
        """Generate a summary of the folder contents"""
        lang_counts = {}
        for f in files:
            lang = f.language or 'Unknown'
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

        summary = f"Local folder: {folder_path}\n"
        summary += f"Total files scanned: {len(files)}\n"
        summary += f"Total folders: {len(structure['folders'])}\n\n"
        summary += "Languages found:\n"
        for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1]):
            summary += f"  - {lang}: {count} files\n"

        return summary


# =============================================================================
# GITHUB INTEGRATION
# =============================================================================

class GitHubIntegration:
    """Fetch and analyze GitHub repositories"""

    API_BASE = "https://api.github.com"

    # File extensions to fetch
    FETCH_EXTENSIONS = {
        '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c', '.h',
        '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.md', '.txt',
        '.json', '.yaml', '.yml', '.toml'
    }

    MAX_FILE_SIZE = 500 * 1024  # 500KB

    def __init__(self, github_token: Optional[str] = None):
        self.token = github_token
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def fetch_repo(self, repo_url: str, max_files: int = 100,
                   branch: str = "main") -> SourceContext:
        """
        Fetch a GitHub repository

        Args:
            repo_url: GitHub URL (e.g., https://github.com/owner/repo)
            max_files: Maximum files to fetch
            branch: Branch to fetch from
        """
        # Parse repo URL
        owner, repo = self._parse_repo_url(repo_url)

        # Get repo info
        repo_info = self._get_repo_info(owner, repo)
        default_branch = repo_info.get('default_branch', branch)

        # Get file tree
        tree = self._get_tree(owner, repo, default_branch)

        # Fetch relevant files
        files = []
        structure = {"folders": set(), "files": []}
        total_size = 0

        for item in tree.get('tree', []):
            if len(files) >= max_files:
                break

            if item['type'] == 'tree':
                structure["folders"].add(item['path'])
                continue

            if item['type'] != 'blob':
                continue

            # Check extension
            ext = os.path.splitext(item['path'])[1].lower()
            if ext not in self.FETCH_EXTENSIONS:
                continue

            # Check size
            size = item.get('size', 0)
            if size > self.MAX_FILE_SIZE:
                continue

            # Fetch content
            try:
                content = self._get_file_content(owner, repo, item['path'], default_branch)

                files.append(SourceFile(
                    path=item['path'],
                    name=os.path.basename(item['path']),
                    content=content,
                    source_type="github",
                    size=size,
                    language=self._detect_language(ext)
                ))

                structure["files"].append(item['path'])
                total_size += size

            except Exception as e:
                continue

        structure["folders"] = list(structure["folders"])
        summary = self._generate_summary(repo_url, repo_info, files, structure)

        return SourceContext(
            source_name=f"{owner}/{repo}",
            source_type="github",
            files=files,
            total_files=len(files),
            total_size=total_size,
            summary=summary,
            structure=structure
        )

    def _parse_repo_url(self, url: str) -> Tuple[str, str]:
        """Parse GitHub URL to get owner and repo"""
        # Handle various URL formats
        url = url.rstrip('/')

        if 'github.com' in url:
            parts = url.split('github.com/')[-1].split('/')
            if len(parts) >= 2:
                return parts[0], parts[1].replace('.git', '')

        # Assume format owner/repo
        parts = url.split('/')
        if len(parts) >= 2:
            return parts[-2], parts[-1].replace('.git', '')

        raise ValueError(f"Could not parse GitHub URL: {url}")

    def _get_repo_info(self, owner: str, repo: str) -> Dict:
        """Get repository information"""
        url = f"{self.API_BASE}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def _get_tree(self, owner: str, repo: str, branch: str) -> Dict:
        """Get repository file tree"""
        url = f"{self.API_BASE}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def _get_file_content(self, owner: str, repo: str, path: str, branch: str) -> str:
        """Get file content from repository"""
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def _detect_language(self, ext: str) -> str:
        """Detect programming language from extension"""
        lang_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.tsx': 'TypeScript/React', '.jsx': 'JavaScript/React',
            '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.h': 'C/C++ Header',
            '.cs': 'C#', '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby',
            '.php': 'PHP', '.swift': 'Swift', '.kt': 'Kotlin',
            '.md': 'Markdown', '.json': 'JSON', '.yaml': 'YAML',
            '.yml': 'YAML', '.toml': 'TOML'
        }
        return lang_map.get(ext, 'Unknown')

    def _generate_summary(self, repo_url: str, repo_info: Dict,
                          files: List[SourceFile], structure: Dict) -> str:
        """Generate summary of repository"""
        lang_counts = {}
        for f in files:
            lang = f.language or 'Unknown'
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

        summary = f"GitHub Repository: {repo_url}\n"
        summary += f"Description: {repo_info.get('description', 'N/A')}\n"
        summary += f"Stars: {repo_info.get('stargazers_count', 0)}\n"
        summary += f"Language: {repo_info.get('language', 'N/A')}\n"
        summary += f"Total files fetched: {len(files)}\n\n"
        summary += "File types found:\n"
        for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1]):
            summary += f"  - {lang}: {count} files\n"

        return summary

    def clone_repo(self, repo_url: str, target_dir: Optional[str] = None) -> str:
        """Clone repository to local directory"""
        if target_dir is None:
            target_dir = tempfile.mkdtemp()

        subprocess.run(['git', 'clone', '--depth', '1', repo_url, target_dir],
                      check=True, capture_output=True)
        return target_dir


# =============================================================================
# GOOGLE DRIVE INTEGRATION
# =============================================================================

class GoogleDriveIntegration:
    """
    Fetch files from Google Drive folders.
    Requires a service account or OAuth credentials.
    """

    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

    # Supported MIME types
    SUPPORTED_MIMES = {
        'application/pdf': '.pdf',
        'text/plain': '.txt',
        'text/markdown': '.md',
        'application/json': '.json',
        'text/csv': '.csv',
        'application/vnd.google-apps.document': '.gdoc',
        'application/vnd.google-apps.spreadsheet': '.gsheet',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
    }

    def __init__(self, credentials_path: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize Google Drive integration.

        Args:
            credentials_path: Path to service account JSON or OAuth credentials
            api_key: Google API key (limited functionality)
        """
        self.credentials_path = credentials_path
        self.api_key = api_key
        self.service = None

        if credentials_path and os.path.exists(credentials_path):
            self._init_service()

    def _init_service(self):
        """Initialize Google Drive API service"""
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build

            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path, scopes=self.SCOPES
            )
            self.service = build('drive', 'v3', credentials=credentials)
        except ImportError:
            raise ImportError(
                "Google Drive integration requires: "
                "pip install google-api-python-client google-auth"
            )
        except Exception as e:
            raise ValueError(f"Failed to initialize Google Drive: {e}")

    def fetch_folder(self, folder_id: str, max_files: int = 100) -> SourceContext:
        """
        Fetch files from a Google Drive folder.

        Args:
            folder_id: Google Drive folder ID (from URL)
            max_files: Maximum number of files to fetch
        """
        if not self.service:
            # Return placeholder if not configured
            return SourceContext(
                source_name=f"gdrive:{folder_id}",
                source_type="gdrive",
                files=[],
                total_files=0,
                total_size=0,
                summary="Google Drive not configured. Add credentials to enable.",
                structure={"folders": [], "files": []}
            )

        files = []
        structure = {"folders": [], "files": []}
        total_size = 0

        # List files in folder
        results = self.service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=max_files,
            fields="files(id, name, mimeType, size)"
        ).execute()

        items = results.get('files', [])

        for item in items:
            if len(files) >= max_files:
                break

            mime_type = item.get('mimeType', '')

            # Handle folders recursively
            if mime_type == 'application/vnd.google-apps.folder':
                structure["folders"].append(item['name'])
                continue

            # Skip unsupported types
            if mime_type not in self.SUPPORTED_MIMES:
                continue

            try:
                content = self._get_file_content(item['id'], mime_type)
                size = int(item.get('size', len(content)))

                files.append(SourceFile(
                    path=item['name'],
                    name=item['name'],
                    content=content,
                    source_type="gdrive",
                    size=size,
                    language=self._detect_type(mime_type)
                ))

                structure["files"].append(item['name'])
                total_size += size

            except Exception as e:
                continue

        summary = self._generate_summary(folder_id, files, structure)

        return SourceContext(
            source_name=f"gdrive:{folder_id}",
            source_type="gdrive",
            files=files,
            total_files=len(files),
            total_size=total_size,
            summary=summary,
            structure=structure
        )

    def _get_file_content(self, file_id: str, mime_type: str) -> str:
        """Get file content from Google Drive"""
        if mime_type.startswith('application/vnd.google-apps'):
            # Export Google Docs/Sheets as text
            export_mime = 'text/plain'
            if 'spreadsheet' in mime_type:
                export_mime = 'text/csv'

            content = self.service.files().export(
                fileId=file_id, mimeType=export_mime
            ).execute()
            return content.decode('utf-8')
        else:
            # Download regular files
            content = self.service.files().get_media(fileId=file_id).execute()
            return content.decode('utf-8', errors='ignore')

    def _detect_type(self, mime_type: str) -> str:
        """Detect file type from MIME type"""
        type_map = {
            'application/pdf': 'PDF',
            'text/plain': 'Text',
            'text/markdown': 'Markdown',
            'application/json': 'JSON',
            'text/csv': 'CSV',
            'application/vnd.google-apps.document': 'Google Doc',
            'application/vnd.google-apps.spreadsheet': 'Google Sheet',
        }
        return type_map.get(mime_type, 'Unknown')

    def _generate_summary(self, folder_id: str, files: List[SourceFile],
                          structure: Dict) -> str:
        """Generate summary of Google Drive folder"""
        type_counts = {}
        for f in files:
            ftype = f.language or 'Unknown'
            type_counts[ftype] = type_counts.get(ftype, 0) + 1

        summary = f"Google Drive Folder: {folder_id}\n"
        summary += f"Total files fetched: {len(files)}\n"
        summary += f"Subfolders found: {len(structure['folders'])}\n\n"
        summary += "File types found:\n"
        for ftype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            summary += f"  - {ftype}: {count} files\n"

        return summary

    @staticmethod
    def extract_folder_id(url: str) -> str:
        """Extract folder ID from Google Drive URL"""
        # Handle various URL formats
        if 'folders/' in url:
            return url.split('folders/')[-1].split('?')[0].split('/')[0]
        if 'id=' in url:
            return url.split('id=')[-1].split('&')[0]
        # Assume it's already the ID
        return url


# =============================================================================
# UNIFIED SOURCE MANAGER
# =============================================================================

class SourceManager:
    """Unified interface for all source types"""

    def __init__(self, github_token: Optional[str] = None,
                 gdrive_credentials: Optional[str] = None):
        self.local_scanner = LocalFolderScanner()
        self.github = GitHubIntegration(github_token)
        self.gdrive = GoogleDriveIntegration(gdrive_credentials)

    def load_source(self, source: str, source_type: str = "auto",
                    max_files: int = 100) -> SourceContext:
        """
        Load context from any source.

        Args:
            source: Path, URL, or ID of the source
            source_type: "local", "github", "gdrive", or "auto" to detect
            max_files: Maximum files to load
        """
        if source_type == "auto":
            source_type = self._detect_source_type(source)

        if source_type == "local":
            return self.local_scanner.scan_folder(source, max_files)
        elif source_type == "github":
            return self.github.fetch_repo(source, max_files)
        elif source_type == "gdrive":
            folder_id = GoogleDriveIntegration.extract_folder_id(source)
            return self.gdrive.fetch_folder(folder_id, max_files)
        else:
            raise ValueError(f"Unknown source type: {source_type}")

    def _detect_source_type(self, source: str) -> str:
        """Auto-detect source type from input"""
        if 'github.com' in source or source.count('/') == 1:
            return "github"
        elif 'drive.google.com' in source or 'docs.google.com' in source:
            return "gdrive"
        elif os.path.exists(os.path.expanduser(source)):
            return "local"
        else:
            # Try as GitHub owner/repo format
            if '/' in source and not source.startswith('/'):
                return "github"
            return "local"

    def get_combined_context(self, sources: List[Dict]) -> str:
        """
        Get combined context from multiple sources.

        Args:
            sources: List of dicts with 'source' and optionally 'type' keys

        Returns:
            Combined context string for AI processing
        """
        contexts = []

        for src in sources:
            try:
                ctx = self.load_source(
                    src['source'],
                    src.get('type', 'auto'),
                    src.get('max_files', 50)
                )
                contexts.append(ctx)
            except Exception as e:
                contexts.append(SourceContext(
                    source_name=src['source'],
                    source_type="error",
                    files=[],
                    total_files=0,
                    total_size=0,
                    summary=f"Error loading source: {e}",
                    structure={}
                ))

        # Build combined context string
        combined = "# Source Context\n\n"

        for ctx in contexts:
            combined += f"## {ctx.source_type.upper()}: {ctx.source_name}\n\n"
            combined += f"{ctx.summary}\n\n"

            # Add key files content
            combined += "### Key Files:\n\n"
            for f in ctx.files[:20]:  # Limit to 20 files per source
                combined += f"#### {f.path}\n"
                combined += f"```{f.language.lower() if f.language else ''}\n"
                # Truncate very long files
                content = f.content[:10000] if len(f.content) > 10000 else f.content
                combined += content
                combined += "\n```\n\n"

        return combined

    def export_context_to_json(self, sources: List[Dict], output_path: str):
        """Export source context to JSON file"""
        contexts = []

        for src in sources:
            try:
                ctx = self.load_source(src['source'], src.get('type', 'auto'))
                contexts.append({
                    'source_name': ctx.source_name,
                    'source_type': ctx.source_type,
                    'total_files': ctx.total_files,
                    'total_size': ctx.total_size,
                    'summary': ctx.summary,
                    'structure': ctx.structure,
                    'files': [
                        {
                            'path': f.path,
                            'name': f.name,
                            'language': f.language,
                            'size': f.size,
                            'content': f.content[:5000]  # Truncate for JSON
                        }
                        for f in ctx.files
                    ]
                })
            except Exception as e:
                contexts.append({
                    'source_name': src['source'],
                    'error': str(e)
                })

        with open(output_path, 'w') as f:
            json.dump(contexts, f, indent=2)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def scan_local_folder(path: str, max_files: int = 100) -> SourceContext:
    """Convenience function to scan a local folder"""
    scanner = LocalFolderScanner()
    return scanner.scan_folder(path, max_files)


def fetch_github_repo(repo_url: str, token: Optional[str] = None,
                      max_files: int = 100) -> SourceContext:
    """Convenience function to fetch a GitHub repository"""
    github = GitHubIntegration(token)
    return github.fetch_repo(repo_url, max_files)


def fetch_gdrive_folder(folder_id: str, credentials_path: Optional[str] = None,
                        max_files: int = 100) -> SourceContext:
    """Convenience function to fetch a Google Drive folder"""
    gdrive = GoogleDriveIntegration(credentials_path)
    return gdrive.fetch_folder(folder_id, max_files)


if __name__ == "__main__":
    # Test local folder scanning
    print("Testing Local Folder Scanner...")
    scanner = LocalFolderScanner()

    # Test with current directory
    ctx = scanner.scan_folder(".")
    print(ctx.summary)
    print(f"Files found: {[f.name for f in ctx.files[:5]]}")
