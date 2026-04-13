---
name: ocas-voyage
description: >
  Voyage: travel planning, itinerary construction, reservation management, and
  lodging search. Parallel lodging search across Expedia, Marriott Bonvoy
  (Strider MCP), Marriott AI, and Google Hotels. Uses Sift for destination
  research and optionally GoPlaces for location enrichment. Trigger phrases:
  'plan a trip', 'build itinerary', 'where to stay', 'find hotels in',
  'Marriott near', 'compare lodging', 'restaurant recommendations for my
  trip', 'travel to', 'optimize my itinerary', 'update voyage'. Do not use for
  generic travel inspiration, visa advice, or airfare-only optimization.
metadata:
  author: Indigo Karasu
  email: mx.indigo.karasu@gmail.com
  version: "2.7.5"
  hermes:
    tags: [travel, itinerary, lodging]
    category: execution
    cron:
      - name: "voyage:update"
        schedule: "0 0 * * *"
        command: "voyage.update"
  openclaw:
    skill_type: system
    visibility: public
    filesystem:
      read:
        - "{agent_root}/commons/data/ocas-voyage/"
        - "{agent_root}/commons/journals/ocas-voyage/"
        - "{agent_root}/commons/data/ocas-taste/"
        - "{agent_root}/commons/data/ocas-weave/"
      write:
        - "{agent_root}/commons/data/ocas-voyage/"
        - "{agent_root}/commons/data/ocas-voyage/itineraries/"
        - "{agent_root}/commons/journals/ocas-voyage/"
    self_update:
      source: "https://github.com/indigokarasu/voyage"
      mechanism: "version-checked tarball from GitHub via gh CLI"
      command: "voyage.update"
      requires_binaries: [gh, tar, python3]
    requires:
      mcp:
        - name: "marriott"
          description: "Marriott Bonvoy hotel search, loyalty points, upgrades, and mobile key via Strider MCP"
          required: false
      capabilities:
        - "web-browsing"
      credentials:
        - name: "flyai_api_key"
          description: "FlyAI API key for enhanced Marriott AI results and package search"
          required: false
    cron:
      - name: "voyage:update"
        schedule: "0 0 * * *"
        command: "voyage.update"
---

# Voyage

Voyage builds complete, constraint-aware travel itineraries — taking a destination, dates, budget, dietary preferences, and pace, then assembling lodging, dining, and activity recommendations into a logistics-optimized plan that is ready for reservation without auto-booking anything. It never presents uncertain operating hours or availability as confirmed fact, and surfaces cost implications throughout so the plan remains honest about what it actually knows.


## When to use

- Plan a multi-day trip with itinerary
- Build or optimize a travel itinerary
- Recommend lodging, restaurants, or activities for a trip
- Manage reservation planning and checklists
- Optimize an existing itinerary for feasibility


## When not to use

- Generic travel inspiration with no planning intent
- Airfare-only or points-only optimization
- Visa, customs, or medical-travel compliance as primary task
- Presenting uncertain availability as confirmed facts


## Responsibility boundary

Voyage owns travel planning, itinerary construction, and reservation management.

Voyage does not own: web research (Sift), preference persistence (Taste), knowledge graph (Elephas), communications (Dispatch).


## Lodging search

When the user needs lodging recommendations, all configured sources fire in parallel. Results are merged into a unified comparison table.

| Source | Provides | Requires |
|--------|----------|----------|
| **Expedia web** | Hotel/package search, total-cost breakdown | None — always available |
| **Marriott Strider MCP** | Real Bonvoy inventory, award nights, elite upgrades, mobile key | `mcp-marriott` installed + Bonvoy OAuth login |
| **Marriott AI / FlyAI** | Package bundling, real-time pricing, POI enrichment | None; `FLYAI_API_KEY` optional for enhanced results |
| **Google Hotels** | Structured results table (price/rating/amenities), search-only | `agent-browser` CLI |
| **Sift** | Destination info, activities, local knowledge, anything platforms don't cover | Sift skill installed |

Results ranked by: total real cost → loyalty/points value → cancellation flexibility → location fit.

See `references/lodging-sources.md` for per-source patterns and failure modes.

**GoPlaces cooperation (optional):** If `ocas-goplaces` is installed, Voyage calls it to resolve ambiguous location input before search (geocoding, distance checks, neighborhood context). If not installed, Voyage surfaces unresolved location ambiguity to the user rather than guessing. Voyage checks for GoPlaces at runtime using the platform skill registry.

**Total cost rule:** Always surface headline price + taxes + mandatory fees + cancellation flexibility before recommending. Never present a listing price as booking-final. See `references/total-cost.md`.

**Booking gate rule:** Never present an option as "ready to book" without: price re-check complete, cancellation terms stated, and explicit user approval. See `references/booking-gates.md`.


## Ontology types

Voyage works with these types from `spec-ocas-ontology.md`:

- **Place** — venues, airports, hotels, restaurants, attractions. Extracted during destination research and itinerary construction.
- **Concept/Event** — trips and travel events (departure, arrival, check-in, activity). Stored in itinerary records.
- **Concept/Action** — booking actions (reserved, cancelled, modified). Recorded in Action Journals.
- **Entity/Person** — travel companions mentioned during trip planning.

Voyage maintains its own trip and itinerary state in `{agent_root}/commons/data/ocas-voyage/`. Entity observations are recorded in journal outputs for downstream Chronicle ingestion.


## Commands

- `voyage.plan.trip` — create a full trip plan from destination, dates, and constraints
- `voyage.recommend.lodging` — parallel lodging search across Expedia, Marriott Strider, Marriott AI, and Google Hotels. Returns unified comparison table with total-cost breakdown and booking-gate summary.
- `voyage.recommend.food` — restaurant recommendations based on route and preferences
- `voyage.recommend.activities` — activity recommendations based on interests and logistics
- `voyage.optimize.itinerary` — optimize an existing itinerary for feasibility and logistics
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


Default config.json:
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

Universal OKRs from spec-ocas-journal.md apply to all runs.

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

- **Sift** — all open web research: destination info, restaurant picks, activity recommendations, local knowledge. Voyage delegates to Sift via Sift's search stack; does not do raw web searches itself.
- **GoPlaces** (`ocas-goplaces`) — location enrichment: geocoding, distance-to-airport/center, neighborhood context, disambiguation of ambiguous location input. Check at runtime: `platform skill registry query | grep goplaces`. If not installed, flag ambiguity to user.
- **Taste** — preference-aware recommendations (read-only)
- **Weave** — trip companion context from social graph (read-only)
- **Elephas** — entity observations emitted via journal


## Journal outputs

Action Journal — all planning, recommendation, and reservation runs.

When entities are encountered during a run, include structured entity observations in `decision.payload`:

- `entities_observed` — list of entities encountered (Place, Concept/Event, Concept/Action, Entity/Person), each with type, name, and context
- `relationships_observed` — connections between entities (e.g., a person associated with a trip, a restaurant located in a destination)
- `preferences_observed` — user preferences inferred from planning choices (e.g., budget range, dietary needs, pace preference)

Each entity observation must include a `user_relevance` field:
- `user` — entity is directly related to the user's world (destinations, hotels, companions, reservations). Most Voyage entities are `user`-relevant since they represent the user's actual travel plans and destinations.
- `agent_only` — entity encountered incidentally (e.g., a landmark mentioned only as a routing waypoint, not as a destination)
- `unknown` — relevance is unclear


## Initialization

On first invocation of any Voyage command, run `voyage.init`:

1. Create `{agent_root}/commons/data/ocas-voyage/` and subdirectories (`plans/`, `itineraries/`)
2. Write default `config.json` and `state.json` if absent
3. Create empty JSONL files: `events.jsonl`, `decisions.jsonl`
4. Create `{agent_root}/commons/journals/ocas-voyage/`
5. Register cron job `voyage:update` if not already present (check the platform scheduling registry first)
6. Log initialization as a DecisionRecord in `decisions.jsonl`
7. **Marriott Strider MCP setup** (run once; skip if `mcp-marriott` already in MCP config):
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
8. **Google Hotels setup**: Google Hotels search requires web browsing access. If the system provides web browsing capability, this is available automatically. If unavailable, Expedia and Marriott cover this path.
9. **Optional credentials** (skip if not available):
   - `FLYAI_API_KEY` — set for enhanced Marriott AI results; skill works without it
10. **GoPlaces check**:
    - Run: `platform skill registry query | grep goplaces`
    - Record result in `{agent_root}/commons/data/ocas-voyage/config.json` under `"goplaces_available": true/false`

## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `voyage:update` | cron | `0 0 * * *` (midnight daily) | `voyage.update` |

```
# Task declared in SKILL.md frontmatter metadata.{platform}.cron
```


## Self-update

`voyage.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

1. Read `source:` from frontmatter → extract `{owner}/{repo}` from URL
2. Read local version from SKILL.md frontmatter `metadata.version`
3. Fetch remote version from SKILL.md frontmatter: `gh api "repos/{owner}/{repo}/contents/SKILL.md" --jq '.content' | base64 -d | grep 'version:' | head -1 | sed 's/.*"\(.*\)".*/\1/'`
4. If remote version equals local version → stop silently
5. Download and install:
   ```bash
   TMPDIR=$(mktemp -d)
   gh api "repos/{owner}/{repo}/tarball/main" > "$TMPDIR/archive.tar.gz"
   mkdir "$TMPDIR/extracted"
   tar xzf "$TMPDIR/archive.tar.gz" -C "$TMPDIR/extracted" --strip-components=1
   cp -R "$TMPDIR/extracted/"* ./
   rm -rf "$TMPDIR"
   ```
6. On failure → retry once. If second attempt fails, report the error and stop.
7. Output exactly: `I updated Voyage from version {old} to {new}`


## Visibility

public


## Support file map

| File | When to read |
|---|---|
| `references/voyage_schemas.md` | Before creating plans, itineraries, or reservations |
| `references/itinerary_constraints.md` | Before constraint application or optimization |
| `references/recommendation_style.md` | Before generating recommendations |
| `references/journal.md` | Before voyage.journal; at end of every run |

## Update command

This skill self-updates every 24 hours via:

```bash
voyage.update
```

This pulls the latest version from GitHub and restarts the skill's background tasks if applicable.
