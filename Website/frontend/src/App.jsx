import { useEffect, useMemo } from "react";
import { HeaderBar } from "./components/HeaderBar.jsx";
import { ContactFields } from "./components/ContactFields.jsx";
import { UploadPanel } from "./components/UploadPanel.jsx";
import { PrintOptionsPanel } from "./components/PrintOptionsPanel.jsx";
import { QueuePanel } from "./components/QueuePanel.jsx";
import { PrinterPanel } from "./components/PrinterPanel.jsx";
import { AuthGateway } from "./components/AuthGateway.jsx";
import { usePrintNetState } from "./state/usePrintNetState.js";
import { allowedRoutes } from "./auth/rolePolicy.js";

function SubmitPage({ state }) {
  return (
    <main className="layout-shell">
      <ContactFields contact={state.contactForm} onFieldChange={state.actions.setContactField} />
      <UploadPanel files={state.files} onFilesAdded={state.actions.addFiles} />
      <PrintOptionsPanel
        options={state.printOptions}
        onOptionChange={state.actions.setPrintOption}
        onSend={state.actions.sendJob}
      />
    </main>
  );
}

function QueuePage({ state }) {
  return (
    <main className="layout-shell">
      <QueuePanel
        jobResult={state.jobResult}
        queueSnapshot={state.queueSnapshot}
        onRefresh={state.actions.refreshQueue}
      />
    </main>
  );
}

function PrintersPage() {
  return (
    <main className="layout-shell">
      <PrinterPanel />
    </main>
  );
}

export default function App() {
  const state = usePrintNetState();
  const allTabs = useMemo(
    () => [
      { key: "submit", label: "Submit Job" },
      { key: "queue", label: "Queue" },
      { key: "printers", label: "Printers" }
    ],
    []
  );
  const role = state.authSession?.role || "student";
  const allowed = useMemo(() => allowedRoutes(role), [role]);
  const tabs = allTabs.filter((item) => allowed.includes(item.key));
  const isAuthenticated = Boolean(String(state.authSession?.token || "").trim());

  useEffect(() => {
    if (!allowed.includes(state.route)) {
      const fallback = allowed.length > 0 ? allowed[0] : "submit";
      state.actions.setRoute(fallback);
    }
  }, [allowed, state.route, state.actions]);

  if (!isAuthenticated) {
    return (
      <AuthGateway
        onAuthenticate={state.actions.signIn}
        statusLine={state.statusLine}
      />
    );
  }

  return (
    <div className="app-shell">
      <HeaderBar
        route={state.route}
        onRouteChange={state.actions.setRoute}
        statusLine={state.statusLine}
        role={role}
        tabs={tabs}
        authSession={state.authSession}
        onSignOut={state.actions.signOut}
      />
      {state.maintenance?.active ? (
        <div className="maintenance-banner" role="alert" aria-live="polite">
          <span className="maintenance-indicator" aria-hidden="true" />
          <span>Maintenance Mode: {state.maintenance.message || "Connection issue detected. Reconnecting..."}</span>
        </div>
      ) : null}
      {state.route === "submit" ? <SubmitPage state={state} /> : null}
      {state.route === "queue" ? <QueuePage state={state} /> : null}
      {state.route === "printers" ? <PrintersPage /> : null}
    </div>
  );
}
