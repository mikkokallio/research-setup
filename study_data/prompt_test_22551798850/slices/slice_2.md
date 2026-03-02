# Frontend UI and State Management (React + Vite)


Goal:
Develop the React + Vite frontend dashboard with all required UI states and data contracts.


Instructions:
Build a single-page React app with a header (app name and system version), status bar (healthz), and main content (data grid/list). Implement explicit UI states: Loading, Empty, Error (with Retry), and Success. Use mock API responses matching the backend contract for initial development.


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
  "Fixed outputs for a given run key."
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
  "Test that Loading state is shown on initial mount.",
  "Test that Success state renders items from /data.",
  "Test that Empty state is shown when /data returns an empty list.",
  "Test that Error state is shown and Retry works when API is unreachable.",
  "Test that system version in header updates based on /info."
]


Tests To Run Now:
[
  "Test that Loading state is shown on initial mount.",
  "Test that Success state renders items from /data (using mock data).",
  "Test that Empty state is shown when /data returns an empty list (using mock data).",
  "Test that Error state is shown and Retry works when API is unreachable (using mock/fake error).",
  "Test that system version in header updates based on /info (using mock data)."
]


Tests Deferred Until Dependencies:
[
  "Test that frontend displays real backend data and handles real backend errors (after slice_1 is available)."
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
