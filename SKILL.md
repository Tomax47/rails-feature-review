---
name: rails-feature-review
description: Review and verify generated Ruby on Rails feature changes against the Engineering Standards skill. Use after an AI agent implements or modifies a Rails feature, when asked for code review, architecture compliance, missing RSpec tests, browser-based development-environment end-to-end testing, edge-case coverage, regression verification, or a go/no-go testing report. Writes narrowly scoped tests, runs available checks, and reports observed evidence; never self-approves unverified work.
---

# Rails Feature Review — Independent verification

**Role:** Act as a skeptical reviewer, not the feature's implementer. Verify the actual working tree, add narrowly scoped automated tests where needed, exercise the feature in a real development browser when supported, and produce a report with evidence and a release decision. Do not implement feature fixes while reviewing; describe required fixes and request a separate implementation pass. Tests and test fixtures are the only allowed code additions, subject to the team's minimal-change, no-comments, and style rules. Use another verification pass after fixes.

## 0. Never violate these guardrails

1. Never run `git commit`, `git push`, `git reset`, `git clean`, `git rebase`, forced checkout, or any other history/worktree-destructive Git operation; only inspect with safe read-only Git commands. Do not deploy or edit remote environments.
2. Never edit `lib/jumpstart/`. If testing requires changes there, report a blocker; the feature implementer must use the established `app/` override pattern.
3. Never add comments to project code or tests, or assign/initialize variables in ERB templates. Do not improvise existing logic or styling. Keep changes limited to necessary test files and smallest required additions.
4. Never introduce SQL-firing operations inside Pundit policy predicates. SQL-based scopes are permitted inside `Scope#resolve`. Inspect method calls with side effects, not just visible `.where` text.
5. Never mutate production data, run destructive database maintenance against shared environments, publish artifacts, send real messages/payments, or access external live services to test. Use isolated test DB, fake external providers, test accounts, and configured development endpoints. If environment identity cannot be verified, stop the risky action and mark it BLOCKED.
6. Any change to feature code, missing architecture decision, prohibited operation, or required exception needs explicit user approval; report it, do not quietly correct it.

## 1. Establish review inputs and evidence

- Identify the repository, requested behavior/acceptance criteria, feature routes, expected UX, changed files, and baseline (ideally a provided base commit/branch). Use `git status --short`, `git diff --stat`, `git diff`, and `git diff --cached` safely. If base is unavailable, review observed working tree and flag uncertainty about attribution. Never execute generated code or scripts blindly.
- Find the **latest installed/source Engineering Standards skill** and its references, version, and scanner. This is authoritative over the bundled snapshot. If unavailable, use `references/standards-snapshot/` as the explicitly dated v2 fallback and disclose it. Never describe the fallback as current policy. Read `references/rule-review-matrix.md` and `references/browser-testing.md`.
- Read relevant adjacent repository implementations and specs before writing tests. Explain actual scope: changed files, affected dependencies, risks, and reachable browser workflows. If application access or required acceptance criteria are missing, perform safe review and tests that are possible; report missing coverage as UNVERIFIED, not PASS.
- Protect secrets, PII, credentials, browser cookies, and screenshots. Redact reports and paths before sharing.

## 2. Review standards and changed code

- Check all eight field-tested FT guardrails on every task, then every applicable AR, OI, BJ, CA, and VW rule. Use the original engineering rule IDs, exact evidence with file and line, severity, proposed minimal correction, and PASS / FAIL / UNVERIFIED / N/A outcome.
- Cross-check Pundit code, controller authorization, organizer composition and transaction rollback, callbacks, business logic location, error propagation and Active Job retry/discard, idempotency, Jbuilder partial reuse, ERB assignments, SQL in views, exact replication of existing logic, comments, styling drift, and minimal diff size.
- Use the **current standards skill's scanner** if present, otherwise bundled `scripts/check_architecture_snapshot.py` as a heuristic supplemental signal. Confirm warnings manually and look for false negatives; a clean scanner output is not a full standards pass. Do not run arbitrary scripts on untrusted project code without reviewing their content and effects.

## 3. Design and implement focused automated tests

- Read `references/test-strategy.md`. Create a feature-specific test matrix with positive, negative, authorization, boundary, failure, and regression cases. Include relevant Rails units, requests, organizers/interactors, models, job retries, idempotency, and views; mark non-applicable types with reasons.
- Follow the project's established RSpec/Minitest framework, factory/fixture conventions, helpers, naming, and mocking techniques; do not add a new testing framework unless approved. Test observable behavior and avoid brittle implementation-coupled expectations.
- Add **only missing, justified tests** in the smallest coherent diff. Do not delete or alter pre-existing tests to make failures disappear. Do not change production code. If tests reveal a bug, record the failing case and the recommended fix, then await a separate change.
- Verify test environment and isolated database before running any command that may write data. Inspect test commands and project scripts for dangerous side effects. Run focused tests, relevant regression suites, and lint/static checks where available; capture exit status, command, counts, failures and logs. A skipped/pending test does not count as passed.

## 4. Functionally test in a real dev browser

- Follow `references/browser-testing.md`. Verify the actual URL is an authorized **development/staging/test** environment, never production. Confirm test identity/account and that external integrations run in sandbox/fake mode. Do not test payments, emails, external API calls, or destructive user actions against live endpoints.
- Open a real browser using available browser automation (for example Playwright, an approved browser connector, or the agent's browser tool). Navigate the feature; exercise the happy path, validation errors, empty and boundary states, unauthorized access, relevant role differences, state transitions, retries/double-submit, and UI regressions as applicable. Include realistic selectors, screenshots and console/network evidence; do not infer success from HTML source or an HTTP response alone.
- When browser tooling, server, credentials, or an isolated dev environment are unavailable, do **not** invent observations, screenshots, counts or test results. Mark browser verification BLOCKED or UNVERIFIED and identify what is missing. Browser tests are a **required gate for UI-bearing features**. For backend-only features document why browser review is N/A and use API/integration behavior tests instead.

## 5. Decide and report

- Write a concise Markdown report using `references/report-template.md`, optionally produce a machine-readable summary with `scripts/report_gate.py` and schema in `references/report-schema.md`.
- Record **exact commands and exit codes**, tested dev URL (redacted if sensitive), browser sessions/flows, evidence paths, added test files, pass/fail/skip counts, cases not exercised, and all rule-level findings with minimal reproduction. Distinguish unit, request/integration, E2E, style, architecture, and unverified work.
- Decision: **READY** only if all mandatory applicable rules and tests pass, required browser E2E was executed and passed, no blocking findings remain, and necessary verification is complete. **NEEDS_FIX** when any blocking rule, functionality, or test fails. **BLOCKED** when required verification cannot be performed or evidence is incomplete; cannot claim ready. **READY_WITH_NOTES** is not allowed as a substitute for unresolved required checks.
- Do not automatically merge, commit, push, deploy, or claim approval. Present actionable recommendations, assign each finding severity, and invite the implementer to repair followed by retesting.

## Bundled resources

- `references/rule-review-matrix.md` — cross-domain and field-tested rule checklist.
- `references/test-strategy.md` — test case selection and edge case requirements.
- `references/browser-testing.md` — authorized development browser protocol.
- `references/report-template.md` and `references/report-schema.md` — auditable report and gate data.
- `references/standards-snapshot/` — bundled dated Engineering Standards v2 reference snapshot, fallback only.
- `scripts/check_architecture_snapshot.py` — **heuristic** baseline scanner copied from original skill, not a certified policy validator.
- `scripts/report_gate.py` — independent deterministic final gate, testable with `tests/test_report_gate.py`.

## User inputs that improve completeness

Prefer defaults from repo/config. If impossible to proceed, ask only for the missing high-impact information: repo or diff; feature requirements/acceptance criteria; authorized dev URL and test account; reference Engineering Standards skill if more recent than bundled fallback. A missing optional detail is not a reason to stop safe inspection; a missing safe dev environment is a reason to stop browser actions.
