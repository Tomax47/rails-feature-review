import copy
import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "scripts" / "report_gate.py"
spec = importlib.util.spec_from_file_location("report_gate", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def sample():
    return {
        "feature": "Test feature",
        "standards_source": "bundled v2 fallback",
        "review_matrix_complete": True,
        "scope_verified": True,
        "checks": [{"id": "FT-001", "required": True, "status": "PASS", "evidence": "verified"}],
        "test_runs": [{"kind": "request", "required": True, "status": "PASS", "command": "bundle exec rspec spec/x_spec.rb", "exit_code": 0, "passed": 5, "failed": 0, "skipped": 0}],
        "browser": {"required": True, "status": "PASS", "flows_executed": 3, "evidence": "trace.zip"},
        "unresolved_blockers": []
    }


class GateTests(unittest.TestCase):
    def test_all_pass(self):
        self.assertEqual(module.gate(sample())["verdict"], "READY")

    def test_failed_rule_blocks(self):
        data = sample()
        data["checks"][0]["status"] = "FAIL"
        self.assertEqual(module.gate(data)["verdict"], "NEEDS_FIX")

    def test_unverified_rule_blocks(self):
        data = sample()
        data["checks"][0]["status"] = "UNVERIFIED"
        self.assertEqual(module.gate(data)["verdict"], "BLOCKED")

    def test_missing_browser_blocks(self):
        data = sample()
        data["browser"] = {"required": True, "status": "UNVERIFIED"}
        self.assertEqual(module.gate(data)["verdict"], "BLOCKED")

    def test_zero_browser_flows_blocks(self):
        data = sample()
        data["browser"]["flows_executed"] = 0
        self.assertEqual(module.gate(data)["verdict"], "BLOCKED")

    def test_browser_na_with_reason_for_backend(self):
        data = sample()
        data["browser"] = {"required": False, "status": "N/A", "reason": "API-only feature"}
        self.assertEqual(module.gate(data)["verdict"], "READY")

    def test_browser_na_no_reason_blocks(self):
        data = sample()
        data["browser"] = {"required": False, "status": "N/A"}
        self.assertEqual(module.gate(data)["verdict"], "BLOCKED")

    def test_missing_tests_blocks(self):
        data = sample()
        data["test_runs"] = []
        self.assertEqual(module.gate(data)["verdict"], "BLOCKED")

    def test_skipped_required_tests_block(self):
        data = sample()
        data["test_runs"][0]["skipped"] = 1
        self.assertEqual(module.gate(data)["verdict"], "BLOCKED")

    def test_inconsistent_test_status_fails(self):
        data = sample()
        data["test_runs"][0]["exit_code"] = 1
        self.assertEqual(module.gate(data)["verdict"], "NEEDS_FIX")

    def test_unresolved_blocker_fails(self):
        data = sample()
        data["unresolved_blockers"] = ["Cannot authorize record"]
        self.assertEqual(module.gate(data)["verdict"], "NEEDS_FIX")

    def test_missing_full_rule_coverage_blocks(self):
        data = sample()
        data["review_matrix_complete"] = False
        self.assertEqual(module.gate(data)["verdict"], "BLOCKED")

    def test_invalid_na_rule_blocks(self):
        data = sample()
        data["checks"][0] = {"id": "FT-003", "required": True, "status": "N/A"}
        self.assertEqual(module.gate(data)["verdict"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
