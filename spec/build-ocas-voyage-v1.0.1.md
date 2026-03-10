# Build Specification: `ocas-voyage` v1.0.1

## Skill identity
- Skill name: `ocas-voyage`
- Version: `1.0.1`
- Author: `Indigo Karasu`
- Email: `mx.indigo.karasu@gmail.com`
- Skill type: `workflow`

## One-sentence build objective
Build a complete, ready-to-install Agent Skill package that turns constrained travel requests into feasible, optimized travel plans with lodging, dining, activities, reservation strategy, and a day-by-day itinerary backed by explicit decision logic.

## Build rules
The coder must build a real Agent Skill package, not a design memo, summary, or partial scaffold.

The package must be self-contained and installable.

The package must preserve the original Voyage functional surface, including:
- destination discovery
- itinerary optimization
- lodging recommendation
- dining strategy
- reservation planning
- decision explanations
- command interface for trip planning and sub-recommendation flows
- local storage for state, events, decisions, and saved plans
- conservative behavior when data confidence is low

Do not compress away functionality for the sake of brevity.

Keep `SKILL.md` operational and routing-aware, but include enough precision that a coder LLM can build the package correctly.

The skill must plan feasible trips rather than aspirational travel moodboards. It should prefer constraint satisfaction, pacing realism, and reservation practicality over novelty for its own sake.

## Critical installability requirement
`SKILL.md` must begin on line 1 with valid YAML frontmatter delimited by `---`.

The YAML frontmatter must be syntactically valid and parseable.

Do not place any prose, comments, blank lines, code fences, or BOM characters before the opening `---`.

The build is invalid if `SKILL.md` does not start with valid YAML frontmatter.

## Required package output
Produce this package:

```text
ocas-voyage/
  skill.json
  SKILL.md
  references/
    voyage_schemas.md
    itinerary_constraints.md
    recommendation_style.md
```

Do not add `scripts/` unless implementation genuinely requires them. This spec does not require scripts.

## `skill.json` requirements
Create a valid `skill.json` with at least these fields:
- `name`: `ocas-voyage`
- `version`: `1.0.1`
- `description`: routing-optimized description
- `author`: `Indigo Karasu`
- `email`: `mx.indigo.karasu@gmail.com`

The description must make clear that Voyage should be used when the user wants:
- a trip plan for a destination
- a structured itinerary with activities, meals, and travel pacing
- lodging recommendations tied to trip geography or loyalty preferences
- restaurant recommendations integrated into a travel plan
- reservation timing or booking strategy for a trip
- optimization of a draft itinerary against real-world constraints

The description must also make clear that Voyage is not for:
- generic destination essays with no planning intent
- pure airfare deal hunting without itinerary construction
- immigration, visa, or legal-travel advice beyond basic flagging
- live booking execution unless another system handles that explicitly

## `SKILL.md` requirements
### YAML frontmatter
`SKILL.md` must start exactly with valid YAML frontmatter. Include fields that match the package identity and runtime intent.

Use frontmatter shaped like this, with valid YAML syntax:

```yaml
---
name: voyage
version: 1.0.1
description: >
  Use this skill when the user wants a structured trip plan, optimized travel
  itinerary, lodging shortlist, dining plan, reservation checklist, or
  destination-specific schedule that must respect timing, transit, and pacing
  constraints.
metadata:
  openclaw:
    id: ocas-voyage
    emoji: "✈️"
    requires:
      bins: ["python3"]
    storage:
      root: ".voyage"
    permissions:
      os: []
      network: ["required:travel_research"]
---
```

The coder may add additional valid YAML fields if useful, but must keep the YAML parseable.

### Required `SKILL.md` sections
After the YAML frontmatter, `SKILL.md` must contain these sections in this order:
1. `# Voyage (ocas-voyage) — Travel Planning Skill`
2. `## When to use`
3. `## When not to use`
4. `## Core promise`
5. `## Invariants`
6. `## External interface`
7. `## Input contract`
8. `## Planning workflow`
9. `## Optimization rules`
10. `## Output requirements`
11. `## Support file map`
12. `## Storage layout`
13. `## Validation rules`

### Section content requirements
#### `## When to use`
Must include realistic trigger language such as:
- plan a trip to Kyoto for 5 days
- build me an itinerary for Tokyo and Osaka
- recommend where to stay based on this trip plan
- optimize this draft itinerary so it is actually feasible
- suggest restaurants that fit the route and reservation reality
- make a reservation checklist for this trip

#### `## When not to use`
Must explicitly exclude nearby non-trigger cases such as:
- generic travel inspiration with no planning intent
- isolated airfare-only or points-only optimization
- pure destination history writeups
- legal, customs, visa, or medical-travel compliance advice as the primary task
- pretending uncertain operating hours, reservation availability, or travel times are confirmed facts

#### `## Core promise`
State clearly that Voyage converts a destination plus constraints into a feasible, optimized, explainable travel plan.

#### `## Invariants`
Include these non-negotiable rules:
- feasibility first
- hard constraints outrank soft preferences
- schedules must include buffers and rest
- uncertain facts must be labeled
- unsafe or low-confidence areas should be avoided or flagged when such data is available
- reservation-critical items must be surfaced clearly
- if confidence is low, planning mode becomes conservative

#### `## External interface`
Preserve these primary and secondary commands:
- `voyage.plan.trip`
- `voyage.recommend.lodging`
- `voyage.recommend.food`
- `voyage.recommend.activities`
- `voyage.optimize.itinerary`

For each command, define:
- purpose
- minimum input
- major optional input
- return shape
- whether it writes state

#### `## Input contract`
Define at minimum these accepted input fields for trip planning:
- `destination`
- `trip_length`
- `arrival_date`
- `departure_date`
- `interests`
- `budget`
- `food_preferences`
- `travel_style`
- `lodging_preferences`
- `season`

The skill must support minimal-input planning using only:
- destination
- either trip length or arrival/departure dates

The input contract must also define the core structured objects from the original skill intent:
- `TravelPlan`
- `ScheduleBlock`
- `DecisionRecord`
- candidate destination/lodging/dining/activity items

#### `## Planning workflow`
Describe the ordered process:
1. normalize request and dates
2. derive planning window and daily usable time
3. gather candidate activities, neighborhoods, restaurants, and lodging options
4. score candidates against constraints and goals
5. construct day-level schedule blocks with meals, travel, rest, and buffers
6. optimize for feasibility first, then distance, pacing, and diversity
7. create lodging shortlist and dining strategy tied to the itinerary
8. generate reservation checklist with deadlines and backups
9. record decision log with alternatives and confidence
10. persist plan, events, and decisions locally

#### `## Optimization rules`
Preserve the original hard and soft constraints.

Hard constraints must include:
- opening hours
- transit feasibility
- meal windows
- travel time
- day length

Soft constraints must include:
- minimize travel distance
- diversity of experiences
- pacing balance
- reservation feasibility

Also require:
- no impossible backtracking schedules
- no stacking of too many reservation-dependent items in one time window
- dining should reflect both quality and route practicality
- lodging selection must consider neighborhood fit, itinerary proximity, transit access, price tier, and loyalty preferences when provided

#### `## Output requirements`
The skill must be able to output all of the original categories:
- transit recommendations
- lodging shortlist
- restaurant recommendations
- activity recommendations
- day-by-day itinerary
- reservation checklist
- decision explanations

The main `TravelPlan` output must include at least:
- destination
- trip length or dates
- lodging recommendations
- transport guidance
- daily schedule
- restaurants
- activities
- reservation checklist
- decision log

Every recommendation or major tradeoff must produce a `DecisionRecord` containing:
- `decision_id`
- `timestamp`
- `type`
- `summary`
- `alternatives`
- `confidence`
- `evidence`

## Support file requirements
### `references/voyage_schemas.md`
Define exact schemas for:
- `TravelPlan`
- `ScheduleBlock`
- `DecisionRecord`
- `ReservationChecklistItem`
- candidate item objects used for activities, restaurants, and lodging

### `references/itinerary_constraints.md`
Define:
- hard vs soft constraints
- conservative-mode behavior
- feasibility rules
- pacing and rest guidance
- handling of uncertain hours or reservation data

### `references/recommendation_style.md`
Define output style rules:
- concise, actionable travel planning language
- no generic tourism filler
- explain selections in practical terms
- distinguish must-book, good-to-book, and flexible items
- surface tradeoffs directly

## Storage layout
The package must use this local storage layout from the original spec:

```text
.voyage/
  state.json
  events.jsonl
  decisions.jsonl
  plans/
```

The `plans/` directory should hold saved plan artifacts keyed by trip or request ID.

### Config

File: `.voyage/config.json`

Required fields:
- `preferences.lodging_style`: preferred lodging type (hotel, boutique, ryokan, etc.)
- `preferences.dining_style`: dining preferences
- `preferences.pace`: trip pace (relaxed, moderate, packed)
- `constraints.budget_daily`: daily budget target
- `constraints.dietary`: dietary restrictions
- `reservation.auto_book`: whether to auto-book or draft-only (default false)
- `reservation.preferred_platforms`: preferred booking platforms
- `optimization.walking_limit_km`: maximum daily walking distance
- `optimization.transit_preference`: preferred transit modes

## Validation rules
The build is valid only if all of the following are true:
- `SKILL.md` starts on line 1 with valid YAML frontmatter
- the package contains `skill.json`, `SKILL.md`, and all required reference files
- all original capability areas remain present
- the skill supports both minimal-input planning and richer constraint-aware planning
- no itinerary schedules activities outside declared opening hours when such hours are known
- no itinerary contains impossible transit timing within the model’s own assumptions
- every recommendation path can emit decision explanations
- every full plan includes a reservation checklist
- the storage layout matches the specified `.voyage/` structure

Also include these acceptance tests in the package validation guidance:

### Test 1 — Minimal input
Input:
- destination: `Kyoto`
- trip_length: `5`

Expected:
- full itinerary
- daily schedule
- restaurant list
- lodging shortlist
- reservation checklist

### Test 2 — Constraint compliance
Expected:
- no activity scheduled outside known opening hours
- no impossible transit timing
- day structure includes meals, travel, rest, and buffers

### Test 3 — Decision logging
Expected:
- every recommendation path produces `DecisionRecord` entries for major choices

### Test 4 — Reservation planning
Expected:
- the final plan includes priority booking items, booking method guidance, deadlines when inferable, and backups

### Test 5 — Conservative mode
Expected:
- when source confidence is low, the plan becomes more conservative, flags uncertainty, and avoids overclaiming feasibility

---

## Responsibility Boundary

Voyage handles travel planning, itinerary construction, and reservation management.

Voyage does not perform general web research. Web search and fact verification belong to Sift.

Voyage does not send communications. Message delivery belongs to Dispatch.

---

## Optional Skill Cooperation

This skill may cooperate with other skills when present but must never depend on them.
If a cooperating skill is absent, this skill must still function normally.

- Sift — delegate web research for destination information, flight availability, and accommodation options.
- Taste — apply preference signals for restaurant, hotel, and experience recommendations.
- Weave — query social graph for travel companion context and local contacts.
- Look — receive image-based travel context such as boarding passes or itineraries.

---

## Journal Outputs

This skill emits the following journal types as defined in the OCAS Journal Specification (spec-ocas-Journals.md):

- Action Journal

Voyage emits Action Journal entries recording itinerary decisions, reservation plans, and booking executions.

---

## Visibility

visibility: public

---

## Universal OKRs

This skill must implement the universal OKRs defined in the OCAS Journal Specification (spec-ocas-Journals.md).

Required universal OKRs:

- Reliability: success_rate >= 0.95, retry_rate <= 0.10
- Validation Integrity: validation_failure_rate <= 0.05
- Efficiency: latency trending downward, repair_events <= 0.05
- Context Stability: context_utilization <= 0.70
- Observability: journal_completeness = 1.0

Skill-specific OKRs should be defined in the built SKILL.md to measure domain-relevant outcomes.

---

## Final Response Format for the Coder

Return:

1. package tree
2. full contents of every file
3. brief validation summary

Do not return planning commentary, process narration, or references to absent documents.
