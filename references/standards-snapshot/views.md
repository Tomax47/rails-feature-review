# Views & Jbuilder — approved intent v0.1
- **VW-001 STANDARD:** Jbuilder templates define structured JSON responses.
- **VW-002 STANDARD:** Extract shared resource JSON representations into Jbuilder partials across index/show/etc.
- **VW-003 HARD:** Presentation computations and formatting belong in decorators; Jbuilder assembles fields rather than computing display values.
- **VW-004 HARD:** Do not build queries inside HTML or Jbuilder templates. Prepare data in controllers or other approved layers.
- **VW-005 STANDARD:** Reusable HTML markup belongs in Rails partials.
- **VW-006 HARD:** Views do not mutate business data, invoke business workflows or make business authorization decisions; approved as an explicit cross-domain implication.
- **VW-007 IMPLEMENTATION:** Inspect adjacent templates, partials, decorators and response conventions.

## Important exception/verification
Consuming a preloaded association in a view is not inherently a new query. Verify eager loading, query count and N+1 behavior before approving collection templates.

## Field-tested ERB restriction
FT-004: Do not add variable initialization or assignments in ERB templates, including locals and instance variables. Prepare them in controller/business/decorator layers and pass them to the view. FT-007 preserves styling.
