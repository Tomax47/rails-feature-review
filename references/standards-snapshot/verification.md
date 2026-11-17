# Cross-domain review and verification protocol
## Governance
Rule changes require code-style review. Deviations from approved rules require explicit human approval specifying rule ID, change scope, justification and owner. Existing violations are not automatic approvals. Do not silently add exemptions.
## Verification status
Each check must be one of PASS, FAIL, UNVERIFIED. A heuristic script cannot assert conformance to architecture semantics. Strict completion requires no FAIL and no unresolved blocking UNVERIFIED. Escalate missing prerequisites; do not assume silent acceptance.
## Required repository evidence (sanitized)
1. Gemfile/lock excerpts (Rails, Interactor, Active Job adapter, Pundit, Pagy, Jbuilder, decorator lib).
2. Model and migration/schema example; exact generator commands if audited.
3. Organizer, two interactors, transaction concern/wrapper, and failure/rollback tests.
4. Ordinary job with `retry_on`, recurring job with batching, scheduler config and idempotency tests.
5. Controller with auth helper, `set_record`, strong params, Pagy, result branches.
6. Jbuilder index/show/shared partial; HTML partial and decorator.
Strip credentials and customer data; do not package private app code into shared skill unless authorized.
## Dependency map
Models -> organizers/interactors; jobs -> organizers, transactions and retries; controllers -> organizers, authorization and Jbuilder; views -> controllers and decorators.
## Acceptance tasks
(1) New model migration using generator only (requires command trace); (2) organizer with interactor composition and enqueue in after; (3) job with retryable timeout and no swallowed exception; (4) index/show controller with proper authorization and Jbuilder partial; (5) view with preloaded relationships; (6) intentionally invalid callback or interactor chain; (7) ambiguous transaction mechanism must trigger clarification.
