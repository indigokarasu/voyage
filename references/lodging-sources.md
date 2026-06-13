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

**Installation** (run once; skip if `mcp-marriott` already in MCP config):
```bash
npm install -g @striderlabs/mcp-marriott
```
Add to platform MCP config:
```json
{
  "mcpServers": {
    "marriott": {
      "command": "mcp-marriott"
    }
  }
}
```
Run OAuth login: `marriott.mobile_key` — opens browser for Bonvoy account login. Re-run if session expires.

Key commands:
- `marriott.search_hotels` — by location, dates, room count; optional brand/points filters
- `marriott.get_bonvoy_status` — points balance and elite tier
- `marriott.request_upgrade` — suite upgrade request for eligible members
- `marriott.mobile_key` — digital room access (also used for OAuth init)

Failure modes:
- OAuth session expired — re-run `marriott.mobile_key` to re-authenticate
- MCP not installed — skip silently, continue with Expedia and Marriott AI

## Marriott AI / FlyAI

No credentials required for basic use. For enhanced results, set the `FLYAI_API_KEY` environment variable (optional).

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

## 1Stay (MCP connector)

Hotel booking MCP server by Stayker (WPF Holdings, LLC). Completes real hotel reservations with confirmation numbers — not search-and-redirect. 300,000+ properties across 140+ countries, loyalty program eligible.

**MCP endpoint:** `https://mcp.stayker.com/mcp` — Streamable HTTP transport.

**Configuration:** Add to Hermes MCP config as connector `1stay` pointing to the endpoint URL. No credentials required for basic search; booking requires a 1Stay account (OAuth 2.0).

**Tools (8):**

| Tool | Type | Purpose |
|------|------|---------|
| `search_hotels` | Read-only | Search by location, dates, guests, optional filters (brand, price, amenities) |
| `get_hotel_details` | Read-only | Room types, amenities, images, live rates for a specific property |
| `book_hotel` | Idempotent | Create reservation → returns secure checkout URL |
| `lookup_booking` | Read-only | Look up reservation with identity verification (name + email) |
| `resend_confirmation` | Open-world | Resend confirmation email to guest |
| `get_booking` | Read-only | Look up reservation by booking ID or confirmation number |
| `cancel_booking` | Destructive, Idempotent | Cancel an existing reservation |
| `search_tools` | Read-only | List available 1Stay tools, optionally filtered by keyword |

**Booking workflow:**
1. `search_hotels` → present results
2. `get_hotel_details` → show room options, rates, cancellation policy
3. `book_hotel` → collect guest name/email/phone in conversation → returns secure checkout URL
4. Guest completes payment on PCI-compliant checkout page (URL valid ~30 min)
5. Confirmation email sent with real hotel confirmation number
6. `get_booking` / `lookup_booking` for post-booking management

**Failure modes:**
- MCP endpoint unreachable — skip 1Stay, continue with other sources
- OAuth not configured — `search_hotels` and `get_hotel_details` may still work; `book_hotel` will fail
- Checkout URL expires after ~30 minutes — treat as booking gate failure, re-book
- No update tool — changes require cancel + re-book pattern
- **Status: Unhealthy** (as of 2026-06-05) — endpoint may be intermittently unavailable

**Total cost note:** Returns live rates from travel distribution networks. Always re-check price via `get_hotel_details` before presenting as final. No resort fee issues (rates are from hotel PMS directly).

## Sift (open web research)

Delegation target for anything the lodging platforms don't cover: destination context, activity recommendations, restaurant picks, local knowledge, neighborhood comparisons.

Do not use Sift for hotel availability or pricing — use the dedicated lodging sources above.
