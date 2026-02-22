export function HeaderBar({ route, onRouteChange, statusLine, role, onRoleChange, tabs }) {
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
        <label className="role-picker">
          <span>Role</span>
          <select value={role} onChange={(event) => onRoleChange(event.target.value)}>
            <option value="student">Student</option>
            <option value="operator">Operator</option>
            <option value="admin">Admin</option>
          </select>
        </label>
        <div className="status-chip" role="status">
          {statusLine}
        </div>
      </div>
    </header>
  );
}
