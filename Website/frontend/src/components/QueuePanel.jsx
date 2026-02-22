export function QueuePanel({ jobResult, queueSnapshot, onRefresh }) {
  const job = jobResult && typeof jobResult === "object" ? jobResult.job : null;
  const snapshot = queueSnapshot && typeof queueSnapshot === "object" ? queueSnapshot.snapshot : null;
  const jobs = Array.isArray(snapshot?.jobs) ? snapshot.jobs : [];
  const rows = jobs.length > 0 ? jobs : job ? [job] : [];
  return (
    <section className="panel card queue-panel">
      <div className="queue-header-row">
        <div className="section-title">Job Queue</div>
        <button type="button" className="queue-refresh-btn" onClick={onRefresh}>
          Refresh
        </button>
      </div>
      {rows.length > 0 ? (
        <div className="queue-details">
          {rows.map((item) => (
            <div key={item.job_id} className="queue-row">
              <div>
                <strong>Job ID:</strong> {item.job_id}
              </div>
              <div>
                <strong>Status:</strong> {item.status}
              </div>
              <div>
                <strong>Model:</strong> {item.model_name}
              </div>
              <div>
                <strong>Profile:</strong> {item.profile_id}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="muted">No submitted job in this session.</div>
      )}
    </section>
  );
}
