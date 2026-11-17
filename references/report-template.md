# Feature verification report — <feature / date>

**Release decision:** READY | NEEDS_FIX | BLOCKED
**Review scope:** repository / diff base / changed files / intended behavior
**Standards source:** installed skill path/version or bundled v2 fallback
**Environment:** app/test DB, development browser URL (redacted), test identity (redacted)

## Executive verdict
One paragraph on whether this is safe to hand back for release consideration. Never say READY if any mandatory test or code rule failed or remains unverified.

## Standards compliance
| Rule ID | Status (PASS/FAIL/UNVERIFIED/N/A) | Evidence file:line or test | Finding / needed correction |
|---|---|---|---|

## Automated tests
| Type | Command | Exit | Passed | Failed | Skipped/pending | Evidence |
|---|---|---|---|---|---|---|

**Tests added:** paths and covered cases. **Tests not run:** reasons.

## Browser functional verification
**Applicability:** required / N/A with justification / blocked
**Browser & viewport:** ...
**Dev URL & account context:** redacted
| Flow & case | Expected | Observed | PASS/FAIL/UNVERIFIED | Evidence |
|---|---|---|---|---|

**Console/network:** ... **Screenshots/traces:** ...

## Edge cases and risk
Explain authorization, validation, rollback, concurrency/idempotency, empty and failure states, UX accessibility, other risks. Explicitly distinguish untested cases.

## Required fixes (prioritized)
| Severity | Rule or test | Reproduction | Minimum proposed change | Retest |
|---|---|---|---|---|

## Evidence and limits
List executed commands/exit codes, unavailable tools, assumptions, coverage holes. State whether any tests were written, whether any feature code was changed (normally none), and verify the working tree is still uncommitted. No unsupported success claims.
