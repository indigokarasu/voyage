---
name: ocas-voyage
description: Voyage: travel planning, itinerary construction, and reservation management. Use when the user wants to plan a trip, build an itinerary, find lodging or restaurants, optimize travel logistics, or manage reservations. Trigger phrases: 'plan a trip', 'build itinerary', 'where to stay', 'restaurant recommendations for my trip', 'travel to', 'optimize my itinerary'. Do not use for generic travel inspiration, visa advice, or airfare-only optimization.
metadata: {"openclaw":{"emoji":"🧭"}}
---

# Voyage

Voyage builds travel itineraries with lodging, dining, and activity recommendations. It respects constraints (budget, dietary, pace), optimizes logistics, and produces reservation-ready plans.


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


## Commands

- `voyage.plan.trip` — create a full trip plan from destination, dates, and constraints
- `voyage.recommend.lodging` — lodging recommendations based on trip context
- `voyage.recommend.food` — restaurant recommendations based on route and preferences
- `voyage.recommend.activities` — activity recommendations based on interests and logistics
- `voyage.optimize.itinerary` — optimize an existing itinerary for feasibility and logistics
- `voyage.status` — current plan state, pending reservations, open decisions
- `voyage.journal` — write journal for the current run; called at end of every run


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
~/openclaw/data/ocas-voyage/
  config.json
  state.json
  events.jsonl
  decisions.jsonl
  plans/

~/openclaw/journals/ocas-voyage/
  YYYY-MM-DD/
    {run_id}.json
```


Default config.json:
```json
{
  "skill_id": "ocas-voyage",
  "skill_version": "2.2.0",
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

- Sift — web research for venue information and availability
- Taste — may read taste model for preference-aware recommendations
- Weave — may read social graph for trip companion context


## Journal outputs

Action Journal — all planning, recommendation, and reservation runs.


## Initialization

On first invocation of any Voyage command, run `voyage.init`:

1. Create `~/openclaw/data/ocas-voyage/` and subdirectories (`plans/`)
2. Write default `config.json` and `state.json` if absent
3. Create empty JSONL files: `events.jsonl`, `decisions.jsonl`
4. Create `~/openclaw/journals/ocas-voyage/`
5. Log initialization as a DecisionRecord in `decisions.jsonl`

Voyage is purely reactive. No cron jobs or heartbeat entries.


## Visibility

public


## Support file map

File | When to read
`references/voyage_schemas.md` | Before creating plans, itineraries, or reservations
`references/itinerary_constraints.md` | Before constraint application or optimization
`references/recommendation_style.md` | Before generating recommendations
`references/journal.md` | Before voyage.journal; at end of every run
