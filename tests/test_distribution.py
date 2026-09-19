from __future__ import annotations

import json
import zipfile
from pathlib import Path

import yaml
from agentstandards.personas import load_personas

from scripts.build_release import build


def test_canonical_registry_contains_all_thirteen_personas() -> None:
    registry = load_personas()
    assert len(registry.planners) == 6
    assert len(registry.critics) == 5
    assert len(registry.gatekeepers) == 2
    assert (
        len(
            {
                persona.id
                for persona in [*registry.planners, *registry.critics, *registry.gatekeepers]
            }
        )
        == 13
    )


def test_release_archives_are_clean_and_installable_shape(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    artifacts = build(root, tmp_path)
    assert {path.name for path in artifacts} == {
        "agentstandards-0.1.0.zip",
        "agentstandards-gate-0.1.0.zip",
        "agentstandards-bundle-0.1.0.zip",
    }
    expected = {
        "agentstandards-0.1.0.zip": {
            "extension.yml",
            "commands/speckit.agentstandards.init.md",
            "runtime/agentstandards/personas.yml",
            "scripts/bash/agentstandards.sh",
            "scripts/powershell/agentstandards.ps1",
            "scripts/python/agentstandards.py",
        },
        "agentstandards-gate-0.1.0.zip": {
            "preset.yml",
            "commands/speckit.tasks.md",
        },
        "agentstandards-bundle-0.1.0.zip": {"bundle.yml", "README.md"},
    }
    for artifact in artifacts:
        with zipfile.ZipFile(artifact) as archive:
            names = set(archive.namelist())
        assert expected[artifact.name].issubset(names)
        assert not any("__pycache__" in name or name.endswith(".pyc") for name in names)


def test_manifests_commands_and_catalogs_have_consistent_version() -> None:
    root = Path(__file__).resolve().parents[1]
    extension = yaml.safe_load((root / "extension.yml").read_text(encoding="utf-8"))
    preset = yaml.safe_load(
        (root / "presets" / "agentstandards-gate" / "preset.yml").read_text(encoding="utf-8")
    )
    workflow = yaml.safe_load(
        (root / "workflows" / "agentstandards-architecture" / "workflow.yml").read_text(
            encoding="utf-8"
        )
    )
    bundle = yaml.safe_load(
        (root / "bundles" / "agentstandards" / "bundle.yml").read_text(encoding="utf-8")
    )
    assert {
        extension["extension"]["version"],
        preset["preset"]["version"],
        workflow["workflow"]["version"],
        bundle["bundle"]["version"],
    } == {"0.1.0"}

    for command in (root / "commands").glob("*.md"):
        text = command.read_text(encoding="utf-8")
        frontmatter = yaml.safe_load(text.split("---", 2)[1])
        assert set(frontmatter["scripts"]) == {"sh", "ps", "py"}

    for path in (root / "catalogs").glob("*.json"):
        catalog = json.loads(path.read_text(encoding="utf-8"))
        assert catalog["schema_version"] == "1.0"
        assert catalog["catalog_url"].startswith("https://")
