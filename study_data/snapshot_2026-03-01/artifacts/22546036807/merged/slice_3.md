## Web
- React + Vite app
- Shows run metadata and a simple status panel

## 1. Product Overview

- Frontend: React + Vite (TypeScript preferred).
- Backend: Python FastAPI.
- Communication: RESTful JSON over HTTP.

The backend must implement four specific endpoints. All responses must be deterministic.

The UI consists of a single Dashboard view that aggregates data from the backend.

The frontend must explicitly handle and visually distinguish between these four states:

### Backend Validation

- [ ] Initial Load: The app shows a "Loading" state immediately upon mount.
- [ ] Data Rendering: Items from the /data endpoint are visible in the UI.
- [ ] Resilience: Manually stopping the backend and clicking "Retry" triggers the "Error" state.
- [ ] Environment: The project runs via npm run dev (Vite) and uvicorn (FastAPI).

## 5. Sample Data Contract