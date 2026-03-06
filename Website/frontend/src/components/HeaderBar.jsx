export function HeaderBar({ route, onRouteChange, statusLine, role, tabs, authSession, onSignOut }) {
  const availableTabs = Array.isArray(tabs) && tabs.length > 0
    ? tabs
    : [
        { key: "submit", label: "Submit Job" },
        { key: "queue", label: "Queue" }
      ];

  return (
    <header className="header-shell">
      <div className="brand-block">
        <div className="brand-title">EON-OpenSlicer</div>
        <div className="brand-subtitle">Web Print Portal</div>
      </div>
      <nav className="tab-strip" aria-label="Main navigation">
        {availableTabs.map((tab) => (
          <button
            key={tab.key}
            className={route === tab.key ? "tab-button is-active" : "tab-button"}
            onClick={() => onRouteChange(tab.key)}
            type="button"
          >
            {tab.label}
          </button>
        ))}
      </nav>
      <div className="header-meta">
        <div className="session-pill" title={String(authSession?.userId || "")}>
          {String(authSession?.userId || "signed-in user")}
        </div>
        <div className="session-pill">{String(role || "student")}</div>
        <button type="button" className="signout-btn" onClick={onSignOut}>
          Sign Out
        </button>
        <div className="status-chip" role="status">
          {statusLine}
        </div>
      </div>
    </header>
  );
}
