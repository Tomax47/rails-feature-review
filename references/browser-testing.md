# Development browser verification protocol

## Preconditions

- Obtain an authorized dev/staging/test URL from application configuration or user, and verify hostname/environment banner/credentials. Prefer localhost / loopback and dedicated test env. An arbitrary remote domain is **not** assumed safe. Never enter real credentials into unknown environments.
- Ensure isolated database, seed data, dedicated test account, fake/sandbox email/payment integrations, and permission to create test records. Inspect app routes and current requirements.
- Use a real browser (Playwright or approved browser-control tool). If not installed, try available supported browser tool. Do not claim a browser test from curl, source inspection or screenshot generation alone.
- Record actual browser/tool/version if available, viewport dimensions, app URL (redact tokens), user role and test data labels. Keep artifacts in repo-approved temp/report paths, not source directories; avoid saving secrets.

## Execute the user journey

1. Open route and confirm DOM is rendered and initial state consistent with requirements.
2. Run happy path using browser interactions (click/type/select), verify visible outcome, persisted behavior where inspectable, and correct redirect/status.
3. Submit invalid/missing/malformed values and verify both errors and no unintended persistence.
4. Try empty, long, boundary, duplicate and repeated-submit scenarios relevant to the feature.
5. Test unauthorized user/role and cross-account record attempts with sandbox identities, avoiding real user data.
6. Test any applicable loading/failure/refresh/back/navigation cases, relevant responsive layout and keyboard interactions.
7. Check browser console errors and failed network requests; identify which are unrelated existing issues; capture screenshot/evidence for key stages and failures.
8. Clean only isolated records you created **through known safe test teardown**, not through destructive DB shell commands. State what remains.

## Browser automation examples

Playwright in an existing JS testing project: reuse its configs, fixtures and browser installation. For Python environments, Playwright may be available; use the team's recommended browser test harness when present. If a test browser cannot access dev app due to network/session controls, mark E2E **BLOCKED** and specify URL/connectivity/auth needs. Do not bypass access controls.

## Applicability

- UI-bearing feature (HTML/JS/Jbuilder rendered into UI): browser E2E required to assert READY.
- API-only/backend feature: browser may be N/A with explicit justification; verify API via request/integration specs and, if dev endpoint is available and safe, actual authorized HTTP calls with appropriate sandbox controls.
- Cannot verify environment: no browser actions; report BLOCKED, never READY.
