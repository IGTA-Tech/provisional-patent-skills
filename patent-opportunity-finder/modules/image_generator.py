"""
Image Generator Module
======================
Generate patent diagrams and capture screenshots for patent applications.

Features:
- Krea AI / NanoBanana Pro for AI-generated patent diagrams
- Playwright for webpage and code screenshots
- Code-to-image conversion
- System architecture diagram generation
"""

import os
import json
import base64
import requests
import tempfile
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime


@dataclass
class GeneratedImage:
    """Represents a generated or captured image"""
    image_data: bytes  # Raw image bytes
    format: str  # png, jpg, svg
    width: int
    height: int
    source: str  # krea, playwright, code_render
    description: str
    filename: str


# =============================================================================
# KREA AI / NANOBANANA PRO IMAGE GENERATION
# =============================================================================

class KreaAIGenerator:
    """
    Generate patent diagrams using Krea AI or NanoBanana Pro.

    Krea AI: https://krea.ai
    - Supports text-to-image generation
    - Good for technical diagrams
    """

    # API endpoints
    KREA_API = "https://api.krea.ai/v1/generate"
    NANOBANANA_API = "https://api.nanobanana.com/v1/images/generate"

    def __init__(self, api_key: Optional[str] = None, provider: str = "krea"):
        self.api_key = api_key or os.getenv("KREA_API_KEY")
        self.provider = provider

    def generate_patent_diagram(
        self,
        description: str,
        diagram_type: str = "system_architecture",
        style: str = "technical_blueprint",
        size: Tuple[int, int] = (1024, 768)
    ) -> GeneratedImage:
        """
        Generate a patent-style technical diagram.

        Args:
            description: What the diagram should show
            diagram_type: system_architecture, flowchart, block_diagram, data_flow, ui_wireframe
            style: technical_blueprint, line_art, schematic, whiteboard
            size: (width, height) tuple

        Returns:
            GeneratedImage with the generated diagram
        """
        # Build optimized prompt for patent diagrams
        prompt = self._build_patent_prompt(description, diagram_type, style)

        if not self.api_key:
            # Return placeholder if no API key
            return self._generate_placeholder(description, diagram_type)

        try:
            if self.provider == "krea":
                return self._call_krea_api(prompt, size)
            else:
                return self._call_nanobanana_api(prompt, size)
        except Exception as e:
            print(f"Image generation error: {e}")
            return self._generate_placeholder(description, diagram_type)

    def _build_patent_prompt(self, description: str, diagram_type: str, style: str) -> str:
        """Build an optimized prompt for patent diagram generation"""

        type_prompts = {
            "system_architecture": "technical system architecture diagram showing components and connections",
            "flowchart": "detailed flowchart with decision diamonds, process rectangles, and directional arrows",
            "block_diagram": "hardware block diagram with labeled components and signal flows",
            "data_flow": "data flow diagram showing data transformations and storage",
            "ui_wireframe": "user interface wireframe with annotated elements",
            "network_diagram": "network topology diagram with nodes and connections",
            "sequence_diagram": "sequence diagram showing message flows between components"
        }

        style_prompts = {
            "technical_blueprint": "clean technical blueprint style, white background, black lines, professional engineering diagram",
            "line_art": "simple line art, minimal colors, clear labels, technical illustration",
            "schematic": "electronic schematic style, component symbols, wire connections",
            "whiteboard": "whiteboard sketch style, hand-drawn appearance, annotations"
        }

        diagram_desc = type_prompts.get(diagram_type, type_prompts["system_architecture"])
        style_desc = style_prompts.get(style, style_prompts["technical_blueprint"])

        prompt = f"""Create a {diagram_desc} for a patent application.

Subject: {description}

Style requirements:
- {style_desc}
- Include numbered labels (1, 2, 3...) for each component
- Add clear text annotations
- Use USPTO patent figure style
- Professional, clean, easily reproducible
- No gradients or complex shading
- High contrast for clear printing"""

        return prompt

    def _call_krea_api(self, prompt: str, size: Tuple[int, int]) -> GeneratedImage:
        """Call Krea AI API to generate image"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "prompt": prompt,
            "width": size[0],
            "height": size[1],
            "num_images": 1,
            "style": "technical"
        }

        response = requests.post(self.KREA_API, json=payload, headers=headers, timeout=60)

        if response.status_code == 200:
            data = response.json()
            # Handle various response formats
            if "images" in data:
                image_url = data["images"][0].get("url") or data["images"][0].get("base64")
            elif "image_url" in data:
                image_url = data["image_url"]
            elif "data" in data:
                image_url = data["data"][0].get("url")
            else:
                raise ValueError(f"Unexpected response format: {data.keys()}")

            # Download image if URL, or decode if base64
            if image_url.startswith("http"):
                img_response = requests.get(image_url)
                image_data = img_response.content
            else:
                image_data = base64.b64decode(image_url)

            return GeneratedImage(
                image_data=image_data,
                format="png",
                width=size[0],
                height=size[1],
                source="krea",
                description=prompt[:100],
                filename=f"patent_diagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
        else:
            raise Exception(f"Krea API error: {response.status_code} - {response.text}")

    def _call_nanobanana_api(self, prompt: str, size: Tuple[int, int]) -> GeneratedImage:
        """Call NanoBanana Pro API to generate image"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "prompt": prompt,
            "width": size[0],
            "height": size[1],
            "model": "nanobanana-pro"
        }

        response = requests.post(self.NANOBANANA_API, json=payload, headers=headers, timeout=60)

        if response.status_code == 200:
            data = response.json()
            image_data = base64.b64decode(data.get("image") or data.get("data", [{}])[0].get("b64_json", ""))

            return GeneratedImage(
                image_data=image_data,
                format="png",
                width=size[0],
                height=size[1],
                source="nanobanana",
                description=prompt[:100],
                filename=f"patent_diagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
        else:
            raise Exception(f"NanoBanana API error: {response.status_code}")

    def _generate_placeholder(self, description: str, diagram_type: str) -> GeneratedImage:
        """Generate a placeholder SVG diagram when API is not available"""

        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="white"/>
  <rect x="10" y="10" width="780" height="580" fill="none" stroke="black" stroke-width="2"/>

  <!-- Title -->
  <text x="400" y="40" text-anchor="middle" font-family="Arial" font-size="16" font-weight="bold">
    FIG. 1 - {diagram_type.upper().replace('_', ' ')}
  </text>

  <!-- Main box -->
  <rect x="250" y="80" width="300" height="150" fill="none" stroke="black" stroke-width="1"/>
  <text x="400" y="160" text-anchor="middle" font-family="Arial" font-size="12">
    {description[:50]}...
  </text>
  <text x="230" y="90" font-family="Arial" font-size="10">100</text>

  <!-- Input -->
  <rect x="50" y="130" width="120" height="50" fill="none" stroke="black" stroke-width="1"/>
  <text x="110" y="160" text-anchor="middle" font-family="Arial" font-size="10">INPUT</text>
  <text x="35" y="140" font-family="Arial" font-size="10">101</text>
  <line x1="170" y1="155" x2="250" y2="155" stroke="black" stroke-width="1" marker-end="url(#arrow)"/>

  <!-- Output -->
  <rect x="630" y="130" width="120" height="50" fill="none" stroke="black" stroke-width="1"/>
  <text x="690" y="160" text-anchor="middle" font-family="Arial" font-size="10">OUTPUT</text>
  <text x="615" y="140" font-family="Arial" font-size="10">102</text>
  <line x1="550" y1="155" x2="630" y2="155" stroke="black" stroke-width="1" marker-end="url(#arrow)"/>

  <!-- Processing blocks -->
  <rect x="150" y="300" width="150" height="80" fill="none" stroke="black" stroke-width="1"/>
  <text x="225" y="345" text-anchor="middle" font-family="Arial" font-size="10">PROCESSOR</text>
  <text x="135" y="310" font-family="Arial" font-size="10">103</text>

  <rect x="500" y="300" width="150" height="80" fill="none" stroke="black" stroke-width="1"/>
  <text x="575" y="345" text-anchor="middle" font-family="Arial" font-size="10">MEMORY</text>
  <text x="485" y="310" font-family="Arial" font-size="10">104</text>

  <!-- Connections -->
  <line x1="400" y1="230" x2="225" y2="300" stroke="black" stroke-width="1"/>
  <line x1="400" y1="230" x2="575" y2="300" stroke="black" stroke-width="1"/>
  <line x1="300" y1="340" x2="500" y2="340" stroke="black" stroke-width="1" stroke-dasharray="5,5"/>

  <!-- Legend -->
  <text x="50" y="500" font-family="Arial" font-size="10">100 - Main Processing Unit</text>
  <text x="50" y="515" font-family="Arial" font-size="10">101 - Input Interface</text>
  <text x="50" y="530" font-family="Arial" font-size="10">102 - Output Interface</text>
  <text x="50" y="545" font-family="Arial" font-size="10">103 - Processing Module</text>
  <text x="50" y="560" font-family="Arial" font-size="10">104 - Memory Storage</text>

  <!-- Note -->
  <text x="400" y="580" text-anchor="middle" font-family="Arial" font-size="9" fill="gray">
    [Placeholder - Configure KREA_API_KEY for AI-generated diagrams]
  </text>

  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="black"/>
    </marker>
  </defs>
</svg>'''

        return GeneratedImage(
            image_data=svg_content.encode('utf-8'),
            format="svg",
            width=800,
            height=600,
            source="placeholder",
            description=description,
            filename=f"patent_diagram_placeholder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.svg"
        )


# =============================================================================
# PLAYWRIGHT SCREENSHOT CAPTURE
# =============================================================================

class PlaywrightCapture:
    """
    Capture screenshots of webpages and render code using Playwright.

    Requires: pip install playwright && playwright install chromium
    """

    def __init__(self):
        self.browser = None
        self.playwright = None
        self._initialized = False

    def _ensure_initialized(self):
        """Lazily initialize Playwright"""
        if self._initialized:
            return True

        try:
            from playwright.sync_api import sync_playwright
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=True)
            self._initialized = True
            return True
        except ImportError:
            print("Playwright not installed. Run: pip install playwright && playwright install chromium")
            return False
        except Exception as e:
            print(f"Playwright initialization error: {e}")
            return False

    def capture_webpage(
        self,
        url: str,
        full_page: bool = False,
        width: int = 1280,
        height: int = 720,
        wait_for: Optional[str] = None
    ) -> Optional[GeneratedImage]:
        """
        Capture a screenshot of a webpage.

        Args:
            url: URL to capture
            full_page: Capture entire scrollable page
            width: Viewport width
            height: Viewport height
            wait_for: CSS selector to wait for before capturing

        Returns:
            GeneratedImage with the screenshot
        """
        if not self._ensure_initialized():
            return None

        try:
            page = self.browser.new_page(viewport={"width": width, "height": height})
            page.goto(url, wait_until="networkidle")

            if wait_for:
                page.wait_for_selector(wait_for, timeout=10000)

            screenshot = page.screenshot(full_page=full_page, type="png")
            page.close()

            return GeneratedImage(
                image_data=screenshot,
                format="png",
                width=width,
                height=height,
                source="playwright",
                description=f"Screenshot of {url}",
                filename=f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
        except Exception as e:
            print(f"Screenshot capture error: {e}")
            return None

    def capture_code_as_image(
        self,
        code: str,
        language: str = "python",
        theme: str = "github-dark",
        font_size: int = 14,
        line_numbers: bool = True
    ) -> Optional[GeneratedImage]:
        """
        Render code as a syntax-highlighted image.

        Args:
            code: Source code to render
            language: Programming language for syntax highlighting
            theme: Color theme (github-dark, monokai, vs-light, dracula)
            font_size: Font size in pixels
            line_numbers: Show line numbers

        Returns:
            GeneratedImage with the rendered code
        """
        if not self._ensure_initialized():
            return None

        # Build HTML with syntax highlighting
        html_content = self._build_code_html(code, language, theme, font_size, line_numbers)

        try:
            page = self.browser.new_page()
            page.set_content(html_content)

            # Wait for highlight.js to process
            page.wait_for_timeout(500)

            # Get the code block dimensions
            code_element = page.query_selector("pre")
            box = code_element.bounding_box()

            # Capture just the code block with some padding
            screenshot = page.screenshot(
                clip={
                    "x": max(0, box["x"] - 10),
                    "y": max(0, box["y"] - 10),
                    "width": box["width"] + 20,
                    "height": box["height"] + 20
                },
                type="png"
            )
            page.close()

            return GeneratedImage(
                image_data=screenshot,
                format="png",
                width=int(box["width"] + 20),
                height=int(box["height"] + 20),
                source="code_render",
                description=f"{language} code snippet",
                filename=f"code_{language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
        except Exception as e:
            print(f"Code rendering error: {e}")
            return None

    def capture_github_repo(
        self,
        repo_url: str,
        capture_readme: bool = True,
        capture_files: List[str] = None
    ) -> List[GeneratedImage]:
        """
        Capture screenshots from a GitHub repository.

        Args:
            repo_url: GitHub repository URL
            capture_readme: Capture the README
            capture_files: List of file paths to capture (e.g., ["src/main.py"])

        Returns:
            List of GeneratedImage objects
        """
        images = []

        if capture_readme:
            img = self.capture_webpage(repo_url, full_page=False)
            if img:
                img.description = f"GitHub repo: {repo_url}"
                images.append(img)

        if capture_files:
            for file_path in capture_files:
                file_url = f"{repo_url}/blob/main/{file_path}"
                img = self.capture_webpage(file_url, full_page=True)
                if img:
                    img.description = f"GitHub file: {file_path}"
                    images.append(img)

        return images

    def _build_code_html(
        self,
        code: str,
        language: str,
        theme: str,
        font_size: int,
        line_numbers: bool
    ) -> str:
        """Build HTML page for code rendering"""

        # Escape HTML characters in code
        import html
        escaped_code = html.escape(code)

        # Add line numbers if requested
        if line_numbers:
            lines = escaped_code.split('\n')
            numbered_lines = []
            for i, line in enumerate(lines, 1):
                numbered_lines.append(f'<span class="line-number">{i:4d}</span>  {line}')
            escaped_code = '\n'.join(numbered_lines)

        return f'''<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/{theme}.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background: #1e1e1e;
        }}
        pre {{
            margin: 0;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
            font-size: {font_size}px;
            line-height: 1.5;
            overflow: visible;
            white-space: pre;
        }}
        .line-number {{
            color: #6e7681;
            user-select: none;
        }}
        code {{
            font-family: inherit;
        }}
    </style>
</head>
<body>
    <pre><code class="language-{language}">{escaped_code}</code></pre>
    <script>hljs.highlightAll();</script>
</body>
</html>'''

    def close(self):
        """Clean up Playwright resources"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self._initialized = False


# =============================================================================
# UNIFIED IMAGE MANAGER
# =============================================================================

class PatentImageManager:
    """
    Unified interface for all patent image generation needs.
    """

    def __init__(self, krea_api_key: Optional[str] = None):
        self.krea = KreaAIGenerator(krea_api_key)
        self.playwright = PlaywrightCapture()
        self.generated_images: List[GeneratedImage] = []

    def generate_system_diagram(self, description: str) -> GeneratedImage:
        """Generate a system architecture diagram"""
        img = self.krea.generate_patent_diagram(
            description,
            diagram_type="system_architecture",
            style="technical_blueprint"
        )
        self.generated_images.append(img)
        return img

    def generate_flowchart(self, description: str) -> GeneratedImage:
        """Generate a process flowchart"""
        img = self.krea.generate_patent_diagram(
            description,
            diagram_type="flowchart",
            style="line_art"
        )
        self.generated_images.append(img)
        return img

    def generate_block_diagram(self, description: str) -> GeneratedImage:
        """Generate a hardware block diagram"""
        img = self.krea.generate_patent_diagram(
            description,
            diagram_type="block_diagram",
            style="schematic"
        )
        self.generated_images.append(img)
        return img

    def capture_reference_webpage(self, url: str) -> Optional[GeneratedImage]:
        """Capture a webpage for reference"""
        img = self.playwright.capture_webpage(url)
        if img:
            self.generated_images.append(img)
        return img

    def capture_code_snippet(self, code: str, language: str = "python") -> Optional[GeneratedImage]:
        """Render code as an image"""
        img = self.playwright.capture_code_as_image(code, language)
        if img:
            self.generated_images.append(img)
        return img

    def capture_github_context(self, repo_url: str, files: List[str] = None) -> List[GeneratedImage]:
        """Capture GitHub repo screenshots"""
        images = self.playwright.capture_github_repo(repo_url, capture_files=files)
        self.generated_images.extend(images)
        return images

    def save_all_images(self, output_dir: str) -> List[str]:
        """Save all generated images to a directory"""
        os.makedirs(output_dir, exist_ok=True)
        saved_paths = []

        for i, img in enumerate(self.generated_images, 1):
            filename = f"FIG_{i}_{img.filename}"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(img.image_data)

            saved_paths.append(filepath)

        return saved_paths

    def get_figure_descriptions(self) -> str:
        """Get brief description of drawings section for patent"""
        if not self.generated_images:
            return "No figures generated."

        descriptions = ["BRIEF DESCRIPTION OF THE DRAWINGS\n"]
        for i, img in enumerate(self.generated_images, 1):
            descriptions.append(f"FIG. {i} is a {img.source} showing {img.description}.")

        return "\n".join(descriptions)

    def close(self):
        """Clean up resources"""
        self.playwright.close()


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def generate_patent_figures(
    invention_description: str,
    code_snippets: List[Dict] = None,
    reference_urls: List[str] = None,
    krea_api_key: Optional[str] = None
) -> Tuple[List[GeneratedImage], str]:
    """
    Generate all figures needed for a patent application.

    Args:
        invention_description: Description of the invention
        code_snippets: List of {"code": str, "language": str} dicts
        reference_urls: List of URLs to capture
        krea_api_key: API key for Krea AI

    Returns:
        Tuple of (list of images, brief description of drawings text)
    """
    manager = PatentImageManager(krea_api_key)

    # Generate standard diagrams
    manager.generate_system_diagram(invention_description)
    manager.generate_flowchart(f"Process flow for {invention_description}")
    manager.generate_block_diagram(f"Hardware implementation of {invention_description}")

    # Capture code snippets
    if code_snippets:
        for snippet in code_snippets:
            manager.capture_code_snippet(
                snippet.get("code", ""),
                snippet.get("language", "python")
            )

    # Capture reference webpages
    if reference_urls:
        for url in reference_urls:
            manager.capture_reference_webpage(url)

    description = manager.get_figure_descriptions()
    images = manager.generated_images

    manager.close()

    return images, description


if __name__ == "__main__":
    print("Testing Patent Image Generator...")

    # Test Krea placeholder
    krea = KreaAIGenerator()
    img = krea.generate_patent_diagram(
        "Machine learning inference optimization system",
        diagram_type="system_architecture"
    )
    print(f"Generated: {img.filename} ({img.source})")

    # Save test image
    with open("/tmp/test_patent_diagram.svg", "wb") as f:
        f.write(img.image_data)
    print("Saved to /tmp/test_patent_diagram.svg")
