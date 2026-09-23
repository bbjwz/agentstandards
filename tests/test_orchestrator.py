from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from agentstandards.context import build_context
from agentstandards.models import (
    DecisionManifest,
    DecisionSelection,
    GateException,
    PersonaPayload,
    Verdict,
)
from agentstandards.orchestrator import (
    CouncilError,
    gate_status,
    validate_run_offline,
    verify_ready_gate,
)
from agentstandards.providers.base import ProviderError, ProviderResult
from agentstandards.providers.fake import FakeProvider
from agentstandards.storage import load_state, read_yaml, write_yaml

from .conftest import council_config, make_runner


def approve_manifest(path: Path) -> DecisionManifest:
    manifest = DecisionManifest.model_validate(read_yaml(path))
    manifest.status = "approved"
    manifest.decided_by = "architecture-owner"
    manifest.decided_at = datetime.now(UTC)
    manifest.selections = [
        DecisionSelection(
            conflict_id=conflict.conflict_id,
            selected_proposal_ids=[conflict.options[0].proposal_id],
            rationale="Selected after reviewing the cited multi-vendor synthesis evidence.",
        )
        for conflict in manifest.conflicts
    ]
    write_yaml(path, manifest)
    return manifest


@pytest.mark.asyncio
async def test_full_council_human_pause_resume_and_ready_gate(
    spec_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        "agentstandards.orchestrator.build_provider",
        lambda config, timeout_seconds: FakeProvider(config, timeout_seconds=timeout_seconds),
    )
    runner = make_runner(spec_project, council_config())
    paths = await runner.architect()
    state = load_state(paths)

    assert state.phase == "awaiting_human"
    assert len(state.completed_artifact_ids) == 48
    planner_independent = json.loads(
        paths.transcript_path("planning", "independent", "systems-architect", "codex").read_text(
            encoding="utf-8"
        )
    )
    assert "BEGIN PEER ARTIFACT" not in planner_independent["visible_user_prompt"]
    planner_disclosed = json.loads(
        paths.transcript_path("planning", "disclosed", "systems-architect", "codex").read_text(
            encoding="utf-8"
        )
    )
    assert "BEGIN PEER ARTIFACT" in planner_disclosed["visible_user_prompt"]
    assert '"underlying_vendor": "anthropic"' in planner_disclosed["visible_user_prompt"]
    assert planner_independent["isolation"]["context_mode"] == "fresh"
    assert planner_independent["isolation"]["prior_conversation_messages"] == 0
    assert planner_independent["isolation"]["provider_session_reused"] is False
    assert (
        planner_independent["isolation"]["invocation_id"]
        != planner_disclosed["isolation"]["invocation_id"]
    )
    assert (
        planner_independent["isolation"]["adapter_instance_id"]
        != planner_disclosed["isolation"]["adapter_instance_id"]
    )

    approve_manifest(paths.decision_manifest)

    resumed = make_runner(spec_project, council_config())
    await resumed.resume()
    report = gate_status(spec_project, spec_project / "specs" / "001-council")
    final_state = load_state(paths)

    assert report.status == "READY"
    assert set(report.ready_participants) >= {"codex", "anthropic"}
    assert final_state.phase == "ready"
    assert len(final_state.completed_artifact_ids) == 53
    assert paths.adr_log.exists()
    attempt_paths = list(paths.transcripts.rglob("*.attempt-*.json"))
    assert len(attempt_paths) == 53
    attempts = [json.loads(path.read_text(encoding="utf-8")) for path in attempt_paths]
    invocation_ids = [item["isolation"]["invocation_id"] for item in attempts]
    adapter_instance_ids = [item["isolation"]["adapter_instance_id"] for item in attempts]
    assert len(invocation_ids) == len(set(invocation_ids))
    assert len(adapter_instance_ids) == len(set(adapter_instance_ids))
    assert {item["isolation"]["context_mode"] for item in attempts} == {"fresh"}
    assert all(item["isolation"]["prior_conversation_messages"] == 0 for item in attempts)
    isolation_by_participant = {
        record.participant_id: record for record in report.validator_isolation
    }
    assert set(isolation_by_participant) >= {"codex", "anthropic"}
    assert all(
        item.independent_invocation_id != item.disclosed_invocation_id
        for item in isolation_by_participant.values()
    )
    assert validate_run_offline(spec_project, spec_project / "specs" / "001-council") == []

    transcript_path = paths.transcript_path("planning", "independent", "systems-architect", "codex")
    original_transcript = transcript_path.read_text(encoding="utf-8")
    tampered = json.loads(original_transcript)
    tampered["visible_output"] = "tampered"
    transcript_path.write_text(json.dumps(tampered), encoding="utf-8")
    feature_dir = spec_project / "specs" / "001-council"
    assert any(
        "output hash mismatch" in error for error in validate_run_offline(spec_project, feature_dir)
    )
    transcript_path.write_text(original_transcript, encoding="utf-8")

    tampered = json.loads(original_transcript)
    tampered["isolation"]["invocation_id"] = planner_disclosed["isolation"]["invocation_id"]
    transcript_path.write_text(json.dumps(tampered), encoding="utf-8")
    isolation_errors = validate_run_offline(spec_project, feature_dir)
    assert any("isolation mismatch" in error for error in isolation_errors)
    assert any("reuses an inference invocation" in error for error in isolation_errors)
    transcript_path.write_text(original_transcript, encoding="utf-8")

    config = council_config()
    feature = feature_dir
    current_context = build_context(spec_project, feature)
    assert (
        verify_ready_gate(spec_project, feature, config, current_context.content_hash).status
        == "READY"
    )
    (feature / "plan.md").write_text("# Changed after validation\n", encoding="utf-8")
    stale_context = build_context(spec_project, feature)
    with pytest.raises(CouncilError, match="stale"):
        verify_ready_gate(spec_project, feature, config, stale_context.content_hash)


class BlockingAnthropic(FakeProvider):
    async def generate(self, **kwargs):  # type: ignore[no-untyped-def]
        result = await super().generate(**kwargs)
        if self.config.id == "anthropic" and "architecture-validator" in kwargs["user_prompt"]:
            parsed = PersonaPayload.model_validate(result.parsed.model_dump())
            parsed.verdict = Verdict.BLOCKED
            parsed.summary = "Blocking validation finding"
            return ProviderResult(
                parsed=parsed,
                visible_output=parsed.model_dump_json(indent=2),
                resolved_model=result.resolved_model,
                request_id=result.request_id,
                usage=result.usage,
            )
        return result


@pytest.mark.asyncio
async def test_required_validator_disagreement_blocks_until_explicit_exception(
    spec_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        "agentstandards.orchestrator.build_provider",
        lambda config, timeout_seconds: BlockingAnthropic(config, timeout_seconds=timeout_seconds),
    )
    config = council_config()
    runner = make_runner(spec_project, config)
    paths = await runner.architect()
    approve_manifest(paths.decision_manifest)

    assert await make_runner(spec_project, config).resume() == paths
    report = gate_status(spec_project, spec_project / "specs" / "001-council")
    assert report.status == "BLOCKED"
    assert report.blocked_participants == ["anthropic"]

    blocking_id = next(
        artifact_id
        for artifact_id in report.validator_artifact_ids
        if artifact_id.endswith(":anthropic")
    )
    manifest = DecisionManifest.model_validate(read_yaml(paths.decision_manifest))
    manifest.status = "exception"
    manifest.exceptions = [
        GateException(
            validator_artifact_ids=[blocking_id],
            reason="Architecture owner accepts the documented tradeoff for this release.",
            approved_by="architecture-owner",
            approved_at=datetime.now(UTC),
        )
    ]
    write_yaml(paths.decision_manifest, manifest)

    await make_runner(spec_project, config).resume()
    excepted = gate_status(spec_project, spec_project / "specs" / "001-council")
    assert excepted.status == "READY"
    assert excepted.exception_applied is True


class OptionalFailureProvider(FakeProvider):
    async def generate(self, **kwargs):  # type: ignore[no-untyped-def]
        if self.config.id == "google":
            raise ProviderError("optional test outage")
        return await super().generate(**kwargs)


@pytest.mark.asyncio
async def test_optional_provider_failure_warns_without_stopping_required_quorum(
    spec_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        "agentstandards.orchestrator.build_provider",
        lambda config, timeout_seconds: OptionalFailureProvider(
            config, timeout_seconds=timeout_seconds
        ),
    )
    config = council_config(optional=True)
    paths = await make_runner(spec_project, config).architect()
    state = load_state(paths)
    assert state.phase == "awaiting_human"
    assert state.optional_warnings
    assert not any(item.endswith(":google") for item in state.completed_artifact_ids)


class RetryOnceProvider(FakeProvider):
    attempts: dict[tuple[str, str], int] = {}

    async def generate(self, **kwargs):  # type: ignore[no-untyped-def]
        key = (self.config.id, kwargs["user_prompt"])
        count = self.attempts.get(key, 0)
        self.attempts[key] = count + 1
        if count == 0:
            raise ProviderError("transient test failure", retryable=True)
        return await super().generate(**kwargs)


@pytest.mark.asyncio
async def test_transient_failure_retries_and_artifacts_remain_idempotent(
    spec_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    RetryOnceProvider.attempts = {}
    adapter_instance_ids: list[str] = []

    def build_retry_provider(config, timeout_seconds):  # type: ignore[no-untyped-def]
        provider = RetryOnceProvider(config, timeout_seconds=timeout_seconds)
        adapter_instance_ids.append(provider.adapter_instance_id)
        return provider

    monkeypatch.setattr(
        "agentstandards.orchestrator.build_provider",
        build_retry_provider,
    )
    config = council_config(retries=1)
    paths = await make_runner(spec_project, config).architect()
    first = load_state(paths)
    assert first.call_count == 96
    assert len(first.completed_artifact_ids) == 48
    assert len(list(paths.transcripts.rglob("*.attempt-*.json"))) == 96
    assert len(adapter_instance_ids) == 96
    assert len(adapter_instance_ids) == len(set(adapter_instance_ids))

    same_paths = await make_runner(spec_project, config).architect()
    second = load_state(same_paths)
    assert same_paths == paths
    assert second.call_count == first.call_count
    assert second.completed_artifact_ids == first.completed_artifact_ids
    assert len(adapter_instance_ids) == 96


class FailRequiredOnceProvider(FakeProvider):
    failed = False

    async def generate(self, **kwargs):  # type: ignore[no-untyped-def]
        prompt = kwargs["user_prompt"]
        if (
            self.config.id == "anthropic"
            and not self.failed
            and "# Persona\nsystems-architect" in prompt
            and "This is the independent pass" in prompt
        ):
            type(self).failed = True
            raise ProviderError("one-time required-provider failure")
        return await super().generate(**kwargs)


@pytest.mark.asyncio
async def test_partial_required_failure_resumes_without_repeating_completed_artifacts(
    spec_project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    FailRequiredOnceProvider.failed = False
    monkeypatch.setattr(
        "agentstandards.orchestrator.build_provider",
        lambda config, timeout_seconds: FailRequiredOnceProvider(
            config, timeout_seconds=timeout_seconds
        ),
    )
    config = council_config(retries=0)
    first_runner = make_runner(spec_project, config)
    with pytest.raises(CouncilError, match="required provider failure"):
        await first_runner.architect()
    assert first_runner.paths is not None
    failed_state = load_state(first_runner.paths)
    assert failed_state.phase == "failed"
    assert 0 < len(failed_state.completed_artifact_ids) < 48

    paths = await make_runner(spec_project, config).architect()
    resumed_state = load_state(paths)
    assert resumed_state.phase == "awaiting_human"
    assert len(resumed_state.completed_artifact_ids) == 48
    assert resumed_state.call_count == 49
    assert len(list(paths.transcripts.rglob("*.attempt-*.json"))) == 49
