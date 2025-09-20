"""Utilities for generating narrative roll documentation."""

from __future__ import annotations

import textwrap
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class _ConfigurationSnippet:
    """Metadata describing a Compose override example for a roll."""

    title: str
    description: str
    service_id: str
    example_template: str

    def render(self) -> Dict[str, str]:
        """Render the snippet to a serialisable dictionary."""

        example = _render_example(self.example_template, self.service_id)
        return {
            "title": self.title,
            "description": self.description,
            "example": example,
        }


def _service_key(service_id: str) -> str:
    """Return the Docker Compose service key for ``service_id``."""

    return service_id.split(".")[-1]


def _render_example(template: str, service_id: str) -> str:
    """Format *template* with the Compose service key for *service_id*."""

    example = template.format(service_key=_service_key(service_id))
    return textwrap.dedent(example).rstrip()


class RollTemplateGenerator:
    """Generate metadata blocks for roll narrative documents."""

    def __init__(self, service_id: str) -> None:
        self.service_id = service_id

    def build(self) -> Dict[str, Any]:
        """Return the metadata dictionary for the configured roll."""

        return {
            "integration_notes": self._integration_metadata(),
        }

    # ------------------------------------------------------------------
    # Metadata helpers
    # ------------------------------------------------------------------
    def _integration_metadata(self) -> Dict[str, Any]:
        """Return integration metadata for the configured roll."""

        snippets = _CONFIGURATION_SNIPPETS.get(self.service_id, [])
        automation = _AUTOMATION_PATTERNS.get(self.service_id, [])

        rendered_snippets: List[Dict[str, str]] = [snippet.render() for snippet in snippets]
        return {
            "configuration_snippets": rendered_snippets,
            "automation_patterns": automation,
        }


_CONFIGURATION_SNIPPETS: Dict[str, List[_ConfigurationSnippet]] = {
    "hosomaki.n8n": [
        _ConfigurationSnippet(
            title="Connect n8n to Supabase for workflow state",
            description="Example environment overrides to target the managed Postgres shipped with Supabase",
            service_id="hosomaki.n8n",
            example_template="""\
            services:
              {service_key}:
                environment:
                  DB_POSTGRESDB_HOST: "supabase-db"
                  DB_POSTGRESDB_DATABASE: "${{N8N_DB_NAME:-n8n}}"
                  DB_POSTGRESDB_USER: "${{SUPABASE_SERVICE_ROLE_USER}}"
                  DB_POSTGRESDB_PASSWORD: "${{SUPABASE_SERVICE_ROLE_PASSWORD}}"
            """,
        ),
    ],
    "hosomaki.ollama": [
        _ConfigurationSnippet(
            title="Expose Ollama through LiteLLM",
            description="Route multi-model traffic via LiteLLM while keeping Ollama local",
            service_id="hosomaki.litellm",
            example_template="""\
            services:
              {service_key}:
                environment:
                  LITELLM_ROUTES: |
                    {{
                      "ollama-chat": {{
                        "host": "http://ollama:11434",
                        "model_list": ["llama3", "mistral"],
                        "api_key": "${{LITELLM_PROXY_KEY}}"
                      }}
                    }}
            """,
        ),
    ],
}


_AUTOMATION_PATTERNS: Dict[str, List[str]] = {
    "hosomaki.n8n": [
        "Use webhook triggers to hand off form submissions to `hosomaki.ollama` for summarization and routing",
        "Schedule nightly RAG ingestion workflows that enrich `futomaki.qdrant` with fresh embeddings",
    ],
    "hosomaki.ollama": [
        "Schedule nightly `ollama pull` updates via `hosomaki.n8n` to keep local models fresh",
        "Use `futomaki.qdrant` to store embeddings produced by Ollama for downstream semantic search",
    ],
}
