import { defineConfig } from "@playwright/test";

const frontendPort = Number.parseInt(String(process.env.PRINTNET_FRONTEND_PORT || "4173"), 10) || 4173;
const frontendBaseUrl = `http://127.0.0.1:${frontendPort}`;

export default defineConfig({
  testDir: "./tests",
  testMatch: /browser_smoke\.spec\.mjs$/,
  timeout: 45_000,
  expect: {
    timeout: 10_000
  },
  use: {
    baseURL: frontendBaseUrl,
    trace: "retain-on-failure",
    screenshot: "only-on-failure"
  },
  webServer: {
    command: `npm run dev -- --host 127.0.0.1 --port ${frontendPort} --strictPort`,
    url: frontendBaseUrl,
    reuseExistingServer: true,
    timeout: 120_000
  }
});
