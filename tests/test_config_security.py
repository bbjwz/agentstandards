from __future__ import annotations

from pathlib import Path

import pytest
from agentstandards.config import CouncilConfig, ParticipantConfig
from agentstandards.context import build_context
from agentstandards.security import SecurityViolation, assert_no_secrets
from pydantic import ValidationError

from .conftest import council_config


@pytest.mark.parametrize("model", ["auto", "route-llm", "default", "unknown"])
def test_auto_routed_models_are_rejected(model: str) -> None:
    with pytest.raises(ValidationError, match="auto-routing"):
        ParticipantConfig(
            id="router",
            transport="openai-compatible",
            underlying_vendor="unknown",
            model=model,
            api_key_env="ROUTER_API_KEY",
            base_url="https://example.invalid/v1",
        )


def test_transport_diversity_does_not_count_as_vendor_diversity() -> None:
    config = council_config()
    duplicate = ParticipantConfig(
        id="openai-gateway",
        transport="openai-compatible",
        underlying_vendor="openai",
        model="gpt-explicit",
        api_key_env="GATEWAY_API_KEY",
        base_url="https://example.invalid/v1",
    )
    with pytest.raises(ValidationError, match="distinct underlying vendors"):
        CouncilConfig(
            configured=True,
            participants=[*config.participants, duplicate],
        )


def test_gateway_identity_cannot_masquerade_as_underlying_vendor() -> None:
    with pytest.raises(ValidationError, match="underlying vendor"):
        ParticipantConfig(
            id="router",
            transport="openai-compatible",
            underlying_vendor="openrouter",
            model="anthropic/claude-explicit",
            api_key_env="ROUTER_API_KEY",
            base_url="https://example.invalid/v1",
        )


def test_context_excludes_source_tasks_and_diffs(spec_project: Path) -> None:
    bundle = build_context(spec_project, spec_project / "specs" / "001-council")
    names = {path.name for path in bundle.files}
    assert "spec.md" in names
    assert "plan.md" in names
    assert "tasks.md" not in names
    assert "application.py" not in names
    assert "Must never leave" not in bundle.content
    assert "SECRET_SOURCE" not in bundle.content


@pytest.mark.parametrize(
    "secret",
    [
        "sk-ant-abcdefghijklmnopqrstuvwxyz123456",
        "ghp_abcdefghijklmnopqrstuvwxyz1234567890",
        "Authorization: Bearer abcdefghijklmnopqrstuvwxyz",
    ],
)
def test_high_confidence_secrets_abort(secret: str) -> None:
    with pytest.raises(SecurityViolation):
        assert_no_secrets(f"credential={secret}", label="test")


def test_secret_in_architecture_context_aborts(spec_project: Path) -> None:
    (spec_project / "specs" / "001-council" / "plan.md").write_text(
        "token: sk-ant-abcdefghijklmnopqrstuvwxyz123456\n", encoding="utf-8"
    )
    with pytest.raises(SecurityViolation):
        build_context(spec_project, spec_project / "specs" / "001-council")
