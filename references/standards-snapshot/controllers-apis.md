# Controllers & APIs — approved intent v0.2
- **CA-001 HARD:** Controllers manage requests, auth, permitted params, record retrieval, and responses; delegate business mutations to organizers.
- **CA-002 HARD:** Permit input using Rails strong parameters. Sanitize, normalize and transform attributes in interactors.
- **CA-003 HARD:** Explicitly authorize controller actions; generally `authorize :order` for index and `authorize @order` for member actions, adapted to resource and local conventions.
- **CA-004 STANDARD:** Use `before_action :set_order` and private record lookup helpers when appropriate; `@order = authorized_orders.find(params[:order_id])` is an accepted example, not an invariant param key.
- **CA-005 ALLOWED:** Read-only controller relations, scopes, filtering, pagination and private query helpers are permitted.
- **CA-006 STANDARD:** Structured JSON responses via Jbuilder templates, not new serializers by default.
- **CA-007 HARD:** Explicitly branch on organizer success/failure; choose correct HTTP response.
- **CA-008 ALLOWED:** Simple inline error JSON is acceptable; structured successful responses use Jbuilder.
- **CA-009 IMPLEMENTATION:** Match repo-specific Pundit / policy_scope / custom authorization helpers, Pagy API, params, response conventions. Do not guess which helper is used.

## Authorization nuance
`authorize` action checks and relation scoping are different concepts. Verify the actual helper; do not conflate `policy(relation)` with standard `policy_scope(relation)`.

## Field-tested authorization restriction
FT-002: Policy predicate methods must not fire SQL; Scope#resolve may build and query relations. An allowed controller query does not authorize a SQL query inside an individual policy rule.
