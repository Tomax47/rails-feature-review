# Review matrix — apply according to changes

Use the newest installed Engineering Standards skill as authority. The snapshot shipped with this reviewer is a fall-back baseline only. Record actual version and any deviations. A row can be N/A only with a reason.

| Area | Rules | Reviewer must verify |
|---|---|---|
| Global operations | FT-001 | No risky Git commands ever invoked; only read-only inspection; no unauthorized remote side effects. |
| Pundit | FT-002, AR-009, CA-003 | Predicates do not trigger SQL (directly or indirectly); SQL belongs in `Scope#resolve`; action/record authorization is present. Do not ban scopes merely for constructing SQL. |
| Jumpstart | FT-003 | `lib/jumpstart/` unchanged; legitimate overrides live in `app/` following repo patterns. |
| Views | FT-004, VW-001..007 | No ERB local/instance assignments; Jbuilder partials; decorators format; no new query construction in views; association preload/N+1; no workflows in templates. |
| Change hygiene | FT-005..008 | No newly added comments; exact source replication on copy requests; styling matches adjacent code; minimum relevant changed lines. |
| ActiveRecord | AR-001..009 | Business logic separated; validations and DB constraints; callbacks; scopes; no job scheduling from models; approval for model methods. |
| Workflow | OI-001..010 | Organizer composes interactors, no nested organizers/interactor-to-interactor calls; after hooks only schedule jobs; context fail string; transactional atomicity; retryable infrastructure exceptions propagate. |
| Jobs | BJ-001..009 | Thin jobs with documented batch selection exception; args match conventions; retry_on/discard_on; idempotency; enqueue placement; recurring processing. |
| Controllers/API | CA-001..009 | Authorization, permitted params, organizer delegation, explicit result branching, read-only relation preparation, Jbuilder success and allowed inline error JSON. |
| Other | repository requirements | Existing app conventions, minimal changes, safe migrations, accessibility, performance and security issues relevant to feature. Do not invent new product requirements. |

For each applicable rule: capture PASS/FAIL/UNVERIFIED/N/A, file:line or test evidence, rationale, and proposed correction. Heuristic static detections are leads, never proof of compliance. Explicitly check source-diff as well as test additions.

Important distinction: Pundit `.exists?`, `.count`, `.pluck`, `.first`, `.find`, `.load`, iteration etc. may trigger SQL in predicate context, including through helper calls. `Scope#resolve` is an allowed query-building location but still requires authorization correctness and privacy. Distinguish `record.association.loaded?` from record retrieval; inspect actual behavior.
