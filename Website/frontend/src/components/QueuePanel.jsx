export function QueuePanel({ jobResult, queueSnapshot, onRefresh }) {
  const maxVisibleRows = 120;
  const job = jobResult && typeof jobResult === "object" ? jobResult.job : null;
  const snapshot = queueSnapshot && typeof queueSnapshot === "object" ? queueSnapshot.snapshot : null;
  const jobs = Array.isArray(snapshot?.jobs) ? snapshot.jobs : [];
  const rows = jobs.length > 0 ? jobs : job ? [job] : [];
  const visibleRows = rows.slice(0, maxVisibleRows);
  const hiddenCount = Math.max(0, rows.length - visibleRows.length);
  return (
    <section className="panel card queue-panel">
      <div className="queue-header-row">
        <div className="section-title queue-title-compact">
          Job Queue
          <span className="queue-count-chip">{Number(snapshot?.job_count || rows.length)} jobs</span>
        </div>
        <button type="button" className="queue-refresh-btn" onClick={onRefresh}>
          Refresh
        </button>
      </div>
      {visibleRows.length > 0 ? (
        <div className="queue-details queue-details-compact">
          {visibleRows.map((item) => (
            <div key={item.job_id} className="queue-row">
              <div className="queue-row-main">
                <strong>{item.model_name || item.job_id}</strong>
                <span className="queue-pill">{item.status}</span>
              </div>
              <div className="queue-row-meta">
                <span>{item.job_id}</span>
                <span>{item.profile_id || "n/a"}</span>
                <span>{item.printer_id || "Unassigned"}</span>
              </div>
            </div>
          ))}
          {hiddenCount > 0 ? (
            <div className="queue-truncated-note muted">
              Showing {visibleRows.length} of {rows.length} jobs. Use Refresh to re-sync full queue state.
            </div>
          ) : null}
        </div>
      ) : (
        <div className="muted">No submitted job in this session.</div>
      )}
    </section>
  );
}
