# Feature test planning

Before adding tests, inventory feature requirements and compare existing coverage. Implement only missing high-value tests consistent with repo conventions. Avoid test code comments and unnecessary setup changes.

## Case selection

1. **Happy path**: expected authorized action persists correctly, returns correct response, UI renders correct state.
2. **Validation/boundaries**: blank, malformed, maximum/minimum, duplicates, missing records, invalid nested params, empty collection, pagination/filter edges where relevant.
3. **Authorization/tenancy**: unauthorized and unauthenticated requests, cross-account record lookup, different roles, missing permissions, 404/403 convention and no data leaks.
4. **Business failure**: organizer `context.fail!` propagates readable error; correct rollback of earlier DB writes; external failures do not falsely signal success.
5. **Background jobs**: `retry_on` receives raised retryable infrastructure exceptions; non-retryable discard/failure behavior; duplicate execution/idempotency; queued only after approved workflow boundaries; no real external calls.
6. **Presentation**: Jbuilder keys, partial consistency, decorator formatting, no SQL-building in ERB/Jbuilder; avoid N+1 and redundant queries where practical.
7. **UI state**: loading, errors, empty state, invalid form, keyboard focus, navigation/back, repeat submit, visual consistency, responsive layout as applicable.
8. **Regression**: neighboring flows plausibly affected by the diff and existing feature tests.

## Running tests

- Confirm commands, dependencies, test env and DB isolation; do not blindly run a custom script with destructive side effects.
- Record test file paths, command/exit, count passed/failed/skipped/pending, and failures. Capture full suite if practical; label not run explicitly.
- Never change production code during reviewer session. Report failed tests as findings and a minimal suggested fix.
- For async workflows test both expected context failures and unexpected infrastructure exception propagation; verify transaction rollback and idempotency instead of assuming them.
- In RSpec projects prefer existing specs and factories; in Minitest use existing fixtures and helpers. Do not create cosmetic tests for every branch just to increase count.
- New test file edits count as changes and must comply with minimal LOC and no comments. A test passing without executing assertions is not sufficient evidence.
