---
plan_id: trip-planning
name: Trip Planning
version: 1.0.0
description: Destination research → itinerary construction → accommodation options. Produces a draft itinerary for review.
parameters:
  destination:
    type: string
    required: true
    description: Primary destination city or region.
  travel_dates:
    type: string
    required: true
    description: "Travel window in ISO 8601 range format: YYYY-MM-DD/YYYY-MM-DD."
  party_size:
    type: number
    required: false
    default: 1
    description: Number of travelers.
steps:
  - id: destination-research
    name: Destination Research
    skill: ocas-voyage
    command: voyage.plan.trip
    on_failure: abort
  - id: lodging-options
    name: Lodging Options
    skill: ocas-voyage
    command: voyage.recommend.lodging
    on_failure: skip
  - id: itinerary-optimize
    name: Itinerary Optimization
    skill: ocas-voyage
    command: voyage.optimize.itinerary
    on_failure: skip
---

## Step 1: destination-research

**Skill:** ocas-voyage
**Command:** voyage.plan.trip

**Inputs:**
- `destination`: `{{params.destination}}`
- `travel_dates`: `{{params.travel_dates}}`
- `party_size`: `{{params.party_size}}`

**Outputs:**
- `trip_plan`: structured trip plan with destination brief and activity suggestions
- `itinerary_id`: ID of the created itinerary

**On failure:** abort

---

## Step 2: lodging-options

**Skill:** ocas-voyage
**Command:** voyage.recommend.lodging

**Inputs:**
- `itinerary_id`: `{{steps.destination-research.itinerary_id}}`
- `party_size`: `{{params.party_size}}`

**Outputs:**
- `lodging_list`: list of accommodation options

**On failure:** skip

---

## Step 3: itinerary-optimize

**Skill:** ocas-voyage
**Command:** voyage.optimize.itinerary

**Inputs:**
- `itinerary_id`: `{{steps.destination-research.itinerary_id}}`

**Outputs:**
- `optimized_itinerary`: itinerary optimized for feasibility and logistics

**On failure:** skip
