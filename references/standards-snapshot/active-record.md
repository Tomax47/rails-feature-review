# Models & ActiveRecord — approved intent v0.3
- **AR-001 HARD:** No multi-step business workflow/orchestration inside ActiveRecord models; use interactors and organizers.
- **AR-002 APPROVAL:** Avoid custom instance methods. Pure reusable predicates are possible only with explicit approval; prefer the correct dedicated abstraction. Never infer permission from duplication.
- **AR-003 HARD:** Model validations concern the model's own attributes; cross-record eligibility and business requirements belong in interactors.
- **AR-004 HARD:** Match applicable model-level integrity validations with suitable database constraints (presence/non-null, uniqueness/unique indexes), where supported and appropriate.
- **AR-005 APPROVAL:** No newly introduced custom ActiveRecord callbacks without explicit approval. In particular never trigger jobs or business operations from model callbacks; prefer sanitization interactors.
- **AR-006 PREFERENCE:** Prefer scopes for reusable queries, including complex joins/aggregation. Do not introduce query objects solely based on scope length.
- **AR-007 PREFERENCE:** Put presentation computations and formatting in decorators, not model methods.
- **AR-008 HARD:** Schedule workflow jobs from organizer `after` hooks through established transaction-safe mechanisms, which have not yet been verified in repository code.
- **AR-009 HARD (cross-domain policy boundary):** Policies authorize only; no database queries or business eligibility logic in policies. Full policy domain deferred to Release 2.

## Initial Rails generation expectation — not yet separately reviewed as numbered rule
Use Rails generators and migration commands to create and apply migrations and schema changes; avoid manual modifications to generated migration/schema files. Verify command provenance with project tooling; final-file inspection cannot prove provenance. Ask if the generator cannot express a needed operation.

## Unverified implementation details
Inspect transaction hooks, schema/database adapter, decorators, scopes, authorization helpers, and migration workflow before enforcement.
