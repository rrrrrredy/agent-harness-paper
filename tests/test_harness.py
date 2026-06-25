import pytest

from harness.core import evaluate_case, load_cases
from harness.providers import has_provider_key, provider_env_var, require_provider_key


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
