from __future__ import annotations

import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from harness.core import evaluate_case, load_cases
from scripts.run_local_reference import reference_actions


FIXTURE = ROOT / "fixtures" / "repo_state_contract"
WORK = ROOT / "dist" / "repo-fixtures" / "saner_state_diff"
RESULTS = ROOT / "results" / "fixtures"


def main() -> None:
    prepare_worktree()
    before = WORK / "before"
    after = WORK / "after"
    shutil.copytree(FIXTURE / "before", before)
    shutil.copytree(FIXTURE / "before", after)

    case = next(item for item in load_cases() if item.id == "state_002")
    payload = reference_actions(case, "thin_contract")
    trace = apply_actions(after, payload["actions"])
    test_result = run_fixture_test(after)
    result = evaluate_case(case, payload, provider="repo_fixture", variant="thin_contract")
    diff_text = unified_tree_diff(before, after)

    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "saner_repo_fixture.diff").write_text(diff_text, encoding="utf-8")
    trace_payload = {
        "case_id": case.id,
        "task_success": result.task_success,
        "state_diff_correct": result.state_diff_correct,
        "permission_violations": result.permission_violations,
        "invalid_tool_calls": result.invalid_tool_calls,
        "unsafe_secret_access": result.unsafe_secret_access,
        "replayable": result.replayable,
        "test_result": test_result,
        "actions": payload["actions"],
        "trace": trace,
        "diff_sha256": sha256_text(diff_text),
    }
    (RESULTS / "saner_repo_fixture_trace.json").write_text(
        json.dumps(trace_payload, indent=2),
        encoding="utf-8",
    )
    (RESULTS / "saner_repo_fixture_summary.md").write_text(
        summary_markdown(trace_payload, diff_text),
        encoding="utf-8",
    )
    print("wrote results/fixtures/saner_repo_fixture_summary.md")


def prepare_worktree() -> None:
    resolved = WORK.resolve()
    dist_root = (ROOT / "dist" / "repo-fixtures").resolve()
    if dist_root not in resolved.parents and resolved != dist_root:
        raise RuntimeError(f"refusing to clean outside fixture output root: {resolved}")
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)


def apply_actions(after: Path, actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    trace: list[dict[str, Any]] = []
    for action in actions:
        tool = action["tool"]
        args = action.get("args", {})
        if tool == "write_file":
            rel_path = Path(str(args["path"]))
            target = after / rel_path
            before_text = target.read_text(encoding="utf-8") if target.exists() else ""
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(str(args.get("content", "")), encoding="utf-8")
            trace.append(
                {
                    "tool": tool,
                    "path": rel_path.as_posix(),
                    "before_sha256": sha256_text(before_text),
                    "after_sha256": sha256_text(target.read_text(encoding="utf-8")),
                }
            )
        elif tool == "run_tests":
            trace.append({"tool": tool, "result": "executed"})
        else:
            trace.append({"tool": tool, "result": "ignored_by_fixture"})
    return trace


def run_fixture_test(after: Path) -> dict[str, Any]:
    module_path = after / "src" / "app.py"
    spec = importlib.util.spec_from_file_location("fixture_app", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    passed = getattr(module, "VALUE", None) == 2
    return {"name": "VALUE == 2", "passed": passed}


def unified_tree_diff(before: Path, after: Path) -> str:
    paths = sorted({p.relative_to(before) for p in before.rglob("*") if is_text_source(p)} | {p.relative_to(after) for p in after.rglob("*") if is_text_source(p)})
    chunks: list[str] = []
    for rel in paths:
        before_text = read_lines(before / rel)
        after_text = read_lines(after / rel)
        if before_text == after_text:
            continue
        chunks.extend(
            difflib.unified_diff(
                before_text,
                after_text,
                fromfile=f"before/{rel.as_posix()}",
                tofile=f"after/{rel.as_posix()}",
                lineterm="",
            )
        )
    return "\n".join(chunks) + ("\n" if chunks else "")


def read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8").splitlines()


def is_text_source(path: Path) -> bool:
    if "__pycache__" in path.parts:
        return False
    return path.is_file() and path.suffix.lower() in {".py", ".md", ".txt", ".json", ".yml", ".yaml"}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def summary_markdown(trace_payload: dict[str, Any], diff_text: str) -> str:
    lines = [
        "# SANER Repository Fixture Summary",
        "",
        "This fixture turns benchmark case `state_002` into a concrete repository-state change.",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| task_success | {trace_payload['task_success']} |",
        f"| state_diff_correct | {trace_payload['state_diff_correct']} |",
        f"| permission_violations | {trace_payload['permission_violations']} |",
        f"| invalid_tool_calls | {trace_payload['invalid_tool_calls']} |",
        f"| unsafe_secret_access | {trace_payload['unsafe_secret_access']} |",
        f"| replayable | {trace_payload['replayable']} |",
        f"| fixture_test | {trace_payload['test_result']['name']}: {trace_payload['test_result']['passed']} |",
        f"| diff_sha256 | `{trace_payload['diff_sha256']}` |",
        "",
        "## Unified Diff",
        "",
        "```diff",
        diff_text.rstrip(),
        "```",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
