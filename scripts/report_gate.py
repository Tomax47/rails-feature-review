#!/usr/bin/env python3
"""Derive an evidence-based review gate from supplied JSON status records."""
import argparse
import json
import sys
from pathlib import Path

STATES = {"PASS", "FAIL", "UNVERIFIED", "BLOCKED", "N/A"}


def gate(payload):
    issues = []
    failures = []
    blockers = []
    if not isinstance(payload, dict):
        raise ValueError("review evidence must be a JSON object")
    checks = payload.get("checks")
    test_runs = payload.get("test_runs")
    browser = payload.get("browser")
    if payload.get("review_matrix_complete") is not True:
        blockers.append("Applicable rule coverage not confirmed complete")
    if payload.get("scope_verified") is not True:
        blockers.append("Review scope not verified complete")
    if not str(payload.get("standards_source", "")).strip():
        blockers.append("Standards source not identified")
    if not isinstance(checks, list) or not checks:
        blockers.append("No standards checks supplied")
        checks = []
    if not isinstance(test_runs, list) or not test_runs:
        blockers.append("No executed test runs supplied")
        test_runs = []
    if not isinstance(browser, dict):
        blockers.append("Browser applicability/verification not supplied")
        browser = {}

    for kind, rows in (("check", checks), ("test", test_runs)):
        for i, row in enumerate(rows):
            if not isinstance(row, dict):
                blockers.append(f"Invalid {kind}[{i}] record")
                continue
            name = str(row.get("id", row.get("kind", i)))
            required = row.get("required")
            status = row.get("status")
            if type(required) is not bool or status not in STATES:
                blockers.append(f"{kind} {name}: missing/invalid required or status")
                continue
            if status == "N/A":
                if required or not str(row.get("reason", "")).strip():
                    blockers.append(f"{kind} {name}: invalid N/A")
                continue
            if required and status == "FAIL":
                failures.append(f"{kind} {name}: failed")
            elif required and status != "PASS":
                blockers.append(f"{kind} {name}: {status}")
            if kind == "test" and required and status == "PASS":
                exit_code = row.get("exit_code")
                passed = row.get("passed")
                failed = row.get("failed")
                skipped = row.get("skipped", 0)
                if not all(type(v) is int and v >= 0 for v in (passed, failed, skipped)) or type(exit_code) is not int:
                    blockers.append(f"test {name}: missing run counts/exit code")
                elif exit_code != 0 or failed > 0:
                    failures.append(f"test {name}: exit code or failure count inconsistent with PASS")
                elif passed < 1 or skipped > 0:
                    blockers.append(f"test {name}: no passing tests or skipped/pending checks")
                if not str(row.get("command", "")).strip():
                    blockers.append(f"test {name}: missing command")
    if browser:
        required = browser.get("required")
        status = browser.get("status")
        if type(required) is not bool or status not in STATES:
            blockers.append("Browser: missing/invalid status or applicability")
        elif not required:
            if status != "N/A" or not str(browser.get("reason", "")).strip():
                blockers.append("Browser: non-applicable requires reason")
        elif status == "FAIL":
            failures.append("Browser: failed")
        elif status != "PASS":
            blockers.append(f"Browser: {status}")
        elif type(browser.get("flows_executed")) is not int or browser["flows_executed"] < 1 or not str(browser.get("evidence", "")).strip():
            blockers.append("Browser: PASS requires executed flows and evidence")
    unresolved = payload.get("unresolved_blockers", [])
    if not isinstance(unresolved, list):
        blockers.append("Invalid unresolved_blockers format")
    elif unresolved:
        failures.extend(f"Unresolved blocker: {str(x)}" for x in unresolved)
    verdict = "NEEDS_FIX" if failures else "BLOCKED" if blockers else "READY"
    return {"feature": payload.get("feature", "unspecified"), "verdict": verdict, "failures": failures, "blocked_verifications": blockers, "notes": issues}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.evidence.read_text(encoding="utf-8"))
        result = gate(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Invalid evidence: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["verdict"] == "READY" else 1


if __name__ == "__main__":
    sys.exit(main())
