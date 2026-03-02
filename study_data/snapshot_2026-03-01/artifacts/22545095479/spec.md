# Base PRD

Build a minimal web + api app for experiment runs.

## Web
- React + Vite app
- Shows run metadata and a simple status panel

## API
- FastAPI app
- Endpoints: /healthz, /info

## Determinism
- No external data sources
- Fixed outputs for a given run key
# Tier 2

- Add a simple table of metrics in the UI
- API includes a deterministic metrics payload
