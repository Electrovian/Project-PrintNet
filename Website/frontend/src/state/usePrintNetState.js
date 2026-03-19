import { useEffect, useMemo, useState } from "react";
import { buildBackendClient, isRegionComplianceError } from "../api/backendClient.js";
import { DEFAULT_CONTACT_FORM, DEFAULT_PRINT_OPTIONS } from "../config.js";

const ACTIVITY_FEED_LIMIT = 200;
const ACTIVITY_POLL_MS = 5000;

function defaultMaintenance() {
  return {
    active: false,
    message: ""
  };
}

function emptyActivityState() {
  return {
    cursor: 0,
    jobsById: {},
    order: []
  };
}

function defaultComplianceState() {
  return {
    checked: false,
    blocked: false,
    reasonCode: "",
    detail: "",
    stateCode: "",
    decision: "allow",
    backendEnv: "",
    unknownPolicy: ""
  };
}

function normalizeCompliancePayload(payload) {
  const compliance = payload && typeof payload === "object" ? payload.compliance : null;
  if (!compliance || typeof compliance !== "object") {
    return defaultComplianceState();
  }
  const decision = String(compliance.decision || "allow").trim().toLowerCase() === "deny" ? "deny" : "allow";
  return {
    checked: true,
    blocked: decision === "deny",
    reasonCode: String(compliance.reason_code || "").trim(),
    detail: String(compliance.detail || "").trim(),
    stateCode: String(compliance.state_code || "").trim(),
    decision,
    backendEnv: String(compliance.backend_env || "").trim(),
    unknownPolicy: String(compliance.unknown_policy || "").trim()
  };
}

function normalizeTimestamp(value) {
  const text = String(value || "").trim();
  if (!text) {
    return "";
  }
  return text;
}

function toSortableTime(value) {
  const text = normalizeTimestamp(value);
  if (!text) {
    return 0;
  }
  const parsed = Date.parse(text);
  if (!Number.isFinite(parsed)) {
    return 0;
  }
  return Number(parsed);
}

function sortJobIds(jobsById) {
  return Object.values(jobsById)
    .sort((a, b) => {
      const seqA = Number(a?._seq || 0);
      const seqB = Number(b?._seq || 0);
      if (seqA !== seqB) {
        return seqB - seqA;
      }
      const timeA = toSortableTime(a?.updated_at_utc || a?.created_at_utc || "");
      const timeB = toSortableTime(b?.updated_at_utc || b?.created_at_utc || "");
      if (timeA !== timeB) {
        return timeB - timeA;
      }
      return String(b?.job_id || "").localeCompare(String(a?.job_id || ""));
    })
    .map((item) => String(item?.job_id || "").trim())
    .filter(Boolean);
}

function normalizeJobRow(raw, seqFallback = 0) {
  const seqValue = Number.parseInt(String(raw?._seq ?? raw?.latest_seq ?? seqFallback), 10);
  const seq = Number.isFinite(seqValue) ? Math.max(0, seqValue) : Math.max(0, Number(seqFallback || 0));
  const created = normalizeTimestamp(raw?.created_at_utc);
  const updated = normalizeTimestamp(raw?.updated_at_utc) || created;
  return {
    job_id: String(raw?.job_id || "").trim(),
    model_name: String(raw?.model_name || "").trim(),
    profile_id: String(raw?.profile_id || "").trim(),
    printer_id: String(raw?.printer_id || "").trim(),
    requested_by: String(raw?.requested_by || "").trim(),
    queue: String(raw?.queue || "").trim(),
    status: String(raw?.status || "").trim() || "unknown",
    created_at_utc: created,
    updated_at_utc: updated,
    _seq: seq
  };
}

function hydrateActivityStateFromSnapshot(snapshotPayload) {
  const snapshot = snapshotPayload && typeof snapshotPayload === "object" ? snapshotPayload.snapshot : null;
  const jobs = Array.isArray(snapshot?.jobs) ? snapshot.jobs : [];
  const jobsById = {};
  for (const item of jobs) {
    const row = normalizeJobRow(item, 0);
    if (!row.job_id) {
      continue;
    }
    jobsById[row.job_id] = row;
  }
  return {
    cursor: 0,
    jobsById,
    order: sortJobIds(jobsById)
  };
}

function mergeFeedIntoActivityState(prevState, feedPayload) {
  const prev = prevState && typeof prevState === "object" ? prevState : emptyActivityState();
  const jobsById = { ...(prev.jobsById || {}) };
  const items = Array.isArray(feedPayload?.items) ? feedPayload.items : [];
  for (const item of items) {
    const jobId = String(item?.job_id || "").trim();
    if (!jobId) {
      continue;
    }
    const incomingSeqRaw = Number.parseInt(String(item?.seq ?? "0"), 10);
    const incomingSeq = Number.isFinite(incomingSeqRaw) ? Math.max(0, incomingSeqRaw) : 0;
    const existing = jobsById[jobId];
    const existingSeq = Number.parseInt(String(existing?._seq ?? "0"), 10);
    if (Number.isFinite(existingSeq) && incomingSeq < existingSeq) {
      continue;
    }
    const updated = normalizeTimestamp(item?.ts_utc);
    const created = normalizeTimestamp(item?.created_at_utc) || normalizeTimestamp(existing?.created_at_utc) || updated;
    jobsById[jobId] = normalizeJobRow(
      {
        job_id: jobId,
        model_name: item?.model_name,
        profile_id: item?.profile_id,
        printer_id: item?.printer_id,
        requested_by: item?.requested_by,
        queue: item?.queue,
        status: item?.status,
        created_at_utc: created,
        updated_at_utc: updated || created
      },
      incomingSeq
    );
  }
  const cursorOutRaw = Number.parseInt(String(feedPayload?.cursor_out ?? prev.cursor ?? 0), 10);
  const cursorOut = Number.isFinite(cursorOutRaw) ? Math.max(0, cursorOutRaw) : Math.max(0, Number(prev.cursor || 0));
  return {
    cursor: cursorOut,
    jobsById,
    order: sortJobIds(jobsById)
  };
}

function buildDerivedQueueSnapshot(basePayload, activityState) {
  const base = basePayload && typeof basePayload === "object" ? basePayload : { ok: true };
  const baseSnapshot = base?.snapshot && typeof base.snapshot === "object" ? base.snapshot : {};
  const jobsById = activityState?.jobsById && typeof activityState.jobsById === "object" ? activityState.jobsById : {};
  const order = Array.isArray(activityState?.order) ? activityState.order : [];
  const jobs = order.map((jobId) => jobsById[jobId]).filter((item) => item && typeof item === "object");
  const statusCounts = {};
  let queueDepth = 0;
  for (const job of jobs) {
    const status = String(job.status || "").trim() || "unknown";
    statusCounts[status] = Number(statusCounts[status] || 0) + 1;
    if (status === "queued") {
      queueDepth += 1;
    }
  }
  return {
    ...base,
    snapshot: {
      ...baseSnapshot,
      job_count: jobs.length,
      status_counts: statusCounts,
      queue_depth: queueDepth,
      jobs
    }
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
  const [queueSnapshotBase, setQueueSnapshotBase] = useState(null);
  const [activityState, setActivityState] = useState(emptyActivityState);
  const [maintenance, setMaintenance] = useState(defaultMaintenance);
  const [compliance, setCompliance] = useState(defaultComplianceState);
  const [authSession, setAuthSession] = useState({
    token: "",
    userId: "",
    role: "student"
  });

  const apiClient = useMemo(() => buildBackendClient(), []);
  const queueSnapshot = useMemo(
    () => buildDerivedQueueSnapshot(queueSnapshotBase, activityState),
    [queueSnapshotBase, activityState]
  );

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

  function _setComplianceBlockedFromError(err) {
    if (!isRegionComplianceError(err)) {
      return false;
    }
    const code = String(err?.code || "").trim() || "REGION_BLOCKED";
    const detail = String(err?.message || err?.detail || "").trim() || "Region compliance policy blocked this request.";
    setCompliance((prev) => ({
      ...prev,
      checked: true,
      blocked: true,
      decision: "deny",
      reasonCode: code,
      detail
    }));
    return true;
  }

  async function refreshCompliance() {
    try {
      const payload = await apiClient.getComplianceRegion();
      const normalized = normalizeCompliancePayload(payload);
      setCompliance(normalized);
      return normalized;
    } catch (err) {
      _setComplianceBlockedFromError(err);
      return defaultComplianceState();
    }
  }

  async function resolveIdentityFromToken(authToken, fallback = {}) {
    const token = String(authToken || "").trim();
    if (!token) {
      throw new Error("Sign-in session required.");
    }
    const response = await apiClient.whoAmI(token);
    const identity = response?.identity || {};
    return {
      token,
      userId: String(identity.user_id || fallback.userId || "").trim(),
      role: String(identity.role || fallback.role || "student")
    };
  }

  async function hardRefreshQueue(authToken, fallbackIdentity = {}) {
    if (compliance?.blocked) {
      throw new Error("Cloud actions are disabled by region compliance policy.");
    }
    const identity = await resolveIdentityFromToken(authToken, fallbackIdentity);
    setAuthSession(identity);
    const snapshot = await apiClient.getQueueSnapshot(identity.token);
    setQueueSnapshotBase(snapshot);
    setActivityState(hydrateActivityStateFromSnapshot(snapshot));
    return identity;
  }

  useEffect(() => {
    let disposed = false;
    async function runPrecheck() {
      const result = await refreshCompliance();
      if (disposed) {
        return;
      }
      if (result?.blocked) {
        setStatusLine("Cloud actions are unavailable in your region.");
      }
    }
    void runPrecheck();
    return () => {
      disposed = true;
    };
  }, [apiClient]);

  useEffect(() => {
    const token = String(authSession.token || "").trim();
    if (!token) {
      return undefined;
    }
    let disposed = false;
    async function runSignedInPrecheck() {
      const result = await refreshCompliance();
      if (disposed) {
        return;
      }
      if (result?.blocked) {
        setStatusLine("Cloud actions are unavailable in your region.");
      }
    }
    void runSignedInPrecheck();
    return () => {
      disposed = true;
    };
  }, [authSession.token]);

  useEffect(() => {
    if (route !== "queue") {
      return undefined;
    }
    if (compliance?.blocked) {
      return undefined;
    }
    const token = String(authSession.token || "").trim();
    if (!token) {
      return undefined;
    }

    let disposed = false;
    let inFlight = false;

    async function pollActivityFeed() {
      if (disposed || inFlight) {
        return;
      }
      inFlight = true;
      try {
        const response = await apiClient.getActivityFeed({
          authToken: token,
          cursor: activityState.cursor,
          limit: ACTIVITY_FEED_LIMIT
        });
        const feed = response?.feed || {};
        if (Boolean(feed?.reset_required)) {
          await hardRefreshQueue(token, authSession);
          inFlight = false;
          return;
        }
        setActivityState((prev) => mergeFeedIntoActivityState(prev, feed));
        setMaintenance(defaultMaintenance());
      } catch (_err) {
        _setComplianceBlockedFromError(_err);
        setMaintenance({
          active: true,
          message: "Queue service unavailable. Retrying connection..."
        });
      } finally {
        inFlight = false;
      }
    }

    void pollActivityFeed();
    const intervalId = window.setInterval(() => {
      void pollActivityFeed();
    }, ACTIVITY_POLL_MS);

    return () => {
      disposed = true;
      window.clearInterval(intervalId);
    };
  }, [apiClient, authSession, activityState.cursor, compliance?.blocked, route]);

  const actions = {
    setRoute,
    refreshCompliance,
    setMaintenance(active, message = "") {
      const enabled = Boolean(active);
      const text = String(message || "").trim();
      setMaintenance(enabled ? { active: true, message: text } : defaultMaintenance());
    },
    async signIn(payload = {}) {
      try {
        if (compliance?.blocked) {
          throw new Error("Cloud sign-in is blocked in this region.");
        }
        const mode = String(payload?.mode || "signin").trim().toLowerCase();
        const step = String(payload?.step || (mode === "signup" ? "signup" : "password")).trim().toLowerCase();
        const requestedUserId = String(payload?.userId || "").trim();
        const password = String(payload?.password || "");
        if (mode === "signin" && step === "verify") {
          const challengeId = String(payload?.challengeId || "").trim();
          const verificationCode = String(payload?.verificationCode || "").trim();
          if (!challengeId) {
            throw new Error("Verification challenge is missing.");
          }
          if (!verificationCode) {
            throw new Error("Verification code is required.");
          }
          setStatusLine("Verifying sign-in code...");
          const authResponse = await apiClient.verifyLoginCode({ challengeId, verificationCode });
          const token = String(authResponse?.session?.token || "").trim();
          const identity = await resolveIdentityFromToken(token, {
            userId: String(authResponse?.session?.user_id || payload?.userId || ""),
            role: String(authResponse?.session?.role || "student")
          });
          setAuthSession(identity);
          setQueueSnapshotBase(null);
          setActivityState(emptyActivityState());
          setJobResult(null);
          setMaintenance(defaultMaintenance());
          setStatusLine("Signed in.");
          return { ok: true, requiresVerification: false };
        }

        if (!requestedUserId) {
          throw new Error("Username or email is required.");
        }
        if (!password) {
          throw new Error("Password is required.");
        }

        if (mode === "signup") {
          setStatusLine("Creating account...");
          const authResponse = await apiClient.registerAccount({ userId: requestedUserId, password });
          const token = String(authResponse?.session?.token || "").trim();
          const identity = await resolveIdentityFromToken(token, {
            userId: String(authResponse?.session?.user_id || requestedUserId),
            role: String(authResponse?.session?.role || "student")
          });
          setAuthSession(identity);
          setQueueSnapshotBase(null);
          setActivityState(emptyActivityState());
          setJobResult(null);
          setMaintenance(defaultMaintenance());
          setStatusLine("Account created and signed in.");
          return { ok: true, requiresVerification: false };
        }

        setStatusLine("Checking credentials...");
        try {
          const authResponse = await apiClient.loginWithPassword({ userId: requestedUserId, password });
          const token = String(authResponse?.session?.token || "").trim();
          const identity = await resolveIdentityFromToken(token, {
            userId: String(authResponse?.session?.user_id || requestedUserId),
            role: String(authResponse?.session?.role || "student")
          });
          setAuthSession(identity);
          setQueueSnapshotBase(null);
          setActivityState(emptyActivityState());
          setJobResult(null);
          setMaintenance(defaultMaintenance());
          setStatusLine("Signed in.");
          return { ok: true, requiresVerification: false };
        } catch (authError) {
          const authCode = String(authError?.code || "").trim().toUpperCase();
          const authDetail = String(authError?.message || "").trim().toUpperCase();
          const verificationRequired =
            authCode === "AUTH_VERIFICATION_REQUIRED" ||
            authDetail.includes("AUTH_VERIFICATION_REQUIRED");
          if (!verificationRequired) {
            throw authError;
          }
        }

        const challengeResponse = await apiClient.requestLoginCode({ userId: requestedUserId, password });
        const challenge = challengeResponse?.challenge || {};
        const challengeId = String(challenge.challenge_id || "").trim();
        if (!challengeId) {
          throw new Error("Unable to start login verification.");
        }
        const deliveryDestination = String(challenge?.delivery?.destination || "").trim();
        setStatusLine(
          deliveryDestination
            ? `Verification code sent to ${deliveryDestination}.`
            : "Verification code sent."
        );
        return {
          ok: true,
          requiresVerification: true,
          challengeId,
          delivery: challenge?.delivery || null,
          debugCode: String(challenge.debug_code || "")
        };
      } catch (err) {
        _setComplianceBlockedFromError(err);
        setStatusLine(`Failed: ${String(err?.message || err)}`);
        throw err;
      }
    },
    signOut(message = "Signed out.") {
      setAuthSession((prev) => ({
        token: "",
        userId: "",
        role: prev.role || "student"
      }));
      setQueueSnapshotBase(null);
      setActivityState(emptyActivityState());
      setStatusLine(String(message || "Signed out."));
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
      if (compliance?.blocked) {
        setStatusLine("Queue disabled by region compliance policy.");
        return;
      }
      const token = String(authSession.token || "").trim();
      if (!token) {
        setQueueSnapshotBase(null);
        setActivityState(emptyActivityState());
        setStatusLine("Queue unavailable: sign in session required.");
        return;
      }
      try {
        await hardRefreshQueue(token, authSession);
        setMaintenance(defaultMaintenance());
        setStatusLine("Queue refreshed.");
      } catch (err) {
        _setComplianceBlockedFromError(err);
        setMaintenance({
          active: true,
          message: "Queue service unavailable. Retrying connection..."
        });
        setStatusLine(`Failed: ${String(err?.message || err)}`);
      }
    },
    async sendJob() {
      try {
        if (compliance?.blocked) {
          throw new Error("Job submission disabled by region compliance policy.");
        }
        setStatusLine("Submitting job...");
        const token = String(authSession.token || "").trim();
        if (!token) {
          throw new Error("Sign in before submitting a job.");
        }
        const identity = await resolveIdentityFromToken(token, authSession);
        setAuthSession(identity);
        const profiles = await apiClient.listProfiles(
          { filament: printOptions.material, nozzle: "0.4" },
          identity.token
        );
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
          authToken: identity.token,
          fileName: firstFile.name,
          dataBase64: encoded
        });
        const uploadedModelName = String(uploaded?.model?.model_name || firstFile.name).trim() || firstFile.name;
        const submitted = await apiClient.submitJob({
          authToken: identity.token,
          modelName: uploadedModelName,
          profileId: profile.profile_id || profile.profileId || "p-default-pla",
          requestedBy: identity.userId,
          printerId: printOptions.printerId
        });
        setJobResult(submitted);
        await hardRefreshQueue(identity.token, identity);
        setMaintenance(defaultMaintenance());
        setStatusLine("Job submitted.");
      } catch (err) {
        _setComplianceBlockedFromError(err);
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
    compliance,
    authSession,
    actions
  };
}
