# Background Jobs — approved intent v0.2
- **BJ-001 HARD:** Regular jobs delegate business execution to organizers; no business calculations, persistence, or unrelated orchestration inside `perform`.
- **BJ-002 ALLOWED:** Persisted ActiveRecord objects (GlobalID) and primitive IDs may be job args. Match repository and organizer API, considering missing/deleted records.
- **BJ-003 CONDITIONAL:** Select `retry_on` and `discard_on` according to error categories; no universal retry policy.
- **BJ-004 HARD:** Protect non-repeatable side effects against duplicate or concurrent job execution. Validate behavior, not just existence of an idempotency key.
- **BJ-005 OPTION:** Persist due work in a dedicated table and use recurring jobs if business scheduling needs durability and visibility. Not mandatory for all delays.
- **BJ-006 HARD:** App workflow job enqueue from organizer `after` hooks; recurring scheduler infrastructure is an exception.
- **BJ-007 CONDITIONAL EXCEPTION:** Recurring jobs may select eligible top-level records and `find_each` them, calling one organizer per record. Detailed due-record queries and business processing stay in interactors.
- **BJ-008 HARD:** Let retryable infrastructure exceptions propagate to Active Job `retry_on` (supersedes old blanket OI-008 rescue wording).
- **BJ-009 HARD:** Ask rather than improvise unclear retries, scheduling, serialization, or idempotency.

## Required integration checks
Retryable timeout escapes organizer; nonretryable business failure produces context `error:`; retries do not duplicate side effects; failure in a batch does not unintentionally repeat completed work. Inspect local adapters and retry config.
