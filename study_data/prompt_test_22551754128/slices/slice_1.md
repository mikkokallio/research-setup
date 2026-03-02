# Backend API Implementation (FastAPI)


Goal:
Implement a deterministic FastAPI backend with four endpoints: /healthz, /info, /metrics, /data, and enable CORS.


Instructions:
Create a FastAPI app with the specified endpoints, each returning fixed, deterministic JSON responses as per the spec. Ensure all endpoints are documented in /docs. Configure CORS to allow requests from the frontend. No external data sources or dynamic state.


Source Requirements (owned by this slice):
[
  "The backend must implement four specific endpoints. All responses must be deterministic.",
  "GET /healthz returns 200 OK with JSON {\"status\": \"ok\"}.",
  "GET /info returns 200 OK with JSON containing string fields version and environment.",
  "GET /metrics returns 200 OK with JSON containing integer fields uptime and requests_total.",
  "GET /data returns 200 OK with JSON object key items as an array; each item includes id (integer), label (string), and status (string).",
  "FastAPI docs (/docs) are accessible and reflect all four endpoints.",
  "No external data sources.",
  "CORS must be configured to allow frontend-backend communication.",
  "Sample data and response shapes are fixed and known in advance."
]


Critical Contracts Needed:
[
  "All backend endpoints must return deterministic, fixed outputs for a given run key.",
  "The /data endpoint returns an array of items, each with id (integer), label (string), and status (string).",
  "CORS must be configured to allow frontend-backend communication."
]


Dependencies:
none


Implementation Dependencies (hard blockers):
none


Validation Dependencies (can author now, run later):
none


Tests To Author Now:
[
  "Test GET /healthz returns 200 and {\"status\": \"ok\"}.",
  "Test GET /info returns 200 and includes string fields version and environment.",
  "Test GET /metrics returns 200 and includes integer fields uptime and requests_total.",
  "Test GET /data returns 200 and items array with correct fields and types.",
  "Test /docs is accessible and documents all endpoints.",
  "Test CORS headers are present for frontend origin."
]


Tests To Run Now:
[
  "Test GET /healthz returns 200 and {\"status\": \"ok\"}.",
  "Test GET /info returns 200 and includes string fields version and environment.",
  "Test GET /metrics returns 200 and includes integer fields uptime and requests_total.",
  "Test GET /data returns 200 and items array with correct fields and types.",
  "Test /docs is accessible and documents all endpoints.",
  "Test CORS headers are present for frontend origin."
]


Tests Deferred Until Dependencies:
[]


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
  "id": "slice_1",
  "title": "Backend API Implementation (FastAPI)",
  "goal": "Implement a deterministic FastAPI backend with four endpoints: /healthz, /info, /metrics, /data, and enable CORS.",
  "instructions": "Create a FastAPI app with the specified endpoints, each returning fixed, deterministic JSON responses as per the spec. Ensure all endpoints are documented in /docs. Configure CORS to allow requests from the frontend. No external data sources or dynamic state.",
  "dependencies": [],
  "implementation_dependencies": [],
  "validation_dependencies": [],
  "source_requirements": [
    "The backend must implement four specific endpoints. All responses must be deterministic.",
    "GET /healthz returns 200 OK with JSON {\"status\": \"ok\"}.",
    "GET /info returns 200 OK with JSON containing string fields version and environment.",
    "GET /metrics returns 200 OK with JSON containing integer fields uptime and requests_total.",
    "GET /data returns 200 OK with JSON object key items as an array; each item includes id (integer), label (string), and status (string).",
    "FastAPI docs (/docs) are accessible and reflect all four endpoints.",
    "No external data sources.",
    "CORS must be configured to allow frontend-backend communication.",
    "Sample data and response shapes are fixed and known in advance."
  ],
  "critical_contracts_needed": [
    "All backend endpoints must return deterministic, fixed outputs for a given run key.",
    "The /data endpoint returns an array of items, each with id (integer), label (string), and status (string).",
    "CORS must be configured to allow frontend-backend communication."
  ],
  "tests_to_author_now": [
    "Test GET /healthz returns 200 and {\"status\": \"ok\"}.",
    "Test GET /info returns 200 and includes string fields version and environment.",
    "Test GET /metrics returns 200 and includes integer fields uptime and requests_total.",
    "Test GET /data returns 200 and items array with correct fields and types.",
    "Test /docs is accessible and documents all endpoints.",
    "Test CORS headers are present for frontend origin."
  ],
  "tests_to_run_now": [
    "Test GET /healthz returns 200 and {\"status\": \"ok\"}.",
    "Test GET /info returns 200 and includes string fields version and environment.",
    "Test GET /metrics returns 200 and includes integer fields uptime and requests_total.",
    "Test GET /data returns 200 and items array with correct fields and types.",
    "Test /docs is accessible and documents all endpoints.",
    "Test CORS headers are present for frontend origin."
  ],
  "tests_deferred_until_dependencies": [],
  "effort_points": 3
}
