export function ComplianceBlockedView({ compliance, onRetry }) {
  const reasonCode = String(compliance?.reasonCode || "").trim() || "REGION_BLOCKED";
  const detail = String(compliance?.detail || "").trim() || "Cloud access is unavailable in your region.";
  const stateCode = String(compliance?.stateCode || "").trim();
  const unknownPolicy = String(compliance?.unknownPolicy || "").trim();
  const backendEnv = String(compliance?.backendEnv || "").trim();
  return (
    <main className="compliance-shell">
      <section className="compliance-card" role="alert" aria-live="assertive">
        <h1>Service Restricted</h1>
        <p className="compliance-detail">{detail}</p>
        <dl className="compliance-meta">
          <div>
            <dt>Reason</dt>
            <dd>{reasonCode}</dd>
          </div>
          <div>
            <dt>Detected State</dt>
            <dd>{stateCode || "Unknown"}</dd>
          </div>
          <div>
            <dt>Unknown Region Policy</dt>
            <dd>{unknownPolicy || "n/a"}</dd>
          </div>
          <div>
            <dt>Backend Environment</dt>
            <dd>{backendEnv || "n/a"}</dd>
          </div>
        </dl>
        <div className="compliance-actions">
          <button type="button" className="queue-refresh-btn" onClick={() => onRetry?.()}>
            Retry Check
          </button>
        </div>
      </section>
    </main>
  );
}
