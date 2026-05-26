# Flight Search Reference

## Execution

All flight searches run via `execute_code` or `terminal()` using the Hermes venv Python:
```bash
/usr/local/lib/hermes-agent/venv/bin/python3 -c "..."
```

## Capabilities

| Search Type | Description |
|---|---|
| **One-way** | Single origin → destination on a specific date |
| **Round-trip** | Outbound + return with separate date control |
| **Multi-city** | Multiple legs with distinct city pairs (may time out for very complex routes) |
| **Date search** | Find cheapest dates across a range (up to 61 days per chunk) |
| **Multi-airport** | Search across multiple origin/destination airports simultaneously |

## Filters Available

- Stops: any, non-stop, 1 stop or fewer, 2 stops or fewer
- Cabin: economy, premium economy, business, first
- Sort: best, cheapest, departure time, arrival time, duration, emissions
- Max duration (minutes)
- Airline filter
- Bags (checked + carry-on)
- Price limit
- Time restrictions (earliest/latest departure/arrival)
- Emissions filter (less CO2)

## Airport Resolution

Use `search_airports()` to resolve city names, IATA codes, or partial matches. Common cities map to multiple airports (e.g., "new york" → JFK, LGA, EWR). Always confirm ambiguous airports with the user before searching.

## Date Search for Trip Planning

When the user has flexible dates, use `SearchDates` to find the cheapest days to fly across a range. This is especially useful for:
- Suggesting date shifts that save money
- Comparing weekday vs weekend pricing
- Finding optimal departure/return combinations

## Presentation Rules

- Always show: price, currency, stops, total duration, airline, flight numbers, departure/arrival times (local)
- For round-trip: show outbound and return separately with combined price
- For date search: show top 5-10 cheapest dates with prices
- Sort by price (default) unless user specifies otherwise
- Include "as of" timestamp — flight prices change frequently
- Never present flight prices as guaranteed or fixed
- Flag when results are limited (e.g., "showing top 5 of 50+ results")

## Failure Modes

See `references/flights.md` for detailed failure modes and troubleshooting.

Common issues:
- **No results**: Try nearby airports, broaden date range, or relax filters
- **Timeout on multi-city**: Search legs individually and combine
- **Airport not found**: Ask user for IATA code or clarify city name
- **Library not installed**: `pip install flights` in the Hermes venv
