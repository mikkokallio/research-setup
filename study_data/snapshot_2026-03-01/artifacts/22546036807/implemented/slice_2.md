Build a minimal web + api app for experiment runs.

## Determinism
- No external data sources
- Fixed outputs for a given run key
This specification defines Project Pulse, a lightweight health-monitoring dashboard. The goal is to provide a standardized blueprint that allows different development workflows (e.g., manual coding vs. AI-generated) to be evaluated against the same functional and aesthetic baseline.

### Technical Constraints

### 2.1 Backend API (FastAPI)

### 2.2 Frontend UI (React + Vite)

## 3. UI State Specifications

## 4. Acceptance Checklist (Strictly Testable)

### Frontend Validation

- [ ] Frontend successfully communicates with the FastAPI backend using configured CORS settings.
- [ ] The UI updates the "System Version" dynamically based on the /info response.

```json
{
  "items": [
    { "id": 1, "label": "System Logic", "status": "Stable" },
    { "id": 2, "label": "Network Latency", "status": "Optimal" }
  ]
}
```