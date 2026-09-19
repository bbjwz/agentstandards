from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
from agentstandards.config import ParticipantConfig
from agentstandards.models import PersonaPayload
from agentstandards.providers.anthropic import AnthropicProvider
from agentstandards.providers.base import ProviderError
from agentstandards.providers.codex import CodexCliProvider
from agentstandards.providers.google import GoogleProvider
from agentstandards.providers.openai_compatible import OpenAICompatibleProvider


def _payload() -> dict:
    return PersonaPayload(
        summary="Structured provider assessment",
        confidence=91,
    ).model_dump(mode="json")


def _patch_client(monkeypatch: pytest.MonkeyPatch, module_httpx, handler) -> None:  # type: ignore[no-untyped-def]
    real_client = httpx.AsyncClient
    transport = httpx.MockTransport(handler)

    def client(*args, **kwargs):  # type: ignore[no-untyped-def]
        kwargs.pop("timeout", None)
        return real_client(transport=transport, timeout=30, **kwargs)

    monkeypatch.setattr(module_httpx, "AsyncClient", client)


@pytest.mark.asyncio
async def test_native_anthropic_adapter_uses_structured_outputs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-a-real-secret")

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body["output_config"]["format"]["type"] == "json_schema"
        assert request.headers["x-api-key"] == "test-key-not-a-real-secret"
        return httpx.Response(
            200,
            headers={"request-id": "anthropic-request"},
            json={
                "id": "msg-test",
                "model": "claude-test",
                "stop_reason": "end_turn",
                "content": [{"type": "text", "text": json.dumps(_payload())}],
                "usage": {"input_tokens": 12, "output_tokens": 8},
            },
        )

    import agentstandards.providers.anthropic as module

    _patch_client(monkeypatch, module.httpx, handler)
    config = ParticipantConfig(
        id="anthropic",
        required=True,
        transport="anthropic",
        underlying_vendor="anthropic",
        model="claude-test",
        api_key_env="ANTHROPIC_API_KEY",
    )
    result = await AnthropicProvider(config, timeout_seconds=30).generate(
        system_prompt="system",
        user_prompt="user",
        output_model=PersonaPayload,
        project_root="/tmp",
    )
    assert result.parsed.summary == "Structured provider assessment"
    assert result.usage.input_tokens == 12


@pytest.mark.asyncio
async def test_native_google_adapter_uses_response_json_schema(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key-not-a-real-secret")

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body["generationConfig"]["responseMimeType"] == "application/json"
        assert "responseJsonSchema" in body["generationConfig"]
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "finishReason": "STOP",
                        "content": {"parts": [{"text": json.dumps(_payload())}]},
                    }
                ],
                "usageMetadata": {
                    "promptTokenCount": 10,
                    "candidatesTokenCount": 7,
                },
            },
        )

    import agentstandards.providers.google as module

    _patch_client(monkeypatch, module.httpx, handler)
    config = ParticipantConfig(
        id="google",
        transport="google",
        underlying_vendor="google",
        model="gemini-test",
        api_key_env="GOOGLE_API_KEY",
    )
    result = await GoogleProvider(config, timeout_seconds=30).generate(
        system_prompt="system",
        user_prompt="user",
        output_model=PersonaPayload,
        project_root="/tmp",
    )
    assert result.parsed.confidence == 91
    assert result.usage.output_tokens == 7


@pytest.mark.asyncio
async def test_openai_compatible_adapter_pins_model_and_schema(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ROUTER_API_KEY", "test-key-not-a-real-secret")

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body["model"] == "explicit-vendor/model-test"
        assert body["response_format"]["json_schema"]["strict"] is True
        return httpx.Response(
            200,
            headers={"x-request-id": "router-request"},
            json={
                "id": "completion-test",
                "model": "explicit-vendor/model-test",
                "choices": [{"message": {"content": json.dumps(_payload())}}],
                "usage": {"prompt_tokens": 14, "completion_tokens": 9},
            },
        )

    import agentstandards.providers.openai_compatible as module

    _patch_client(monkeypatch, module.httpx, handler)
    config = ParticipantConfig(
        id="router",
        transport="openai-compatible",
        underlying_vendor="explicit-vendor",
        model="explicit-vendor/model-test",
        api_key_env="ROUTER_API_KEY",
        base_url="https://router.example/v1",
    )
    result = await OpenAICompatibleProvider(config, timeout_seconds=30).generate(
        system_prompt="system",
        user_prompt="user",
        output_model=PersonaPayload,
        project_root="/tmp",
    )
    assert result.resolved_model == "explicit-vendor/model-test"
    assert result.request_id == "router-request"


@pytest.mark.asyncio
async def test_anthropic_timeout_is_retryable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-a-real-secret")

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("test timeout", request=request)

    import agentstandards.providers.anthropic as module

    _patch_client(monkeypatch, module.httpx, handler)
    config = ParticipantConfig(
        id="anthropic",
        required=True,
        transport="anthropic",
        underlying_vendor="anthropic",
        model="claude-test",
        api_key_env="ANTHROPIC_API_KEY",
    )
    with pytest.raises(ProviderError) as captured:
        await AnthropicProvider(config, timeout_seconds=30).generate(
            system_prompt="system",
            user_prompt="user",
            output_model=PersonaPayload,
            project_root="unused",
        )
    assert captured.value.retryable is True


@pytest.mark.asyncio
async def test_anthropic_refusal_is_visible_and_not_retried(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-a-real-secret")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "model": "claude-test",
                "stop_reason": "refusal",
                "content": [{"type": "text", "text": "I cannot perform this review."}],
            },
        )

    import agentstandards.providers.anthropic as module

    _patch_client(monkeypatch, module.httpx, handler)
    config = ParticipantConfig(
        id="anthropic",
        required=True,
        transport="anthropic",
        underlying_vendor="anthropic",
        model="claude-test",
        api_key_env="ANTHROPIC_API_KEY",
    )
    with pytest.raises(ProviderError) as captured:
        await AnthropicProvider(config, timeout_seconds=30).generate(
            system_prompt="system",
            user_prompt="user",
            output_model=PersonaPayload,
            project_root="unused",
        )
    assert captured.value.retryable is False
    assert captured.value.visible_output == "I cannot perform this review."


@pytest.mark.asyncio
async def test_openai_compatible_repairs_invalid_json_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ROUTER_API_KEY", "test-key-not-a-real-secret")
    requests = 0
    reserved_repairs = 0

    async def reserve_repair() -> None:
        nonlocal reserved_repairs
        reserved_repairs += 1

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal requests
        requests += 1
        content = "not-json" if requests == 1 else json.dumps(_payload())
        return httpx.Response(
            200,
            json={
                "model": "explicit-vendor/model-test",
                "choices": [{"message": {"content": content}}],
            },
        )

    import agentstandards.providers.openai_compatible as module

    _patch_client(monkeypatch, module.httpx, handler)
    config = ParticipantConfig(
        id="router",
        transport="openai-compatible",
        underlying_vendor="explicit-vendor",
        model="explicit-vendor/model-test",
        api_key_env="ROUTER_API_KEY",
        base_url="https://router.example/v1",
    )
    result = await OpenAICompatibleProvider(config, timeout_seconds=30).generate(
        system_prompt="system",
        user_prompt="user",
        output_model=PersonaPayload,
        project_root="unused",
        reserve_call=reserve_repair,
    )
    assert requests == 2
    assert reserved_repairs == 1
    assert [exchange.kind for exchange in result.exchanges] == ["generate", "repair"]
    assert result.parsed.confidence == 91


@pytest.mark.asyncio
async def test_codex_participant_runs_in_isolated_empty_directory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: dict[str, object] = {}

    class Process:
        returncode = 0

        async def communicate(self, stdin: bytes):
            observed["stdin"] = stdin.decode()
            return b'{"thread_id":"codex-test","usage":{"input_tokens":3,"output_tokens":2}}\n', b""

        def kill(self) -> None:
            raise AssertionError("process should not be killed")

        async def wait(self) -> None:
            return None

    async def create_subprocess(*args, **kwargs):  # type: ignore[no-untyped-def]
        observed["args"] = args
        observed["cwd"] = kwargs["cwd"]
        output_path = args[args.index("--output-last-message") + 1]
        Path(output_path).write_text(json.dumps(_payload()), encoding="utf-8")
        return Process()

    monkeypatch.setattr(
        "agentstandards.providers.codex.asyncio.create_subprocess_exec",
        create_subprocess,
    )
    config = ParticipantConfig(
        id="codex",
        required=True,
        transport="codex-cli",
        underlying_vendor="openai",
        model="gpt-test",
        executable="codex",
    )
    result = await CodexCliProvider(config, timeout_seconds=30).generate(
        system_prompt="system",
        user_prompt="architecture only",
        output_model=PersonaPayload,
        project_root="/project/with/source",
    )
    args = observed["args"]
    assert isinstance(args, tuple)
    isolated = args[args.index("--cd") + 1]
    assert isolated == observed["cwd"]
    assert isolated != "/project/with/source"
    assert result.request_id == "codex-test"
