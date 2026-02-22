import test from "node:test";
import assert from "node:assert/strict";

import {
  DEFAULT_CONTACT_FORM,
  DEFAULT_PRINT_OPTIONS,
  resolveApiBaseUrl
} from "../src/config.js";
import {
  FrontendContractError,
  normalizeContactPayload,
  normalizePrintRequestPayload,
  normalizePrinterRegistrationPayload,
  normalizeSessionPayload
} from "../src/contracts.js";
import { BackendApiError, buildBackendClient } from "../src/api/backendClient.js";

test("resolveApiBaseUrl uses explicit base url", () => {
  const value = resolveApiBaseUrl("http://localhost:9000/api/v9/");
  assert.equal(value, "http://localhost:9000/api/v9");
});

test("resolveApiBaseUrl uses location-like fallback", () => {
  const value = resolveApiBaseUrl("", { protocol: "https:", hostname: "example.com", port: "443" });
  assert.equal(value, "https://example.com:443/api/v1");
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
  await client.healthLive();
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
  assert.equal(calls.length, 6);
  assert.equal(calls[0].url, "http://localhost:8000/api/v1/health/live");
  assert.equal(calls[1].url, "http://localhost:8000/api/v1/auth/session");
  assert.match(calls[2].url, /\/auth\/whoami\?/);
  assert.match(calls[3].url, /\/profiles\/catalog\?/);
  assert.equal(calls[4].init.method, "POST");
  assert.equal(calls[5].init.method, "POST");
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
