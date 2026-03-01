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