# Machine-readable review gate

Use `scripts/report_gate.py <evidence.json> [--output final-report.json]`. It validates key status fields and returns a deterministic verdict. The script cannot establish that real tests ran; reviewer must supply truthful evidence and cite it in the Markdown report.

Example input:

```json
{
  "feature": "Orders update",
  "standards_source": "installed engineering-standards v2",
  "review_matrix_complete": true,
  "scope_verified": true,
  "checks": [
    {"id": "FT-001", "required": true, "status": "PASS", "evidence": "read-only git audit"},
    {"id": "CA-003", "required": true, "status": "PASS", "evidence": "request spec"}
  ],
  "test_runs": [
    {"kind": "request", "required": true, "status": "PASS", "command": "bundle exec rspec spec/requests/orders_spec.rb", "exit_code": 0, "passed": 5, "failed": 0, "skipped": 0}
  ],
  "browser": {"required": true, "status": "PASS", "flows_executed": 4, "evidence": "artifacts/e2e-trace.zip"},
  "unresolved_blockers": []
}
```

All required applicable checks/test_runs/browser entries must be PASS for READY. Browser required and no flows executed => BLOCKED. Required FAIL or unresolved_blockers => NEEDS_FIX. Required UNVERIFIED/BLOCKED => BLOCKED. `N/A` must set `required:false` and a nonempty `reason`. Empty `checks` or `test_runs` => BLOCKED, not READY. JSON output is for tooling; Markdown report remains necessary.
