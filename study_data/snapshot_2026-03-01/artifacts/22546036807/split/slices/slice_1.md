# Base PRD

## API
- FastAPI app
- Endpoints: /healthz, /info

Project Pulse is a single-page application (SPA) that monitors and displays the status of a backend service. It serves as a "Hello World" for full-stack integration, focusing on state management, API resilience, and observability.

## 2. Functional Requirements

| Endpoint | Method | Purpose | Sample Response |
|---|---|---|---|
| /healthz | GET | Liveness check | {"status": "ok"} |
| /info | GET | System metadata | {"version": "1.0.0", "environment": "dev"} |
| /metrics | GET | Mock telemetry | {"uptime": 3600, "requests_total": 42} |
| /data | GET | Dashboard content | {"items": [{"id": 1, "value": "Active"}]} |

- Header: Displays the App Name and the current system version (from /info).
- Status Bar: A visual indicator of the /healthz status (Green for "ok", Red for errors).
- Main Content: A grid or list displaying the items from /data.

- Loading: A spinner or skeleton screen shown while the initial fetch is in progress.
- Empty: A specific message ("No data available") if /data returns an empty list.
- Error: A prominent alert if the API is unreachable or returns a 5xx code, including a "Retry" button.
- Success: The populated dashboard once data is successfully retrieved.

- [ ] GET /healthz returns 200 OK with JSON {"status": "ok"}.
- [ ] GET /metrics returns 200 OK with JSON containing integer fields `uptime` and `requests_total`.
- [ ] GET /info returns 200 OK with JSON containing string fields `version` and `environment`.
- [ ] GET /data returns 200 OK with JSON object key `items` as an array; each item includes `id` (integer), `label` (string), and `status` (string).
- [ ] FastAPI docs (/docs) are accessible and reflect all four endpoints.

### Integration

To ensure deterministic testing, the /data endpoint should default to: