# Initialization Procedure

On first invocation of any Voyage command, run `voyage.init`:

1. Create `{agent_root}/commons/data/ocas-voyage/` and subdirectories (`plans/`, `itineraries/`)
2. Write default `config.json` and `state.json` if absent
3. Create empty JSONL files: `events.jsonl`, `decisions.jsonl`
4. Create `{agent_root}/commons/journals/ocas-voyage/`
5. Register cron job `voyage:update` if not already present (check the platform scheduling registry first)
6. Log initialization as a DecisionRecord in `decisions.jsonl`

## Marriott Strider MCP Setup (run once)

Skip if `mcp-marriott` already in MCP config:
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

## Google Hotels Setup

Google Hotels search requires web browsing access. If the system provides web browsing capability, this is available automatically. If unavailable, Expedia and Marriott cover this path.

## Flights Library Setup

The `flights` Python package must be installed in the Hermes venv:
```bash
/usr/local/lib/hermes-agent/venv/bin/python3 -m pip install flights
```

Verify with: `/usr/local/lib/hermes-agent/venv/bin/python3 -c "from fli.search.flights import SearchFlights; print('OK')"`

Record result in config: `"flights_available": true/false`

## Optional Credentials

- `FLYAI_API_KEY` — set for enhanced Marriott AI results; skill works without it

## GoPlaces Check

- Run: `platform skill registry query | grep goplaces`
- Record result in `{agent_root}/commons/data/ocas-voyage/config.json` under `"goplaces_available": true/false`
