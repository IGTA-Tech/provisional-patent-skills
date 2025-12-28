"""
AI Providers Module
====================
Unified interface for Claude, OpenAI, Perplexity, and diagram generation APIs.
"""

import os
import requests
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class AIResponse:
    """Unified response from any AI provider"""
    content: str
    provider: str
    model: str
    usage: Dict[str, int]
    success: bool
    error: Optional[str] = None


class AIProvider(ABC):
    """Abstract base class for AI providers"""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> AIResponse:
        pass


class ClaudeProvider(AIProvider):
    """
    Anthropic Claude API Provider
    Uses native API calls (not SDK wrapper)
    """

    API_URL = "https://api.anthropic.com/v1/messages"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY required")

    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> AIResponse:
        """
        Generate response using Claude API

        Args:
            prompt: User message
            system_prompt: System instructions
            model: Model to use (claude-sonnet-4-20250514, claude-opus-4-20250514, etc.)
            max_tokens: Maximum tokens in response
            temperature: Creativity (0-1)
        """
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        messages = [{"role": "user", "content": prompt}]

        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages
        }

        if system_prompt:
            payload["system"] = system_prompt

        if temperature != 0.7:
            payload["temperature"] = temperature

        try:
            response = requests.post(self.API_URL, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()

            content = data["content"][0]["text"]
            usage = {
                "input_tokens": data.get("usage", {}).get("input_tokens", 0),
                "output_tokens": data.get("usage", {}).get("output_tokens", 0)
            }

            return AIResponse(
                content=content,
                provider="claude",
                model=model,
                usage=usage,
                success=True
            )

        except requests.exceptions.RequestException as e:
            return AIResponse(
                content="",
                provider="claude",
                model=model,
                usage={},
                success=False,
                error=str(e)
            )


class OpenAIProvider(AIProvider):
    """
    OpenAI API Provider
    """

    API_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY required")

    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        model: str = "gpt-4o",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> AIResponse:
        """Generate response using OpenAI API"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(self.API_URL, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()

            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})

            return AIResponse(
                content=content,
                provider="openai",
                model=model,
                usage=usage,
                success=True
            )

        except requests.exceptions.RequestException as e:
            return AIResponse(
                content="",
                provider="openai",
                model=model,
                usage={},
                success=False,
                error=str(e)
            )


class PerplexityProvider(AIProvider):
    """
    Perplexity API Provider
    Best for real-time research with citations
    """

    API_URL = "https://api.perplexity.ai/chat/completions"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY required")

    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        model: str = "sonar",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> AIResponse:
        """Generate response using Perplexity API (with web search)"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages
        }

        try:
            response = requests.post(self.API_URL, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()

            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})

            return AIResponse(
                content=content,
                provider="perplexity",
                model=model,
                usage=usage,
                success=True
            )

        except requests.exceptions.RequestException as e:
            return AIResponse(
                content="",
                provider="perplexity",
                model=model,
                usage={},
                success=False,
                error=str(e)
            )

    def research(self, topic: str) -> AIResponse:
        """Specialized research query with citations"""
        system = "You are a patent research expert. Provide detailed information with sources."
        return self.generate(topic, system_prompt=system)


class DiagramProvider:
    """
    Diagram/Artwork Generation Provider
    Placeholder for Napkin.ai, Krea.ai, or similar

    Set API key via: DIAGRAM_API_KEY environment variable
    """

    def __init__(self, api_key: str = None, provider: str = "napkin"):
        self.api_key = api_key or os.getenv("DIAGRAM_API_KEY")
        self.provider = provider

        # Provider endpoints (to be configured)
        self.endpoints = {
            "napkin": "https://api.napkin.ai/v1/generate",
            "krea": "https://api.krea.ai/v1/generate",
            "ideogram": "https://api.ideogram.ai/generate"
        }

    def generate_diagram(
        self,
        description: str,
        diagram_type: str = "flowchart",
        style: str = "technical"
    ) -> Dict[str, Any]:
        """
        Generate a patent diagram from text description

        Args:
            description: Text description of what to draw
            diagram_type: flowchart, system_diagram, block_diagram, ui_mockup
            style: technical, sketch, formal

        Returns:
            Dict with 'image_url', 'svg', or 'error'
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "DIAGRAM_API_KEY not set. Set environment variable or pass api_key.",
                "placeholder": self._generate_ascii_placeholder(description, diagram_type)
            }

        # Construct prompt for diagram generation
        prompt = f"""Generate a {diagram_type} diagram for a patent application.

Description: {description}

Style: {style}, clean lines, reference numbers (101, 102, etc.), suitable for USPTO filing.
"""

        # This is a placeholder - actual implementation depends on which API is used
        endpoint = self.endpoints.get(self.provider)

        if not endpoint:
            return {
                "success": False,
                "error": f"Unknown provider: {self.provider}",
                "placeholder": self._generate_ascii_placeholder(description, diagram_type)
            }

        # TODO: Implement actual API call when key is provided
        return {
            "success": False,
            "error": "API integration pending - provide API key and endpoint",
            "placeholder": self._generate_ascii_placeholder(description, diagram_type)
        }

    def _generate_ascii_placeholder(self, description: str, diagram_type: str) -> str:
        """Generate ASCII art placeholder for diagram"""

        if diagram_type == "flowchart":
            return """
┌─────────────────┐
│     START       │
│      300        │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Process Step   │
│      302        │
└────────┬────────┘
         │
         v
   ◇───────────◇
  ╱             ╲
 ╱   Decision    ╲
╱      304        ╲
◇─────────────────◇
│YES           NO│
v                v
┌──────┐    ┌──────┐
│ 306  │    │ 308  │
└──────┘    └──────┘
         │
         v
┌─────────────────┐
│      END        │
│      310        │
└─────────────────┘
"""
        elif diagram_type == "system_diagram":
            return """
┌─────────────────────────────────────────────────────┐
│                    SYSTEM 100                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────┐        ┌──────────┐        ┌────────┐│
│  │ Client   │───────>│  Server  │───────>│Database││
│  │   101    │  102   │   104    │  106   │  108   ││
│  └──────────┘        └──────────┘        └────────┘│
│       │                   │                        │
│       │              ┌────┴────┐                   │
│       └─────────────>│   ML    │                   │
│                      │  Engine │                   │
│                      │   110   │                   │
│                      └─────────┘                   │
│                                                     │
└─────────────────────────────────────────────────────┘
"""
        else:
            return f"""
┌─────────────────────────────────────┐
│         {diagram_type.upper():^25} │
│                                     │
│  [Placeholder for: {description[:20]}...]│
│                                     │
│  Reference numbers: 101, 102, 103   │
│                                     │
└─────────────────────────────────────┘
"""


class YouTubeTranscriptProvider:
    """
    Fetch transcripts from YouTube videos
    No API key required - uses youtube-transcript-api
    """

    def __init__(self):
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            self.api = YouTubeTranscriptApi()
            self.available = True
        except ImportError:
            self.available = False

    def get_transcript(self, video_id: str) -> Dict[str, Any]:
        """
        Get transcript from YouTube video

        Args:
            video_id: YouTube video ID (e.g., 'dQw4w9WgXcQ')

        Returns:
            Dict with 'transcript', 'success', 'error'
        """
        if not self.available:
            return {
                "success": False,
                "error": "youtube-transcript-api not installed. Run: pip install youtube-transcript-api"
            }

        try:
            transcript = self.api.fetch(video_id)
            full_text = ' '.join([entry.text for entry in transcript])

            return {
                "success": True,
                "transcript": full_text,
                "video_id": video_id,
                "url": f"https://youtube.com/watch?v={video_id}",
                "length": len(full_text)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_multiple(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """Get transcripts from multiple videos"""
        return [self.get_transcript(vid) for vid in video_ids]


class AIOrchestrator:
    """
    Orchestrates multiple AI providers for patent generation workflow
    """

    def __init__(
        self,
        claude_key: str = None,
        openai_key: str = None,
        perplexity_key: str = None,
        diagram_key: str = None
    ):
        self.providers = {}

        if claude_key or os.getenv("ANTHROPIC_API_KEY"):
            try:
                self.providers["claude"] = ClaudeProvider(claude_key)
            except ValueError:
                pass

        if openai_key or os.getenv("OPENAI_API_KEY"):
            try:
                self.providers["openai"] = OpenAIProvider(openai_key)
            except ValueError:
                pass

        if perplexity_key or os.getenv("PERPLEXITY_API_KEY"):
            try:
                self.providers["perplexity"] = PerplexityProvider(perplexity_key)
            except ValueError:
                pass

        self.diagram = DiagramProvider(diagram_key)
        self.youtube = YouTubeTranscriptProvider()

    def get_available_providers(self) -> List[str]:
        """Return list of configured providers"""
        return list(self.providers.keys())

    def generate(
        self,
        prompt: str,
        provider: str = "claude",
        system_prompt: str = None,
        **kwargs
    ) -> AIResponse:
        """Generate using specified provider"""
        if provider not in self.providers:
            available = self.get_available_providers()
            if not available:
                return AIResponse(
                    content="",
                    provider=provider,
                    model="",
                    usage={},
                    success=False,
                    error="No AI providers configured. Set API keys."
                )
            provider = available[0]

        return self.providers[provider].generate(prompt, system_prompt, **kwargs)

    def research(self, topic: str) -> AIResponse:
        """Use Perplexity for research (falls back to Claude)"""
        if "perplexity" in self.providers:
            return self.providers["perplexity"].research(topic)
        elif "claude" in self.providers:
            system = "You are a patent research expert. Provide detailed analysis."
            return self.providers["claude"].generate(topic, system)
        else:
            return AIResponse(
                content="",
                provider="none",
                model="",
                usage={},
                success=False,
                error="No research provider available"
            )


# Convenience functions
def get_orchestrator(**keys) -> AIOrchestrator:
    """Get configured AI orchestrator"""
    return AIOrchestrator(**keys)


if __name__ == "__main__":
    print("Testing AI Providers Module...")

    # Test YouTube (no key needed)
    yt = YouTubeTranscriptProvider()
    if yt.available:
        print("✓ YouTube Transcript API available")
    else:
        print("✗ YouTube Transcript API not installed")

    # Test diagram placeholder
    diag = DiagramProvider()
    result = diag.generate_diagram("ML inference pipeline", "flowchart")
    print("\n✓ Diagram placeholder generated:")
    print(result.get("placeholder", "")[:200])
