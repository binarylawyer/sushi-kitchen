"""Tests for the roll narrative template generator."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docs.manifest.narratives.rolls.generate_roll import RollTemplateGenerator


@pytest.mark.parametrize(
    ("roll_id", "expected_service_key", "unexpected_prefix"),
    [
        ("hosomaki.n8n", "n8n", "hosomaki.n8n:"),
        ("hosomaki.ollama", "litellm", "hosomaki.litellm:"),
    ],
)
def test_integration_snippet_uses_compose_service_key(
    roll_id: str, expected_service_key: str, unexpected_prefix: str
) -> None:
    """Ensure configuration snippets render Docker Compose keys correctly."""

    generator = RollTemplateGenerator(roll_id)
    integration_notes = generator._integration_metadata()

    snippets = integration_notes["configuration_snippets"]
    assert snippets, "Expected at least one configuration snippet"

    example = snippets[0]["example"]
    assert f"  {expected_service_key}:" in example
    assert unexpected_prefix not in example
