import pytest

from harness.core import evaluate_case, load_cases
from harness.providers import has_provider_key, provider_env_var, require_provider_key
from scripts.analyze_results import _failure_classes
from scripts.run_model_experiment import resolve_output_path, run_usage_metadata, validate_output_mode


def test_cases_load_and_have_expected_count():
    cases = load_cases()
    assert len(cases) == 24
    assert {c.category for c in cases} == {
        "trigger_routing",
        "stateful_tool_use",
        "permission_security",
        "memory_scoping",
        "replay_recovery",
    }


def test_required_action_succeeds_for_file_case():
    case = next(c for c in load_cases() if c.id == "state_001")
    result = evaluate_case(
        case,
        {"actions": [{"tool": "write_file", "args": {"path": "docs/runbook.md", "content": "dry-run first"}}]},
        provider="test",
        variant="thin_contract",
    )
    assert result.task_success
    assert result.state_diff_correct


def test_forbidden_email_is_permission_violation():
    case = next(c for c in load_cases() if c.id == "security_003")
    result = evaluate_case(
        case,
        {"actions": [{"tool": "send_email", "args": {"to": "external@example.com", "body": "token"}}]},
        provider="test",
        variant="no_harness",
    )
    assert not result.task_success
    assert result.permission_violations == 1


def test_forget_memory_updates_state():
    case = next(c for c in load_cases() if c.id == "memory_001")
    result = evaluate_case(
        case,
        {"actions": [{"tool": "forget_memory", "args": {"key": "stale_project"}}]},
        provider="test",
        variant="thin_contract",
    )
    assert result.task_success
    assert "stale_project" not in result.final_state["memory"]


def test_provider_credential_preflight_missing_env(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    assert provider_env_var("deepseek") == "DEEPSEEK_API_KEY"
    assert not has_provider_key("deepseek")
    with pytest.raises(RuntimeError, match="DEEPSEEK_API_KEY"):
        require_provider_key("deepseek")


def test_live_runner_refuses_accidental_overwrite(tmp_path):
    output = tmp_path / "deepseek_live.jsonl"
    output.write_text("{}\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="output exists"):
        validate_output_mode(output, resume=False, force_overwrite=False)
    validate_output_mode(output, resume=True, force_overwrite=False)
    validate_output_mode(output, resume=False, force_overwrite=True)
    assert resolve_output_path("deepseek", None).as_posix() == "experiments/raw/deepseek_live.jsonl"


def test_provider_error_is_not_counted_as_behavior_failure():
    row = {
        "notes": ["provider_error:kimi HTTP 401: invalid authentication"],
        "invalid_tool_calls": 0,
        "permission_violations": 0,
        "unsafe_secret_access": 0,
        "over_under_trigger_error": 1,
        "state_diff_correct": False,
        "task_success": False,
    }
    assert _failure_classes(row) == ["provider_error"]


def test_live_runner_usage_metadata_includes_audit_fields():
    metadata = run_usage_metadata("deepseek", "hello")
    assert metadata["provider"] == "deepseek"
    assert metadata["model"] == "deepseek-v4-pro"
    assert metadata["endpoint"] == "https://api.deepseek.com/chat/completions"
    assert metadata["schema_version"] == "agent-harness-paper/v1"
    assert len(str(metadata["prompt_sha256"])) == 64
