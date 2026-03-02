# FastAPI Backend Endpoints


Goal:
Implement a deterministic FastAPI backend with /healthz, /info, /metrics, and /data endpoints.


Instructions:
Create a FastAPI app exposing the four required endpoints, each returning fixed, deterministic JSON responses as specified. Ensure CORS is enabled for local frontend development. Include OpenAPI docs at /docs reflecting all endpoints and their response schemas.


Dependencies:
none


Implementation Dependencies (hard blockers):
none


Validation Dependencies (can author now, run later):
none


Tests To Author Now:
[
  "GET /healthz returns 200 OK with {\"status\": \"ok\"}",
  "GET /metrics returns 200 OK with integer fields uptime and requests_total",
  "GET /info returns 200 OK with string fields version and environment",
  "GET /data returns 200 OK with items array, each item has id (int), label (str), status (str)",
  "GET /docs is accessible and documents all endpoints"
]


Tests To Run Now:
[
  "GET /healthz returns 200 OK with {\"status\": \"ok\"}",
  "GET /metrics returns 200 OK with integer fields uptime and requests_total",
  "GET /info returns 200 OK with string fields version and environment",
  "GET /data returns 200 OK with items array, each item has id (int), label (str), status (str)",
  "GET /docs is accessible and documents all endpoints"
]


Tests Deferred Until Dependencies:
[]


Effort Points:
3


Slice JSON (authoritative):
{
  "id": "slice_1",
  "title": "FastAPI Backend Endpoints",
  "goal": "Implement a deterministic FastAPI backend with /healthz, /info, /metrics, and /data endpoints.",
  "instructions": "Create a FastAPI app exposing the four required endpoints, each returning fixed, deterministic JSON responses as specified. Ensure CORS is enabled for local frontend development. Include OpenAPI docs at /docs reflecting all endpoints and their response schemas.",
  "dependencies": [],
  "implementation_dependencies": [],
  "validation_dependencies": [],
  "tests_to_author_now": [
    "GET /healthz returns 200 OK with {\"status\": \"ok\"}",
    "GET /metrics returns 200 OK with integer fields uptime and requests_total",
    "GET /info returns 200 OK with string fields version and environment",
    "GET /data returns 200 OK with items array, each item has id (int), label (str), status (str)",
    "GET /docs is accessible and documents all endpoints"
  ],
  "tests_to_run_now": [
    "GET /healthz returns 200 OK with {\"status\": \"ok\"}",
    "GET /metrics returns 200 OK with integer fields uptime and requests_total",
    "GET /info returns 200 OK with string fields version and environment",
    "GET /data returns 200 OK with items array, each item has id (int), label (str), status (str)",
    "GET /docs is accessible and documents all endpoints"
  ],
  "tests_deferred_until_dependencies": [],
  "effort_points": 3
}


Shared Context JSON:
{
  "full_spec": "# Base PRD\n\nBuild a minimal web + api app for experiment runs.\n\n## Web\n- React + Vite app\n- Shows run metadata and a simple status panel\n\n## API\n- FastAPI app\n- Endpoints: /healthz, /info\n\n## Determinism\n- No external data sources\n- Fixed outputs for a given run key\nThis specification defines Project Pulse, a lightweight health-monitoring dashboard. The goal is to provide a standardized blueprint that allows different development workflows (e.g., manual coding vs. AI-generated) to be evaluated against the same functional and aesthetic baseline.\n\n## 1. Product Overview\n\nProject Pulse is a single-page application (SPA) that monitors and displays the status of a backend service. It serves as a \"Hello World\" for full-stack integration, focusing on state management, API resilience, and observability.\n\n### Technical Constraints\n\n- Frontend: React + Vite (TypeScript preferred).\n- Backend: Python FastAPI.\n- Communication: RESTful JSON over HTTP.\n\n## 2. Functional Requirements\n\n### 2.1 Backend API (FastAPI)\n\nThe backend must implement four specific endpoints. All responses must be deterministic.\n\n| Endpoint | Method | Purpose | Sample Response |\n|---|---|---|---|\n| /healthz | GET | Liveness check | {\"status\": \"ok\"} |\n| /info | GET | System metadata | {\"version\": \"1.0.0\", \"environment\": \"dev\"} |\n| /metrics | GET | Mock telemetry | {\"uptime\": 3600, \"requests_total\": 42} |\n| /data | GET | Dashboard content | {\"items\": [{\"id\": 1, \"value\": \"Active\"}]} |\n\n### 2.2 Frontend UI (React + Vite)\n\nThe UI consists of a single Dashboard view that aggregates data from the backend.\n\n- Header: Displays the App Name and the current system version (from /info).\n- Status Bar: A visual indicator of the /healthz status (Green for \"ok\", Red for errors).\n- Main Content: A grid or list displaying the items from /data.\n\n## 3. UI State Specifications\n\nThe frontend must explicitly handle and visually distinguish between these four states:\n\n- Loading: A spinner or skeleton screen shown while the initial fetch is in progress.\n- Empty: A specific message (\"No data available\") if /data returns an empty list.\n- Error: A prominent alert if the API is unreachable or returns a 5xx code, including a \"Retry\" button.\n- Success: The populated dashboard once data is successfully retrieved.\n\n## 4. Acceptance Checklist (Strictly Testable)\n\n### Backend Validation\n\n- [ ] GET /healthz returns 200 OK with JSON {\"status\": \"ok\"}.\n- [ ] GET /metrics returns 200 OK with JSON containing integer fields `uptime` and `requests_total`.\n- [ ] GET /info returns 200 OK with JSON containing string fields `version` and `environment`.\n- [ ] GET /data returns 200 OK with JSON object key `items` as an array; each item includes `id` (integer), `label` (string), and `status` (string).\n- [ ] FastAPI docs (/docs) are accessible and reflect all four endpoints.\n\n### Frontend Validation\n\n- [ ] Initial Load: The app shows a \"Loading\" state immediately upon mount.\n- [ ] Data Rendering: Items from the /data endpoint are visible in the UI.\n- [ ] Resilience: Manually stopping the backend and clicking \"Retry\" triggers the \"Error\" state.\n- [ ] Environment: The project runs via npm run dev (Vite) and uvicorn (FastAPI).\n\n### Integration\n\n- [ ] Frontend successfully communicates with the FastAPI backend using configured CORS settings.\n- [ ] The UI updates the \"System Version\" dynamically based on the /info response.\n\n## 5. Sample Data Contract\n\nTo ensure deterministic testing, the /data endpoint should default to:\n\n```json\n{\n  \"items\": [\n    { \"id\": 1, \"label\": \"System Logic\", \"status\": \"Stable\" },\n    { \"id\": 2, \"label\": \"Network Latency\", \"status\": \"Optimal\" }\n  ]\n}\n```"
}


Authoritative Full Spec:
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
This specification defines Project Pulse, a lightweight health-monitoring dashboard. The goal is to provide a standardized blueprint that allows different development workflows (e.g., manual coding vs. AI-generated) to be evaluated against the same functional and aesthetic baseline.

## 1. Product Overview

Project Pulse is a single-page application (SPA) that monitors and displays the status of a backend service. It serves as a "Hello World" for full-stack integration, focusing on state management, API resilience, and observability.

### Technical Constraints

- Frontend: React + Vite (TypeScript preferred).
- Backend: Python FastAPI.
- Communication: RESTful JSON over HTTP.

## 2. Functional Requirements

### 2.1 Backend API (FastAPI)

The backend must implement four specific endpoints. All responses must be deterministic.

| Endpoint | Method | Purpose | Sample Response |
|---|---|---|---|
| /healthz | GET | Liveness check | {"status": "ok"} |
| /info | GET | System metadata | {"version": "1.0.0", "environment": "dev"} |
| /metrics | GET | Mock telemetry | {"uptime": 3600, "requests_total": 42} |
| /data | GET | Dashboard content | {"items": [{"id": 1, "value": "Active"}]} |

### 2.2 Frontend UI (React + Vite)

The UI consists of a single Dashboard view that aggregates data from the backend.

- Header: Displays the App Name and the current system version (from /info).
- Status Bar: A visual indicator of the /healthz status (Green for "ok", Red for errors).
- Main Content: A grid or list displaying the items from /data.

## 3. UI State Specifications

The frontend must explicitly handle and visually distinguish between these four states:

- Loading: A spinner or skeleton screen shown while the initial fetch is in progress.
- Empty: A specific message ("No data available") if /data returns an empty list.
- Error: A prominent alert if the API is unreachable or returns a 5xx code, including a "Retry" button.
- Success: The populated dashboard once data is successfully retrieved.

## 4. Acceptance Checklist (Strictly Testable)

### Backend Validation

- [ ] GET /healthz returns 200 OK with JSON {"status": "ok"}.
- [ ] GET /metrics returns 200 OK with JSON containing integer fields `uptime` and `requests_total`.
- [ ] GET /info returns 200 OK with JSON containing string fields `version` and `environment`.
- [ ] GET /data returns 200 OK with JSON object key `items` as an array; each item includes `id` (integer), `label` (string), and `status` (string).
- [ ] FastAPI docs (/docs) are accessible and reflect all four endpoints.

### Frontend Validation

- [ ] Initial Load: The app shows a "Loading" state immediately upon mount.
- [ ] Data Rendering: Items from the /data endpoint are visible in the UI.
- [ ] Resilience: Manually stopping the backend and clicking "Retry" triggers the "Error" state.
- [ ] Environment: The project runs via npm run dev (Vite) and uvicorn (FastAPI).

### Integration

- [ ] Frontend successfully communicates with the FastAPI backend using configured CORS settings.
- [ ] The UI updates the "System Version" dynamically based on the /info response.

## 5. Sample Data Contract

To ensure deterministic testing, the /data endpoint should default to:

```json
{
  "items": [
    { "id": 1, "label": "System Logic", "status": "Stable" },
    { "id": 2, "label": "Network Latency", "status": "Optimal" }
  ]
}
```
