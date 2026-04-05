# Lodging Sources

Per-source patterns and failure modes for `voyage.recommend.lodging`.

## Expedia (web mode)

Always available. Navigate `expedia.com` via browser tools.

Search pattern: destination + dates + traveler count → filter by property type, budget, cancellation → open 3–5 candidates → verify fees and policies on candidate page.

Failure modes:
- Price changes between search and checkout — re-check before recommending
- Package savings hide weak flight shape — evaluate separately
- Resort fees not shown until checkout — explicitly check candidate page

## Marriott Strider MCP (`mcp-marriott`)

Requires `@striderlabs/mcp-marriott` installed and Bonvoy OAuth active.

Key commands:
- `marriott.search_hotels` — by location, dates, room count; optional brand/points filters
- `marriott.get_bonvoy_status` — points balance and elite tier
- `marriott.request_upgrade` — suite upgrade request for eligible members
- `marriott.mobile_key` — digital room access (also used for OAuth init)

Failure modes:
- OAuth session expired — re-run `marriott.mobile_key` to re-authenticate
- MCP not installed — skip silently, continue with Expedia and Marriott AI

## Marriott AI / FlyAI

No credentials required; `FLYAI_API_KEY` optional for enhanced results.

Key commands:
- `search-marriott-hotel` — Marriott properties with real-time pricing
- `search-marriott-package` — bundled deals
- `search-poi` — points of interest near destination (useful for itinerary enrichment)

Output: single-line JSON; pipe through `jq` for structured display. Present as comparison table.

Failure modes:
- FlyAI service unavailable — skip, continue with other sources
- Package savings require date stability — note cancellation risk

## Google Hotels (agent-browser)

Requires `agent-browser` CLI. Search-only; cannot complete bookings.

Pattern: encode dates → open Google Hotels URL with location and encoded dates → snapshot results → extract structured table.

Session: use `--session hotels` to isolate.

Failure modes:
- `agent-browser` not installed — skip silently
- DOM structure changes — use snapshot extraction, not fragile selectors

## Sift (open web research)

Delegation target for anything the lodging platforms don't cover: destination context, activity recommendations, restaurant picks, local knowledge, neighborhood comparisons.

Do not use Sift for hotel availability or pricing — use the dedicated lodging sources above.
