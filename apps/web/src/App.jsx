const env = {
  runKey: import.meta.env.VITE_RUN_KEY || "local",
  model: import.meta.env.VITE_MODEL || "unknown",
  condition: import.meta.env.VITE_CONDITION || "unknown",
  tier: import.meta.env.VITE_TIER || "unknown",
  apiUrl: import.meta.env.VITE_API_URL || "http://localhost:8000",
};

export default function App() {
  return (
    <div className="page">
      <header>
        <h1>Experiment Run</h1>
        <p className="subtitle">Deterministic web + api scaffold</p>
      </header>

      <section className="card">
        <h2>Run Metadata</h2>
        <ul>
          <li>
            <strong>Run Key:</strong> {env.runKey}
          </li>
          <li>
            <strong>Model:</strong> {env.model}
          </li>
          <li>
            <strong>Condition:</strong> {env.condition}
          </li>
          <li>
            <strong>Tier:</strong> {env.tier}
          </li>
          <li>
            <strong>API:</strong> {env.apiUrl}
          </li>
        </ul>
      </section>

      <section className="card">
        <h2>Status</h2>
        <p>Waiting for run artifacts and metrics.</p>
      </section>
    </div>
  );
}
