# Integration & End-to-End Validation


Goal:
Integrate frontend and backend, validate CORS, and run end-to-end tests for full-stack functionality.


Instructions:
Run both the FastAPI backend and React + Vite frontend together. Verify that the frontend can fetch data from the backend with CORS enabled. Execute end-to-end tests covering all acceptance criteria, including UI state transitions, live data rendering, and error handling when the backend is stopped.


Source Requirements (owned by this slice):
[
  "Frontend successfully communicates with the FastAPI backend using configured CORS settings.",
  "The project runs via npm run dev (Vite) and uvicorn (FastAPI).",
  "Resilience: Manually stopping the backend and clicking \"Retry\" triggers the \"Error\" state.",
  "The UI updates the \"System Version\" dynamically based on the /info response.",
  "Integration: UI state transitions and data rendering are correct with live backend."
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
  "End-to-end test: Frontend fetches /info, /healthz, /data from backend and displays correct UI states.",
  "Test: Stopping backend and clicking Retry shows Error state.",
  "Test: UI updates system version dynamically from backend.",
  "Test: CORS headers allow frontend requests."
]


Tests To Run Now:
[]


Tests Deferred Until Dependencies:
[
  "All end-to-end and integration tests (require both frontend and backend running)."
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
  "Frontend and backend can be developed and tested independently using the defined API contracts.",
  "Sample data and response shapes are fixed and known in advance.",
  "No external data sources are used; all data is static or mock."
]


Spec Reference:
work/spec.md


Slice JSON (authoritative):
{
  "id": "slice_3",
  "title": "Integration & End-to-End Validation",
  "goal": "Integrate frontend and backend, validate CORS, and run end-to-end tests for full-stack functionality.",
  "instructions": "Run both the FastAPI backend and React + Vite frontend together. Verify that the frontend can fetch data from the backend with CORS enabled. Execute end-to-end tests covering all acceptance criteria, including UI state transitions, live data rendering, and error handling when the backend is stopped.",
  "dependencies": [
    "slice_1",
    "slice_2"
  ],
  "implementation_dependencies": [
    "slice_1",
    "slice_2"
  ],
  "validation_dependencies": [],
  "source_requirements": [
    "Frontend successfully communicates with the FastAPI backend using configured CORS settings.",
    "The project runs via npm run dev (Vite) and uvicorn (FastAPI).",
    "Resilience: Manually stopping the backend and clicking \"Retry\" triggers the \"Error\" state.",
    "The UI updates the \"System Version\" dynamically based on the /info response.",
    "Integration: UI state transitions and data rendering are correct with live backend."
  ],
  "critical_contracts_needed": [
    "CORS must be configured to allow frontend-backend communication.",
    "Frontend and backend communicate via RESTful JSON over HTTP."
  ],
  "tests_to_author_now": [
    "End-to-end test: Frontend fetches /info, /healthz, /data from backend and displays correct UI states.",
    "Test: Stopping backend and clicking Retry shows Error state.",
    "Test: UI updates system version dynamically from backend.",
    "Test: CORS headers allow frontend requests."
  ],
  "tests_to_run_now": [],
  "tests_deferred_until_dependencies": [
    "All end-to-end and integration tests (require both frontend and backend running)."
  ],
  "effort_points": 3
}
