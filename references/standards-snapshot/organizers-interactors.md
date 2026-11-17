# Organizers & Interactors — approved intent v0.3
Framework: collectiveidea `Interactor` and `Interactor::Organizer`; repo extensions unknown.
- **OI-001 HARD:** Organizers compose interactors, never organizers; no organizer-to-organizer direct calls.
- **OI-002 HARD:** Interactors never call interactors. Compose steps in organizer `organize` declarations.
- **OI-003 ARCHITECTURE:** Each interactor owns one well-defined operation.
- **OI-004 CONDITIONAL:** Reuse a focused interactor in multiple organizers for workflow steps; extract pure utility/calculation into plain Ruby object where appropriate.
- **OI-005 HARD:** Organizer `after` blocks may only schedule jobs; no persistence, API, analytics, or other business logic.
- **OI-006 CONDITIONAL:** `before` and `around` hooks may handle technical concerns, not business steps.
- **OI-007 HARD:** Jobs delegate to organizers for ordinary async workflows; originating organizer schedules downstream jobs in `after`.
- **OI-008 HARD, AMENDED:** Use `context.fail!(error: human_readable_string)` for expected business failures. Catch and convert unexpected *non-retryable* exceptions where approved. **Do not catch and swallow retryable infrastructure exceptions** that should reach Active Job `retry_on`. Unknown classifications require clarification. Sanitization/exception boundaries require repo inspection.
- **OI-009 HARD INTENT; IMPLEMENTATION UNVERIFIED:** Atomic DB workflow writes must roll back together on interactor failure. Do not assume `Interactor::Organizer` alone provides transaction atomicity; inspect custom transaction mechanism and test `context.fail!` rollback.
- **OI-010 IMPLEMENTATION:** Respect existing collectiveidea framework and repository extensions.
