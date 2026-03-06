import { useEffect, useMemo, useState } from "react";
import { buildBackendClient } from "../api/backendClient.js";
import { DEFAULT_CONTACT_FORM, DEFAULT_PRINT_OPTIONS } from "../config.js";

function defaultMaintenance() {
  return {
    active: false,
    message: ""
  };
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    if (!(file instanceof Blob)) {
      reject(new Error("Selected file is missing blob content."));
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      const result = String(reader.result || "");
      const commaIndex = result.indexOf(",");
      if (commaIndex < 0) {
        resolve("");
        return;
      }
      resolve(result.slice(commaIndex + 1));
    };
    reader.onerror = () => {
      reject(new Error("Unable to read selected file."));
    };
    reader.readAsDataURL(file);
  });
}

export function usePrintNetState() {
  const [route, setRoute] = useState("submit");
  const [contactForm, setContactForm] = useState(DEFAULT_CONTACT_FORM);
  const [printOptions, setPrintOptions] = useState(DEFAULT_PRINT_OPTIONS);
  const [files, setFiles] = useState([]);
  const [statusLine, setStatusLine] = useState("Idle");
  const [jobResult, setJobResult] = useState(null);
  const [queueSnapshot, setQueueSnapshot] = useState(null);
  const [maintenance, setMaintenance] = useState(defaultMaintenance);
  const [authSession, setAuthSession] = useState({
    token: "",
    userId: "",
    role: "student"
  });

  const apiClient = useMemo(() => buildBackendClient(), []);

  useEffect(() => {
    if (typeof window === "undefined" || typeof fetch !== "function") {
      return undefined;
    }

    let disposed = false;

    function activateMaintenance(message) {
      if (disposed) {
        return;
      }
      const text = String(message || "").trim() || "Connection unstable. Reconnecting...";
      setMaintenance({ active: true, message: text });
    }

    function clearMaintenance() {
      if (disposed) {
        return;
      }
      setMaintenance(defaultMaintenance());
    }

    async function probeConnection() {
      const controller = new AbortController();
      const timeoutId = window.setTimeout(() => controller.abort(), 6000);
      try {
        const probeUrl = `/?eon_probe=${Date.now()}`;
        const response = await fetch(probeUrl, {
          method: "GET",
          cache: "no-store",
          signal: controller.signal
        });
        window.clearTimeout(timeoutId);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        clearMaintenance();
      } catch (_err) {
        window.clearTimeout(timeoutId);
        activateMaintenance("Tunnel/network issue detected. Maintenance mode active while reconnecting.");
      }
    }

    function handleOffline() {
      activateMaintenance("You are offline. Maintenance mode active until connection returns.");
    }

    function handleOnline() {
      void probeConnection();
    }

    void probeConnection();
    const intervalId = window.setInterval(() => {
      void probeConnection();
    }, 15000);

    window.addEventListener("offline", handleOffline);
    window.addEventListener("online", handleOnline);

    return () => {
      disposed = true;
      window.clearInterval(intervalId);
      window.removeEventListener("offline", handleOffline);
      window.removeEventListener("online", handleOnline);
    };
  }, []);

  const actions = {
    setRoute,
    setMaintenance(active, message = "") {
      const enabled = Boolean(active);
      const text = String(message || "").trim();
      setMaintenance(enabled ? { active: true, message: text } : defaultMaintenance());
    },
    async signIn(payload = {}) {
      try {
        setStatusLine("Signing in...");
        const requestedUserId = String(payload?.userId || "").trim() || "web-user";
        const session = await apiClient.createSession({
          userId: requestedUserId
        });
        const token = String(session?.session?.token || "").trim();
        setAuthSession({
          token,
          userId: String(session?.session?.user_id || requestedUserId),
          role: String(session?.session?.role || authSession.role || "student")
        });
        setMaintenance(defaultMaintenance());
        setStatusLine("Signed in.");
      } catch (err) {
        setStatusLine(`Failed: ${String(err?.message || err)}`);
        throw err;
      }
    },
    signOut() {
      setAuthSession((prev) => ({
        token: "",
        userId: "",
        role: prev.role || "student"
      }));
      setStatusLine("Signed out.");
    },
    setContactField(key, value) {
      setContactForm((prev) => ({ ...prev, [key]: value }));
    },
    setPrintOption(key, value) {
      setPrintOptions((prev) => ({ ...prev, [key]: value }));
    },
    addFiles(fileList) {
      const rows = Array.from(fileList || []).map((file) => ({
        name: String(file?.name || "unnamed.stl"),
        size: Number(file?.size || 0),
        blob: file instanceof Blob ? file : null
      }));
      setFiles(rows);
    },
    async refreshQueue() {
      const token = String(authSession.token || "").trim();
      if (!token) {
        setQueueSnapshot(null);
        setStatusLine("Queue unavailable: sign in session required.");
        return;
      }
      try {
        const snapshot = await apiClient.getQueueSnapshot(token);
        setQueueSnapshot(snapshot);
        setMaintenance(defaultMaintenance());
        setStatusLine("Queue refreshed.");
      } catch (err) {
        setMaintenance({
          active: true,
          message: "Queue service unavailable. Retrying connection..."
        });
        setStatusLine(`Failed: ${String(err?.message || err)}`);
      }
    },
    async sendJob() {
      try {
        setStatusLine("Submitting job...");
        const session = await apiClient.createSession({
          userId: contactForm.email || contactForm.name || "web-user"
        });
        const token = String(session?.session?.token || "").trim();
        setAuthSession({
          token,
          userId: String(session?.session?.user_id || contactForm.email || "web-user"),
          role: String(session?.session?.role || authSession.role || "student")
        });
        const profiles = await apiClient.listProfiles({ filament: printOptions.material, nozzle: "0.4" }, token);
        const profile = Array.isArray(profiles?.profiles) && profiles.profiles.length > 0 ? profiles.profiles[0] : null;
        if (!profile) {
          throw new Error("No matching profile available.");
        }
        if (files.length <= 0 || !(files[0]?.blob instanceof Blob)) {
          throw new Error("Select at least one STL or STEP file before submitting.");
        }
        const firstFile = files[0];
        const encoded = await fileToBase64(firstFile.blob);
        if (!String(encoded || "").trim()) {
          throw new Error("Selected file is empty or unreadable.");
        }
        const uploaded = await apiClient.uploadModel({
          authToken: token,
          fileName: firstFile.name,
          dataBase64: encoded
        });
        const uploadedModelName = String(uploaded?.model?.model_name || firstFile.name).trim() || firstFile.name;
        const submitted = await apiClient.submitJob({
          authToken: token,
          modelName: uploadedModelName,
          profileId: profile.profile_id || profile.profileId || "p-default-pla",
          requestedBy: session?.session?.user_id || contactForm.email || "web-user",
          printerId: printOptions.printerId
        });
        setJobResult(submitted);
        const snapshot = await apiClient.getQueueSnapshot(token);
        setQueueSnapshot(snapshot);
        setMaintenance(defaultMaintenance());
        setStatusLine("Job submitted.");
      } catch (err) {
        setMaintenance({
          active: true,
          message: "Print services temporarily unavailable. Retrying connection..."
        });
        setStatusLine(`Failed: ${String(err?.message || err)}`);
      }
    }
  };

  return {
    route,
    contactForm,
    printOptions,
    files,
    statusLine,
    jobResult,
    queueSnapshot,
    maintenance,
    authSession,
    actions
  };
}
