# Frontend UI Implementation (React + Vite)


Goal:
Build a single-page React + Vite dashboard that fetches and displays backend data, with explicit UI states.


Instructions:
Create a React + Vite app with a Dashboard view. On mount, fetch /info, /healthz, and /data from the backend. Display the app name and system version in the header, a status bar reflecting /healthz, and a grid/list of items from /data. Implement UI states: Loading, Empty, Error (with Retry), and Success. Use TypeScript if possible.


Source Requirements (owned by this slice):
[
  "Frontend: React + Vite (TypeScript preferred).",
  "The UI consists of a single Dashboard view that aggregates data from the backend.",
  "Header: Displays the App Name and the current system version (from /info).",
  "Status Bar: A visual indicator of the /healthz status (Green for \"ok\", Red for errors).",
  "Main Content: A grid or list displaying the items from /data.",
  "The frontend must explicitly handle and visually distinguish between these four states: Loading, Empty, Error, Success.",
  "Initial Load: The app shows a \"Loading\" state immediately upon mount.",
  "Data Rendering: Items from the /data endpoint are visible in the UI.",
  "Resilience: Manually stopping the backend and clicking \"Retry\" triggers the \"Error\" state.",
  "The UI updates the \"System Version\" dynamically based on the /info response.",
  "No external data sources.",
  "Sample data and response shapes are fixed and known in advance."
]


Critical Contracts Needed:
[
  "Frontend and backend communicate via RESTful JSON over HTTP.",
  "The /data endpoint returns an array of items, each with id (integer), label (string), and status (string)."
]


Dependencies:
none


Implementation Dependencies (hard blockers):
none


Validation Dependencies (can author now, run later):
slice_1


Tests To Author Now:
[
  "Test that the Loading state is shown on initial mount.",
  "Test that the Error state appears if the backend is unreachable.",
  "Test that the Empty state appears if /data returns an empty list.",
  "Test that the Success state displays items from /data.",
  "Test that the header displays the app name and system version from /info.",
  "Test that the status bar is green for 'ok' and red for errors.",
  "Test that clicking Retry in Error state retries the fetch."
]


Tests To Run Now:
[
  "Test that the Loading state is shown on initial mount.",
  "Test that the Error state appears if the backend is unreachable (mocked).",
  "Test that the Empty state appears if /data returns an empty list (mocked).",
  "Test that the Success state displays items from /data (mocked).",
  "Test that the header displays the app name and system version from /info (mocked).",
  "Test that the status bar is green for 'ok' and red for errors (mocked).",
  "Test that clicking Retry in Error state retries the fetch (mocked)."
]


Tests Deferred Until Dependencies:
[
  "End-to-end test: UI fetches real backend and displays live data.",
  "Integration test: UI updates system version dynamically from backend."
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
  "id": "slice_2",
  "title": "Frontend UI Implementation (React + Vite)",
  "goal": "Build a single-page React + Vite dashboard that fetches and displays backend data, with explicit UI states.",
  "instructions": "Create a React + Vite app with a Dashboard view. On mount, fetch /info, /healthz, and /data from the backend. Display the app name and system version in the header, a status bar reflecting /healthz, and a grid/list of items from /data. Implement UI states: Loading, Empty, Error (with Retry), and Success. Use TypeScript if possible.",
  "dependencies": [],
  "implementation_dependencies": [],
  "validation_dependencies": [
    "slice_1"
  ],
  "source_requirements": [
    "Frontend: React + Vite (TypeScript preferred).",
    "The UI consists of a single Dashboard view that aggregates data from the backend.",
    "Header: Displays the App Name and the current system version (from /info).",
    "Status Bar: A visual indicator of the /healthz status (Green for \"ok\", Red for errors).",
    "Main Content: A grid or list displaying the items from /data.",
    "The frontend must explicitly handle and visually distinguish between these four states: Loading, Empty, Error, Success.",
    "Initial Load: The app shows a \"Loading\" state immediately upon mount.",
    "Data Rendering: Items from the /data endpoint are visible in the UI.",
    "Resilience: Manually stopping the backend and clicking \"Retry\" triggers the \"Error\" state.",
    "The UI updates the \"System Version\" dynamically based on the /info response.",
    "No external data sources.",
    "Sample data and response shapes are fixed and known in advance."
  ],
  "critical_contracts_needed": [
    "Frontend and backend communicate via RESTful JSON over HTTP.",
    "The /data endpoint returns an array of items, each with id (integer), label (string), and status (string)."
  ],
  "tests_to_author_now": [
    "Test that the Loading state is shown on initial mount.",
    "Test that the Error state appears if the backend is unreachable.",
    "Test that the Empty state appears if /data returns an empty list.",
    "Test that the Success state displays items from /data.",
    "Test that the header displays the app name and system version from /info.",
    "Test that the status bar is green for 'ok' and red for errors.",
    "Test that clicking Retry in Error state retries the fetch."
  ],
  "tests_to_run_now": [
    "Test that the Loading state is shown on initial mount.",
    "Test that the Error state appears if the backend is unreachable (mocked).",
    "Test that the Empty state appears if /data returns an empty list (mocked).",
    "Test that the Success state displays items from /data (mocked).",
    "Test that the header displays the app name and system version from /info (mocked).",
    "Test that the status bar is green for 'ok' and red for errors (mocked).",
    "Test that clicking Retry in Error state retries the fetch (mocked)."
  ],
  "tests_deferred_until_dependencies": [
    "End-to-end test: UI fetches real backend and displays live data.",
    "Integration test: UI updates system version dynamically from backend."
  ],
  "effort_points": 3
}
