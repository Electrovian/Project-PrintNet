import test from "node:test";
import assert from "node:assert/strict";

import { BackendApiError, buildBackendClient } from "../src/api/backendClient.js";

test("queue orchestration client methods map paths and methods", async () => {
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

  await client.getQueueSnapshot("session-000001");
  await client.sendWorkerHeartbeat({ authToken: "session-000002", workerId: "worker-01" });
  await client.runWorkerTick({ authToken: "session-000002", workerId: "worker-01", maxJobs: 2 });

  assert.equal(calls.length, 3);
  assert.match(calls[0].url, /\/queue\/snapshot\?/);
  assert.equal(calls[1].init.method, "POST");
  assert.equal(calls[2].init.method, "POST");

  const heartbeatBody = JSON.parse(calls[1].init.body);
  const tickBody = JSON.parse(calls[2].init.body);
  assert.equal(heartbeatBody.worker_id, "worker-01");
  assert.equal(tickBody.max_jobs, 2);
});

test("queue orchestration client methods require auth token", async () => {
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

  await assert.rejects(() => client.getQueueSnapshot(""), BackendApiError);
  await assert.rejects(() => client.sendWorkerHeartbeat({}), BackendApiError);
  await assert.rejects(() => client.runWorkerTick({ maxJobs: 1 }), BackendApiError);
});
