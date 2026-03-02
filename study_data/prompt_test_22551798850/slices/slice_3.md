# Integration and End-to-End Validation


Goal:
Integrate frontend and backend, configure CORS, and validate full-stack operation.


Instructions:
Connect the frontend to the running FastAPI backend, ensure CORS is correctly configured, and verify all UI states and data flows work with real API responses. Run end-to-end tests covering the acceptance checklist.


Source Requirements (owned by this slice):
[
  "Frontend successfully communicates with the FastAPI backend using configured CORS settings.",
  "The project runs via npm run dev (Vite) and uvicorn (FastAPI).",
  "The UI updates the \"System Version\" dynamically based on the /info response.",
  "Resilience: Manually stopping the backend and clicking \"Retry\" triggers the \"Error\" state.",
  "Acceptance Checklist (Strictly Testable): Backend Validation, Frontend Validation, Integration."
]


Critical Contracts Needed:
[
  "CORS must be configured to allow frontend-backend communication.",
  "Frontend and backend communicate via RESTful JSON over HTTP."
]


Dependencies:
slice_1, slice_2


Implementation Dependencies (hard blockers):
slice_1, slice_2


Validation Dependencies (can author now, run later):
none


Tests To Author Now:
[
  "End-to-end test: Frontend loads and displays data from backend.",
  "End-to-end test: UI shows Error state and Retry works when backend is stopped.",
  "End-to-end test: System version updates dynamically from /info.",
  "End-to-end test: All UI states (Loading, Empty, Error, Success) are reachable with real backend."
]


Tests To Run Now:
[]


Tests Deferred Until Dependencies:
[
  "All end-to-end tests (after both slices are implemented and integrated)."
]


Effort Points:
3


Global Critical Contracts (shared):
[
  "All backend endpoints must return deterministic, fixed outputs for a given run key.",
  "Frontend and backend communicate via RESTful JSON over HTTP.",
  "The /data endpoint returns an array of items, each with id (integer), label (string), and status (string).",
  "CORS must be configured to allow frontend-backend communication."
]


Cross-Slice Assumptions (shared):
[
  "Frontend and backend are developed in separate directories/projects.",
  "API endpoint URLs and response shapes are agreed upon and stable.",
  "Frontend can be developed and tested using mock data before backend is available.",
  "Backend endpoints are accessible at a known base URL during integration."
]


Spec Reference:
work/spec.md
