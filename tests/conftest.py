from __future__ import annotations

import json
from pathlib import Path

import pytest
from agentstandards.config import CouncilConfig, LimitsConfig, ParticipantConfig
from agentstandards.context import build_context
from agentstandards.orchestrator import CouncilRunner


@pytest.fixture
def spec_project(tmp_path: Path) -> Path:
    (tmp_path / ".specify" / "memory").mkdir(parents=True)
    (tmp_path / ".specify" / "memory" / "constitution.md").write_text(
        "# Constitution\nArchitecture decisions are traceable.\n", encoding="utf-8"
    )
    feature = tmp_path / "specs" / "001-council"
    feature.mkdir(parents=True)
    (feature / "spec.md").write_text(
        "# Feature\n## Requirements\n- REQ-001: produce a bounded design.\n",
        encoding="utf-8",
    )
    (feature / "plan.md").write_text(
        "# Plan\nUse an asynchronous provider-neutral council.\n", encoding="utf-8"
    )
    (feature / "tasks.md").write_text("# Must never leave the project\n", encoding="utf-8")
    (tmp_path / "application.py").write_text("SECRET_SOURCE = True\n", encoding="utf-8")
    (tmp_path / ".specify" / "feature.json").write_text(
        json.dumps({"feature_directory": "specs/001-council"}), encoding="utf-8"
    )
    return tmp_path


def council_config(*, optional: bool = False, retries: int = 1) -> CouncilConfig:
    participants = [
        ParticipantConfig(
            id="codex",
            required=True,
            transport="codex-cli",
            underlying_vendor="openai",
            model="gpt-test",
            executable="codex",
        ),
        ParticipantConfig(
            id="anthropic",
            required=True,
            transport="anthropic",
            underlying_vendor="anthropic",
            model="claude-test",
            api_key_env="ANTHROPIC_API_KEY",
        ),
    ]
    if optional:
        participants.append(
            ParticipantConfig(
                id="google",
                transport="google",
                underlying_vendor="google",
                model="gemini-test",
                api_key_env="GOOGLE_API_KEY",
            )
        )
    return CouncilConfig(
        configured=True,
        participants=participants,
        limits=LimitsConfig(
            max_concurrency=8,
            request_timeout_seconds=30,
            max_retries=retries,
            max_calls_per_run=200,
            max_total_input_tokens=100_000,
            max_total_output_tokens=100_000,
            max_cost_usd=10,
        ),
    )


def make_runner(project: Path, config: CouncilConfig) -> CouncilRunner:
    feature = project / "specs" / "001-council"
    return CouncilRunner(
        context=build_context(project, feature),
        config=config,
        config_path=(
            project / ".specify" / "extensions" / "agentstandards" / "agentstandards-config.yml"
        ),
    )
