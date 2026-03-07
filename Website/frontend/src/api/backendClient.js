import { resolveApiBaseUrl } from "../config.js";
import {
  normalizeAuthCredentials,
  normalizeLoginCodeRequestPayload,
  normalizeLoginCodeVerifyPayload,
  normalizeModelUploadPayload,
  normalizePrintRequestPayload,
  normalizePrinterRegistrationPayload,
  normalizeSessionPayload
} from "../contracts.js";

export class BackendApiError extends Error {
  constructor(code, detail, status = 500) {
    super(String(detail || code || "backend api error"));
    this.name = "BackendApiError";
    this.code = String(code || "BACKEND_API_ERROR");
    this.status = Number(status || 500);
  }
}

const REGION_COMPLIANCE_CODES = new Set(["REGION_BLOCKED", "REGION_GEO_UNDETERMINED"]);

function asPath(path) {
  const value = String(path || "").trim();
  if (!value) {
    return "/";
  }
  return value.startsWith("/") ? value : `/${value}`;
}

function requireAuthToken(authToken) {
  const token = String(authToken || "").trim();
  if (!token) {
    throw new BackendApiError("AUTH_TOKEN_REQUIRED", "authToken is required for protected endpoint.", 401);
  }
  return token;
}

export function isRegionComplianceError(error) {
  const code = String(error?.code || "").trim().toUpperCase();
  if (REGION_COMPLIANCE_CODES.has(code)) {
    return true;
  }
  const status = Number(error?.status || 0);
  return status === 451;
}

async function parseResponse(response) {
  let payload = {};
  try {
    payload = await response.json();
  } catch (_err) {
    payload = {};
  }
  if (response.ok) {
    return payload;
  }
  const error = payload && payload.error ? payload.error : {};
  throw new BackendApiError(error.code || "BACKEND_API_ERROR", error.detail || "Request failed.", response.status);
}

export function buildBackendClient({ baseUrl = "", fetchImpl = null, locationLike = null } = {}) {
  const runtimeLocation =
    locationLike || (typeof window !== "undefined" && window.location ? window.location : null);
  const resolvedBaseUrl = resolveApiBaseUrl(baseUrl, runtimeLocation).replace(/\/+$/, "");
  const fetcher = typeof fetchImpl === "function" ? fetchImpl : fetch;
  if (typeof fetcher !== "function") {
    throw new BackendApiError("FETCH_UNAVAILABLE", "No fetch implementation was provided.", 500);
  }

  async function request(path, { method = "GET", body = null, headers = null } = {}) {
    const url = `${resolvedBaseUrl}${asPath(path)}`;
    const init = {
      method: String(method || "GET").toUpperCase(),
      headers: { "Content-Type": "application/json" }
    };
    if (headers && typeof headers === "object") {
      Object.assign(init.headers, headers);
    }
    if (body && typeof body === "object") {
      init.body = JSON.stringify(body);
    }
    const response = await fetcher(url, init);
    return parseResponse(response);
  }

  return {
    baseUrl: resolvedBaseUrl,
    async healthLive() {
      return request("/health/live");
    },
    async healthReady() {
      return request("/health/ready");
    },
    async getComplianceRegion() {
      return request("/compliance/region");
    },
    async createSession(payload) {
      const body = normalizeSessionPayload(payload);
      return request("/auth/session", { method: "POST", body: { user_id: body.userId, role: body.role } });
    },
    async registerAccount(payload) {
      const body = normalizeAuthCredentials(payload);
      return request("/auth/register", { method: "POST", body: { user_id: body.userId, password: body.password } });
    },
    async loginWithPassword(payload) {
      const body = normalizeAuthCredentials(payload);
      return request("/auth/login", { method: "POST", body: { user_id: body.userId, password: body.password } });
    },
    async requestLoginCode(payload) {
      const body = normalizeLoginCodeRequestPayload(payload);
      return request("/auth/login/request-code", {
        method: "POST",
        body: { user_id: body.userId, password: body.password }
      });
    },
    async verifyLoginCode(payload) {
      const body = normalizeLoginCodeVerifyPayload(payload);
      return request("/auth/login/verify-code", {
        method: "POST",
        body: { challenge_id: body.challengeId, verification_code: body.verificationCode }
      });
    },
    async whoAmI(authToken) {
      const token = requireAuthToken(authToken);
      return request(`/auth/whoami?auth_token=${encodeURIComponent(token)}`);
    },
    async listProfiles(filters = {}, authToken = "") {
      const token = requireAuthToken(authToken);
      const params = new URLSearchParams();
      const keys = ["vendor", "model", "nozzle", "process", "filament"];
      for (const key of keys) {
        const value = String(filters[key] || "").trim();
        if (value) {
          params.set(key, value);
        }
      }
      params.set("auth_token", token);
      const query = params.toString();
      const suffix = query ? `?${query}` : "";
      return request(`/profiles/catalog${suffix}`);
    },
    async registerPrinter(payload) {
      const body = normalizePrinterRegistrationPayload(payload);
      const token = requireAuthToken(payload?.authToken);
      return request("/printers/register", {
        method: "POST",
        body: {
          auth_token: token,
          printer_id: body.printerId,
          name: body.name,
          connector_type: body.connectorType,
          endpoint: body.endpoint
        }
      });
    },
    async submitJob(payload) {
      const body = normalizePrintRequestPayload(payload);
      const token = requireAuthToken(payload?.authToken);
      return request("/jobs/submit", {
        method: "POST",
        body: {
          auth_token: token,
          model_name: body.modelName,
          profile_id: body.profileId,
          requested_by: body.requestedBy,
          printer_id: body.printerId
        }
      });
    },
    async uploadModel(payload) {
      const body = normalizeModelUploadPayload(payload);
      const token = requireAuthToken(payload?.authToken);
      return request("/jobs/upload-model", {
        method: "POST",
        body: {
          auth_token: token,
          file_name: body.fileName,
          data_base64: body.dataBase64
        }
      });
    },
    async getJobStatus(jobId, authToken = "") {
      const normalized = String(jobId || "").trim();
      const token = requireAuthToken(authToken);
      return request(`/jobs/status?job_id=${encodeURIComponent(normalized)}&auth_token=${encodeURIComponent(token)}`);
    },
    async getJobEvents(jobId, authToken = "") {
      const normalized = String(jobId || "").trim();
      const token = requireAuthToken(authToken);
      return request(`/jobs/events?job_id=${encodeURIComponent(normalized)}&auth_token=${encodeURIComponent(token)}`);
    },
    async getQueueSnapshot(authToken = "") {
      const token = requireAuthToken(authToken);
      return request(`/queue/snapshot?auth_token=${encodeURIComponent(token)}`);
    },
    async getActivityFeed(payload = {}) {
      const token = requireAuthToken(payload?.authToken);
      const cursorValue = Number.parseInt(String(payload?.cursor ?? "0"), 10);
      const limitValue = Number.parseInt(String(payload?.limit ?? "200"), 10);
      const cursor = Number.isFinite(cursorValue) ? Math.max(0, cursorValue) : 0;
      const limit = Number.isFinite(limitValue) ? Math.max(1, Math.min(1000, limitValue)) : 200;
      return request(
        `/activity/feed?auth_token=${encodeURIComponent(token)}&cursor=${encodeURIComponent(cursor)}&limit=${encodeURIComponent(limit)}`
      );
    },
    async sendWorkerHeartbeat(payload = {}) {
      const token = requireAuthToken(payload?.authToken);
      const workerId = String(payload?.workerId || "").trim();
      const body = { auth_token: token };
      if (workerId) {
        body.worker_id = workerId;
      }
      return request("/queue/worker/heartbeat", { method: "POST", body });
    },
    async runWorkerTick(payload = {}) {
      const token = requireAuthToken(payload?.authToken);
      const workerId = String(payload?.workerId || "").trim();
      const maxJobs = payload?.maxJobs;
      const body = { auth_token: token };
      if (workerId) {
        body.worker_id = workerId;
      }
      if (maxJobs !== undefined && maxJobs !== null && `${maxJobs}`.trim() !== "") {
        body.max_jobs = maxJobs;
      }
      return request("/queue/worker/tick", { method: "POST", body });
    },
    async getOpsMetrics(authToken = "") {
      const token = requireAuthToken(authToken);
      return request(`/ops/metrics?auth_token=${encodeURIComponent(token)}`);
    },
    async getOpsAudit(authToken = "", limit = 50) {
      const token = requireAuthToken(authToken);
      const normalized = Number.isFinite(Number(limit)) ? Number(limit) : 50;
      return request(`/ops/audit?auth_token=${encodeURIComponent(token)}&limit=${encodeURIComponent(normalized)}`);
    },
    async getReleaseReadiness(authToken = "") {
      const token = requireAuthToken(authToken);
      return request(`/ops/release-readiness?auth_token=${encodeURIComponent(token)}`);
    },
    async setReleaseCheck(payload = {}) {
      const token = requireAuthToken(payload?.authToken);
      const checkName = String(payload?.checkName || "").trim();
      const detail = String(payload?.detail || "").trim();
      const passed = Boolean(payload?.passed);
      return request("/ops/release-readiness/check", {
        method: "POST",
        body: {
          auth_token: token,
          check_name: checkName,
          passed,
          detail
        }
      });
    }
  };
}
