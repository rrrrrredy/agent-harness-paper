from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from harness.core import evaluate_case, load_cases
from scripts.run_local_reference import reference_actions


def main() -> None:
    cases = load_cases()
    assert len(cases) == 24, f"expected 24 cases, found {len(cases)}"
    ids = {case.id for case in cases}
    assert "security_001" in ids, "missing security_001"
    case = next(item for item in cases if item.id == "security_001")
    payload = reference_actions(case, "thin_contract")
    result = evaluate_case(case, payload, provider="local_reference", variant="thin_contract")
    assert result.task_success, "security_001 reference task should succeed"
    assert result.state_diff_correct, "security_001 reference state diff should pass"
    assert result.permission_violations == 0, "security_001 should have no permission violation"
    assert result.unsafe_secret_access == 0, "security_001 should not access secrets"
    assert result.replayable, "security_001 reference trajectory should be replayable"
    print("smoke test passed")


if __name__ == "__main__":
    main()
