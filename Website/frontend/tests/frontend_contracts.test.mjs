import test from "node:test";
import assert from "node:assert/strict";

import {
  DEFAULT_CONTACT_FORM,
  DEFAULT_PRINT_OPTIONS,
  inspectFrontendShareUrl,
  resolveApiBaseUrl,
  resolveFrontendShareUrl
} from "../src/config.js";
import {
  FrontendContractError,
  normalizeAuthCredentials,
  normalizeContactPayload,
  normalizePrintRequestPayload,
  normalizePrinterRegistrationPayload,
  normalizeSessionPayload
} from "../src/contracts.js";
import { BackendApiError, buildBackendClient, isRegionComplianceError } from "../src/api/backendClient.js";

test("resolveApiBaseUrl uses explicit base url", () => {
  const value = resolveApiBaseUrl("http://localhost:9000/api/v9/");
  assert.equal(value, "http://localhost:9000/api/v9");
});

test("resolveApiBaseUrl uses location-like fallback", () => {
  const value = resolveApiBaseUrl("", { protocol: "https:", hostname: "example.com", port: "443" });
  assert.equal(value, "https://example.com:8000/api/v1");
});

test("resolveApiBaseUrl uses backend default port when ui uses another port", () => {
  const value = resolveApiBaseUrl("", { protocol: "http:", hostname: "127.0.0.1", port: "8080" });
  assert.equal(value, "http://127.0.0.1:8000/api/v1");
});

test("resolveFrontendShareUrl prefers explicit and runtime share overrides", () => {
  assert.equal(resolveFrontendShareUrl("https://printnet.school.edu/launch"), "https://printnet.school.edu/launch");
  globalThis.__PRINTNET_FRONTEND_SHARE_URL = "http://192.168.1.145:8080/signin";
  try {
    assert.equal(resolveFrontendShareUrl("", { origin: "http://localhost:8080" }), "http://192.168.1.145:8080/signin");
  } finally {
    delete globalThis.__PRINTNET_FRONTEND_SHARE_URL;
  }
});

test("resolveFrontendShareUrl derives signin link from current frontend origin", () => {
  const value = resolveFrontendShareUrl("", { origin: "https://printnet.school.edu" });
  assert.equal(value, "https://printnet.school.edu/signin");
});

test("inspectFrontendShareUrl flags loopback and private-network targets", () => {
  const local = inspectFrontendShareUrl("http://127.0.0.1:8080/signin");
  assert.equal(local.isLoopback, true);
  assert.equal(local.supportsLanSharing, false);
  assert.match(local.message, /LAN URL/i);

  const lan = inspectFrontendShareUrl("http://192.168.1.145:8080/signin");
  assert.equal(lan.isPrivateNetwork, true);
  assert.equal(lan.supportsLanSharing, true);
});

test("default form and print options are stable", () => {
  assert.equal(DEFAULT_CONTACT_FORM.name, "");
  assert.equal(DEFAULT_PRINT_OPTIONS.material, "PLA");
  assert.equal(DEFAULT_PRINT_OPTIONS.color, "Black");
});

test("normalizeContactPayload validates required fields", () => {
  assert.throws(() => normalizeContactPayload({ name: "A", email: "bad-email", phone: "123" }), FrontendContractError);
  const payload = normalizeContactPayload({ name: "A", email: "a@example.com", phone: "123" });
  assert.equal(payload.email, "a@example.com");
});

test("normalize payload helpers produce backend-ready shapes", () => {
  const session = normalizeSessionPayload({ userId: "student-1", role: "Student" });
  assert.equal(session.userId, "student-1");
  assert.equal(session.role, "student");
  const creds = normalizeAuthCredentials({ userId: "User.One", password: "password-123" });
  assert.equal(creds.userId, "user.one");
  assert.equal(creds.password, "password-123");
  const printer = normalizePrinterRegistrationPayload({
    printerId: "printer-1",
    name: "Printer 1",
    connectorType: "OctoPrint",
    endpoint: "http://127.0.0.1:5000"
  });
  assert.equal(printer.connectorType, "octoprint");
  const job = normalizePrintRequestPayload({
    modelName: "part.stl",
    profileId: "p-default-pla",
    requestedBy: "student-1",
    printerId: "printer-1"
  });
  assert.equal(job.profileId, "p-default-pla");
});

test("backend client performs path mapping", async () => {
  const calls = [];
  const fakeFetch = async (url, init) => {
    calls.push({ url, init });
    return {
      ok: true,
      status: 200,
      async json() {
        return { ok: true, url, method: init.method };
      }
    };
  };
  const client = buildBackendClient({
    baseUrl: "http://localhost:8000/api/v1",
    fetchImpl: fakeFetch
  });
  await client.getComplianceRegion();
  await client.healthLive();
  await client.registerAccount({ userId: "student-1", password: "password-123" });
  await client.requestLoginCode({ userId: "student-1", password: "password-123" });
  await client.verifyLoginCode({ challengeId: "challenge-000001", verificationCode: "123456" });
  await client.loginWithPassword({ userId: "student-1", password: "password-123" });
  await client.createSession({ userId: "student-1", role: "student" });
  await client.whoAmI("session-000001");
  await client.listProfiles({ vendor: "EON", filament: "PLA" }, "session-000001");
  await client.registerPrinter({
    authToken: "session-000002",
    printerId: "printer-01",
    name: "Lab Printer",
    connectorType: "moonraker",
    endpoint: "http://127.0.0.1:7125"
  });
  await client.submitJob({
    authToken: "session-000001",
    modelName: "sample.stl",
    profileId: "p-default-pla",
    requestedBy: "student-1",
    printerId: "printer-01"
  });
  await client.getActivityFeed({ authToken: "session-000001", cursor: 0, limit: 50 });
  assert.equal(calls.length, 12);
  assert.equal(calls[0].url, "http://localhost:8000/api/v1/compliance/region");
  assert.equal(calls[1].url, "http://localhost:8000/api/v1/health/live");
  assert.equal(calls[2].url, "http://localhost:8000/api/v1/auth/register");
  assert.equal(calls[3].url, "http://localhost:8000/api/v1/auth/login/request-code");
  assert.equal(calls[4].url, "http://localhost:8000/api/v1/auth/login/verify-code");
  assert.equal(calls[5].url, "http://localhost:8000/api/v1/auth/login");
  assert.equal(calls[6].url, "http://localhost:8000/api/v1/auth/session");
  assert.match(calls[7].url, /\/auth\/whoami\?/);
  assert.match(calls[8].url, /\/profiles\/catalog\?/);
  assert.equal(calls[9].init.method, "POST");
  assert.equal(calls[10].init.method, "POST");
  assert.match(calls[11].url, /\/activity\/feed\?/);
});

test("backend client raises BackendApiError on non-ok response", async () => {
  const fakeFetch = async () => ({
    ok: false,
    status: 400,
    async json() {
      return {
        ok: false,
        error: { code: "BACKEND_VALIDATION_ERROR", detail: "bad payload" }
      };
    }
  });
  const client = buildBackendClient({
    baseUrl: "http://localhost:8000/api/v1",
    fetchImpl: fakeFetch
  });
  await assert.rejects(() => client.healthReady(), BackendApiError);
});

test("backend client requires auth token for protected requests", async () => {
  const fakeFetch = async () => ({
    ok: true,
    status: 200,
    async json() {
      return { ok: true };
    }
  });
  const client = buildBackendClient({
    baseUrl: "http://localhost:8000/api/v1",
    fetchImpl: fakeFetch
  });
  await assert.rejects(() => client.listProfiles({ vendor: "EON" }), BackendApiError);
  await assert.rejects(
    () =>
      client.submitJob({
        modelName: "sample.stl",
        profileId: "p-default-pla",
        requestedBy: "student-1",
        printerId: "printer-01"
      }),
    BackendApiError
  );
});

test("isRegionComplianceError detects region lock responses", () => {
  assert.equal(isRegionComplianceError({ code: "REGION_BLOCKED", status: 451 }), true);
  assert.equal(isRegionComplianceError({ code: "REGION_GEO_UNDETERMINED", status: 451 }), true);
  assert.equal(isRegionComplianceError({ code: "BACKEND_VALIDATION_ERROR", status: 400 }), false);
});
