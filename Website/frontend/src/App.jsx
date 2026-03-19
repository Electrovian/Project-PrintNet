import { useEffect, useMemo } from "react";
import { HeaderBar } from "./components/HeaderBar.jsx";
import { ContactFields } from "./components/ContactFields.jsx";
import { UploadPanel } from "./components/UploadPanel.jsx";
import { PrintOptionsPanel } from "./components/PrintOptionsPanel.jsx";
import { QueuePanel } from "./components/QueuePanel.jsx";
import { PrinterPanel } from "./components/PrinterPanel.jsx";
import { AuthGateway } from "./components/AuthGateway.jsx";
import { ComplianceBlockedView } from "./components/ComplianceBlockedView.jsx";
import { usePrintNetState } from "./state/usePrintNetState.js";
import { allowedRoutes } from "./auth/rolePolicy.js";

function normalizeUserKey(value) {
  const text = String(value || "").trim();
  if (!text) {
    return "";
  }
  try {
    return decodeURIComponent(text).toLowerCase();
  } catch (_err) {
    return text.toLowerCase();
  }
}

function routeFromPathname(pathname) {
  const path = String(pathname || "/").trim();
  const normalized = path.toLowerCase();
  if (normalized.startsWith("/home/")) {
    const segments = path.split("/").filter(Boolean);
    const pathUser = segments.length >= 2 ? String(segments[1] || "").trim() : "";
    const section = segments.length >= 3 ? String(segments[2] || "").trim().toLowerCase() : "";
    if (section === "queue") {
      return { route: "queue", pathUser };
    }
    if (section === "printers") {
      return { route: "printers", pathUser };
    }
    return { route: "submit", pathUser };
  }
  if (normalized.startsWith("/queue")) {
    return { route: "queue", pathUser: "" };
  }
  if (normalized.startsWith("/printers")) {
    return { route: "printers", pathUser: "" };
  }
  return { route: "submit", pathUser: "" };
}

function routeToPathname(route, userId) {
  const safeUser = encodeURIComponent(String(userId || "").trim() || "user");
  if (route === "queue") {
    return `/home/${safeUser}/queue`;
  }
  if (route === "printers") {
    return `/home/${safeUser}/printers`;
  }
  return `/home/${safeUser}`;
}

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

  useEffect(() => {
    if (!isAuthenticated || typeof window === "undefined") {
      return;
    }
    const syncRouteFromUrl = () => {
      const parsed = routeFromPathname(window.location?.pathname || "/");
      const sessionUser = normalizeUserKey(state.authSession?.userId || "");
      const pathUser = normalizeUserKey(parsed.pathUser || "");
      if (pathUser && sessionUser && pathUser !== sessionUser) {
        state.actions.signOut("Session invalid for requested account path. Please sign in again.");
        window.history.replaceState({}, "", "/signin");
        return;
      }
      const requested = parsed.route;
      if (!allowed.includes(requested)) {
        return;
      }
      if (requested !== state.route) {
        state.actions.setRoute(requested);
      }
    };
    syncRouteFromUrl();
    window.addEventListener("popstate", syncRouteFromUrl);
    return () => {
      window.removeEventListener("popstate", syncRouteFromUrl);
    };
  }, [isAuthenticated, allowed, state.route, state.actions, state.authSession?.userId]);

  useEffect(() => {
    if (isAuthenticated || typeof window === "undefined") {
      return;
    }
    const currentPath = String(window.location?.pathname || "/").toLowerCase();
    if (currentPath !== "/signin" && currentPath !== "/register" && currentPath !== "/sso" && currentPath !== "/verify") {
      window.history.replaceState({}, "", "/signin");
    }
  }, [isAuthenticated]);

  useEffect(() => {
    if (!isAuthenticated || typeof window === "undefined") {
      return;
    }
    const targetPath = routeToPathname(state.route, state.authSession?.userId || "");
    const currentPath = String(window.location?.pathname || "/");
    if (currentPath !== targetPath) {
      window.history.replaceState({}, "", targetPath);
    }
  }, [isAuthenticated, state.route, state.authSession?.userId]);

  if (state.compliance?.blocked) {
    return (
      <ComplianceBlockedView
        compliance={state.compliance}
        onRetry={state.actions.refreshCompliance}
      />
    );
  }

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
