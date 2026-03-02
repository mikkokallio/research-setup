# FastAPI Backend Implementation


Goal:
Implement a deterministic FastAPI backend with four endpoints and OpenAPI docs.


Instructions:
Create a FastAPI app with endpoints: /healthz (GET, returns {"status": "ok"}), /info (GET, returns {"version": "1.0.0", "environment": "dev"}), /metrics (GET, returns {"uptime": 3600, "requests_total": 42}), and /data (GET, returns {"items": [{"id": 1, "label": "System Logic", "status": "Stable"}, {"id": 2, "label": "Network Latency", "status": "Optimal"}]}). Ensure all responses are deterministic and types match the spec. Enable CORS for local frontend development and verify /docs exposes all endpoints.


Dependencies:
none
