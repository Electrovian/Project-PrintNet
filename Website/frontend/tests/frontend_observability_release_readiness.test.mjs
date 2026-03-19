import test from "node:test";
import assert from "node:assert/strict";

import { BackendApiError, buildBackendClient } from "../src/api/backendClient.js";

test("ops client methods map to observability and release readiness routes", async () => {
  const calls = [];
  const fakeFetch = async (url, init) => {
    calls.push({ url, init });
    return {
      ok: true,
      status: 200,
      async json() {
        return { ok: true };
      }
    };
  };

  const client = buildBackendClient({
    baseUrl: "http://localhost:8000/api/v1",
    fetchImpl: fakeFetch
  });

  await client.getOpsMetrics("session-000001");
  await client.getOpsAudit("session-000001", 20);
  await client.getReleaseReadiness("session-000002");
  await client.setReleaseCheck({
    authToken: "session-000003",
    checkName: "authz_enforced",
    passed: true,
    detail: "validated"
  });

  assert.equal(calls.length, 4);
  assert.match(calls[0].url, /\/ops\/metrics\?/);
  assert.match(calls[1].url, /\/ops\/audit\?/);
  assert.match(calls[2].url, /\/ops\/release-readiness\?/);
  assert.match(calls[3].url, /\/ops\/release-readiness\/check$/);
  assert.equal(calls[3].init.method, "POST");
  const body = JSON.parse(calls[3].init.body);
  assert.equal(body.check_name, "authz_enforced");
  assert.equal(body.passed, true);
});

test("ops client methods require auth token", async () => {
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

  await assert.rejects(() => client.getOpsMetrics(""), BackendApiError);
  await assert.rejects(() => client.getOpsAudit(""), BackendApiError);
  await assert.rejects(() => client.getReleaseReadiness(""), BackendApiError);
  await assert.rejects(() => client.setReleaseCheck({ checkName: "backend_health", passed: true }), BackendApiError);
});
