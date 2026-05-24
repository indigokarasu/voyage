---
name: ocas-voyage
description: >
  Voyage: travel planning, itinerary construction, reservation management,
  lodging search, and flight search. Parallel lodging search across Expedia,
  Marriott Bonvoy (Strider MCP), Marriott AI, and Google Hotels. Flight search
  via Google Flights (fli library). Uses Sift for destination research and
  optionally GoPlaces for location enrichment. Trigger phrases:
  'plan a trip', 'build itinerary', 'where to stay', 'find hotels in',
  'Marriott near', 'compare lodging', 'restaurant recommendations for my
  trip', 'travel to', 'optimize my itinerary', 'update voyage',
  'find flights', 'cheapest flights to', 'flight prices', 'fly from',
  'airfare to', 'best time to fly'. Do not use for
  generic travel inspiration, visa advice, or points-only optimization.
metadata:
  author: Indigo Karasu
  email: mx.indigo.karasu@gmail.com
  version: "2.8.0"
  tags: [travel, itinerary, lodging, flights]
  category: execution
license: MIT
---

# Voyage

Voyage builds complete, constraint-aware travel itineraries — taking a destination, dates, budget, dietary preferences, and pace, then assembling lodging, dining, and activity recommendations into a logistics-optimized plan that is ready for reservation without auto-booking anything. It never presents uncertain operating hours or availability as confirmed fact, and surfaces cost implications throughout so the plan remains honest about what it actually knows.

## When to use

- Plan a multi-day trip with itinerary
- Build or optimize a travel itinerary
- Recommend lodging, restaurants, or activities for a trip
- Search for flights (one-way, round-trip, multi-city)
- Find cheapest dates to fly for a trip
- Manage reservation planning and checklists
- Optimize an existing itinerary for feasibility

## When not to use

- Generic travel inspiration with no planning intent
- Points-only optimization (use Rally for mileage runs and award hacking)
- Visa, customs, or medical-travel compliance as primary task
- Presenting uncertain availability as confirmed facts

## Responsibility boundary

Voyage owns travel planning, itinerary construction, and reservation management.

Voyage does not own: web research (Sift), preference persistence (Taste), knowledge graph (Elephas), communications (Dispatch).

## Lodging search

All configured sources fire in parallel: Expedia (always available), Marriott Strider MCP (requires `mcp-marriott` + Bonvoy OAuth), Marriott AI (optional), Google Hotels (requires browser), and Sift (destination context). Results are merged and ranked by total real cost → loyalty value → cancellation flexibility → location fit.

- **GoPlaces** (optional): resolves ambiguous location input via geocoding. If not installed, flag ambiguity to the user.
- **Total cost rule:** Always surface headline price + taxes + mandatory fees + cancellation flexibility. Never present listing price as booking-final. See `references/total-cost.md`.
- **Booking gate rule:** Never present "ready to book" without price re-check, cancellation terms, and explicit user approval. See `references/booking-gates.md`.

See `references/lodging-sources.md` for per-source patterns, auth setup, and failure modes.

## Flight search

Uses the `fli` Python library (PyPI: `flights`) to query Google Flights directly — no API key or browser required. Run via Hermes venv: `/usr/local/lib/hermes-agent/venv/bin/python3 -c "..."`.

**Capabilities:** one-way, round-trip, multi-city, date-range search, multi-airport.

**Filters:** stops, cabin class, sort order, max duration, airline, bags, price limit, time restrictions, emissions.

**Presentation:** Always show price, currency, stops, duration, airline, flight numbers, local times. Include "as of" timestamp. Never present prices as guaranteed.

See `references/flights.md` for detailed API patterns, airport resolution, date search, and failure modes.

## Ontology types

Voyage works with these types from `spec-ocas-ontology.md`:

- **Place** — venues, airports, hotels, restaurants, attractions
- **Concept/Event** — trips and travel events (departure, arrival, check-in, activity)
- **Concept/Action** — booking actions (reserved, cancelled, modified)
- **Entity/Person** — travel companions

Voyage maintains trip and itinerary state in `{agent_root}/commons/data/ocas-voyage/`. Entity observations are recorded in journal outputs for downstream Chronicle ingestion.

## Commands

- `voyage.plan.trip` — create a full trip plan from destination, dates, and constraints
- `voyage.recommend.lodging` — parallel lodging search; returns unified comparison table
- `voyage.recommend.flights` — Google Flights search; returns structured options with pricing
- `voyage.recommend.food` — restaurant recommendations based on route and preferences
- `voyage.recommend.activities` — activity recommendations based on interests and logistics
- `voyage.optimize.itinerary` — optimize an existing itinerary for feasibility
- `voyage.status` — current plan state, pending reservations, open decisions
- `voyage.journal` — write journal for the current run; called at end of every run
- `voyage.update` — pull latest from GitHub source; preserves journals and data

## Run completion

After every Voyage command:

1. Persist plan state, recommendations, and reservation details to local files
2. Log material decisions to `decisions.jsonl`
3. Write journal via `voyage.journal`

## Invariants

- Never present uncertain operating hours or availability as confirmed
- Respect dietary constraints in all food recommendations
- Budget awareness throughout — surface cost implications
- Reservation-ready means actionable, not auto-booked (unless explicitly enabled)

## Storage layout

```
{agent_root}/commons/data/ocas-voyage/
  config.json
  state.json
  events.jsonl
  decisions.jsonl
  plans/

{agent_root}/commons/journals/ocas-voyage/
  YYYY-MM-DD/
    {run_id}.json
```

Default `config.json`:
```json
{
  "skill_id": "ocas-voyage",
  "skill_version": "2.3.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "defaults": {
    "diet": "vegetarian",
    "pace": "moderate",
    "auto_book": false
  },
  "retention": {
    "days": 0,
    "max_records": 10000
  }
}
```

## OKRs

```yaml
skill_okrs:
  - name: itinerary_feasibility
    metric: fraction of itinerary days passing logistics feasibility checks
    direction: maximize
    target: 0.95
    evaluation_window: 30_runs
  - name: constraint_compliance
    metric: fraction of recommendations satisfying all stated constraints
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs
  - name: availability_honesty
    metric: fraction of uncertain availability items flagged appropriately
    direction: maximize
    target: 1.0
    evaluation_window: 30_runs
```

## Optional skill cooperation

- **Sift** — all open web research: destination info, restaurant picks, activity recommendations, local knowledge
- **GoPlaces** (`ocas-goplaces`) — location enrichment: geocoding, distance checks, neighborhood context. Check at runtime; if not installed, flag ambiguity to user.
- **Taste** — preference-aware recommendations (read-only)
- **Weave** — trip companion context from social graph (read-only)
- **Elephas** — entity observations emitted via journal

## Journal outputs

Action Journal — all planning, recommendation, and reservation runs.

When entities are encountered, include structured observations in `decision.payload`:

- `entities_observed` — list of entities (type, name, context)
- `relationships_observed` — connections between entities
- `preferences_observed` — user preferences inferred from planning choices

Each entity observation must include `user_relevance`: `user` (directly related to user's world), `agent_only` (incidental), or `unknown`.

## Initialization

On first invocation, run `voyage.init`:

1. Create data/journal directories and default config/state files
2. Create empty JSONL files: `events.jsonl`, `decisions.jsonl`
3. Register cron job `voyage:update` if not already present
4. Log initialization as a DecisionRecord
5. Record availability of optional components (Marriott MCP, flights library, GoPlaces) in config

See `references/lodging-sources.md` for Marriott Strider MCP setup. See `references/flights.md` for flights library installation and verification.

## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `voyage:update` | cron | `0 0 * * *` (midnight daily) | `voyage.update` |

## Self-update

`voyage.update` pulls the latest package from GitHub. Runs silently — no output unless the version changed or an error occurred. On success: `I updated Voyage from version {old} to {new}`.

## Visibility

public

## Gotchas

- **GoPlaces is optional** — If not installed, flag location ambiguity to the user rather than guessing.
- **Total cost must be surfaced** — Always show headline price + taxes + mandatory fees + cancellation flexibility.
- **Flight prices are volatile** — Always include an "as of" timestamp. Never present prices as guaranteed.
- **Multi-city flight search may timeout** — Search legs individually for complex routes.
- **Booking gate requires explicit approval** — Never present "ready to book" without price re-check, cancellation terms, and user confirmation.
- **Marriott Strider MCP requires setup** — See `references/lodging-sources.md` for OAuth and installation steps.

## Support file map

| File | When to read |
|---|---|
| `references/voyage_schemas.md` | Before creating plans, itineraries, or reservations |
| `references/itinerary_constraints.md` | Before constraint application or optimization |
| `references/recommendation_style.md` | Before generating recommendations |
| `references/journal.md` | Before voyage.journal; at end of every run |
| `references/flights.md` | Before any flight search; contains API patterns, airport resolution, failure modes |
| `references/lodging-sources.md` | Before lodging search; per-source patterns and failure modes |
