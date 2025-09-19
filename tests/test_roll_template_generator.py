import importlib.util
from pathlib import Path

import yaml


GENERATOR_PATH = Path(__file__).resolve().parent.parent / "docs" / "manifest" / "narratives" / "rolls" / "generate_roll.py"


def load_generator_module():
    spec = importlib.util.spec_from_file_location("roll_generator", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load roll generator module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_front_matter(markdown: str):
    parts = markdown.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Missing YAML front matter in generated roll")
    yaml_block = parts[1].strip()
    body = parts[2]
    return yaml.safe_load(yaml_block), body


def ids_from(items):
    return [item["id"] if isinstance(item, dict) and "id" in item else item for item in items]


def test_generate_roll_front_matter_integrates_manifest_data(tmp_path):
    module = load_generator_module()
    generator = module.RollTemplateGenerator()
    output_path = generator.write_roll("hosomaki.ollama", tmp_path)
    assert output_path.exists()

    front_matter, body = extract_front_matter(output_path.read_text(encoding="utf-8"))

    assert front_matter["id"] == "hosomaki.ollama"
    assert front_matter["style"] == "Hosomaki"
    assert front_matter["title"].lower().startswith("ollama")
    assert front_matter["capabilities"]["provides"] == ["cap.llm-api", "cap.embeddings"]

    combo_ids = ids_from(front_matter["bundles"]["combos"])
    bento_ids = ids_from(front_matter["bundles"]["bento_boxes"])
    platter_ids = ids_from(front_matter["bundles"]["platters"])

    assert "combo.chat-local" in combo_ids
    assert "bento.ai-agent-foundation" in bento_ids
    assert "platter.hosomaki-core" in platter_ids

    assert front_matter["docker"]["image"] == "ollama/ollama:latest"
    assert front_matter["resources"]["cpu"]["minimum_cores"] == 2
    assert front_matter["resources"]["memory"]["minimum_mb"] == 4096
    assert front_matter["schema_version"] == "1.0.0"
    assert "quick_service_snapshot" in front_matter["export"]["sections"]

    assert "## 🍱 Quick service snapshot" in body
    assert "hosomaki.ollama" in body


def test_generate_roll_body_highlights_related_services(tmp_path):
    module = load_generator_module()
    generator = module.RollTemplateGenerator()
    output_path = generator.write_roll("hosomaki.n8n", tmp_path)

    front_matter, body = extract_front_matter(output_path.read_text(encoding="utf-8"))

    assert front_matter["id"] == "hosomaki.n8n"
    assert "bento.ai-agent-foundation" in ids_from(front_matter["bundles"]["bento_boxes"])
    works_with_section = body.split("## 🤝 Works great with", 1)[1]
    related_lines = [line for line in works_with_section.splitlines() if line.strip().startswith("- `")]
    assert len(related_lines) >= 3
    assert "## ⚙️ Deployment checklist" in body
    assert "generate_compose.py" in body
