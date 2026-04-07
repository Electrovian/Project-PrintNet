import { expect, test } from "@playwright/test";

const backendBaseUrl = String(process.env.PRINTNET_API_BASE_URL || "http://127.0.0.1:8000/api/v1").replace(/\/+$/, "");
const password = "SmokePass_123!";
const uniqueSuffix = () => `${Date.now()}-${Math.random().toString(16).slice(2, 8)}`;

async function ensureBackendLive() {
  const response = await fetch(`${backendBaseUrl}/health/live`, {
    headers: {
      Accept: "application/json"
    }
  });
  expect(response.ok, `Backend health endpoint returned ${response.status}`).toBeTruthy();
  const body = await response.json();
  expect(body).toMatchObject({ ok: true });
}

async function seedApiBase(page) {
  await page.addInitScript((baseUrl) => {
    window.__PRINTNET_API_BASE_URL = baseUrl;
  }, backendBaseUrl);
}

async function signUpAndEnterApp(page, email) {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "EON PrintNet" })).toBeVisible();
  await page.getByRole("button", { name: "Sign Up" }).click();
  await page.getByLabel("Display Name (Optional)").fill(`Browser Smoke ${uniqueSuffix()}`);
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Organization").fill("Launch Lab");
  await page.locator(".auth-form input[type='password']").first().fill(password);
  await page.locator(".auth-form input[type='password']").nth(1).fill(password);
  await page.locator(".auth-form").getByRole("button", { name: "Create Account" }).click();
  await expect(page.locator(".header-shell")).toBeVisible();
  await expect(page.locator(".status-chip")).toContainText(/Account created and signed in|Signed in/);
}

async function signIn(page, email) {
  await page.getByRole("button", { name: "Sign Out" }).click();
  await expect(page.getByRole("heading", { name: "EON PrintNet" })).toBeVisible();
  await page.locator(".auth-tabs").getByRole("button", { name: "Sign In" }).click();
  await page.locator(".auth-form").getByLabel("Username or Email").fill(email);
  await page.locator(".auth-form input[type='password']").first().fill(password);
  await page.locator(".auth-form").getByRole("button", { name: "Sign In" }).click();
  await expect(page.locator(".header-shell")).toBeVisible();
  await expect(page.locator(".status-chip")).toContainText("Signed in.");
}

test("loads, authenticates, submits a job, and shows queue visibility", async ({ page }) => {
  await ensureBackendLive();
  await seedApiBase(page);

  const email = `browser.smoke.${uniqueSuffix()}@example.com`;
  const modelName = `browser-smoke-${Date.now()}.stl`;

  await signUpAndEnterApp(page, email);
  await signIn(page, email);

  await page.locator(".header-shell").getByRole("button", { name: "Queue" }).click();
  await expect(page.getByText("Job Queue")).toBeVisible();
  await expect(page.getByText("No submitted job in this session.")).toBeVisible();

  await page.getByRole("button", { name: "Submit Job" }).click();
  await page.getByLabel("Name").fill("Browser Smoke");
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Phone").fill("555-0100");
  await page.getByLabel("Project Notes").fill("Launch torture smoke");
  await page.locator(".dropzone input[type='file']").setInputFiles({
    name: modelName,
    mimeType: "application/sla",
    buffer: Buffer.from("solid browser-smoke\nendsolid browser-smoke\n")
  });

  await page.getByRole("button", { name: "Send to Printer Queue" }).click();
  await expect(page.locator(".status-chip")).toContainText("Job submitted.");

  await page.locator(".header-shell").getByRole("button", { name: "Queue" }).click();
  await expect(page.getByText(modelName)).toBeVisible();
  await expect(page.locator(".queue-count-chip")).not.toHaveText("0 jobs");
});

test("shows an error and maintenance banner when submission is attempted without a file", async ({ page }) => {
  await ensureBackendLive();
  await seedApiBase(page);

  const email = `browser.smoke.error.${uniqueSuffix()}@example.com`;
  await signUpAndEnterApp(page, email);
  await page.getByRole("button", { name: "Submit Job" }).click();
  await page.getByRole("button", { name: "Send to Printer Queue" }).click();

  await expect(page.locator(".status-chip")).toContainText("Failed: Select at least one STL or STEP file before submitting.");
  await expect(page.locator(".maintenance-banner")).toBeVisible();
  await expect(page.locator(".maintenance-banner")).toContainText("Print services temporarily unavailable");
});

test("shows a maintenance banner when the network probe fails after sign-in", async ({ page }) => {
  await ensureBackendLive();
  await seedApiBase(page);

  await page.route(/eon_probe=/, async (route) => {
    await route.fulfill({
      status: 503,
      contentType: "application/json",
      body: JSON.stringify({ error: { code: "TUNNEL_DOWN", detail: "Probe unavailable" } })
    });
  });

  const email = `browser.smoke.maintenance.${uniqueSuffix()}@example.com`;
  await signUpAndEnterApp(page, email);
  await page.evaluate(() => window.dispatchEvent(new Event("online")));
  await expect(page.locator(".maintenance-banner")).toBeVisible();
  await expect(page.locator(".maintenance-banner")).toContainText("Tunnel/network issue detected");
});

test("shows a compliance block when the backend denies the region", async ({ page }) => {
  await ensureBackendLive();
  await seedApiBase(page);

  await page.route(/\/api\/v1\/compliance\/region$/, async (route) => {
    await route.fulfill({
      status: 451,
      contentType: "application/json",
      body: JSON.stringify({
        error: {
          code: "REGION_BLOCKED",
          detail: "Region compliance policy blocked this request."
        },
        compliance: {
          decision: "deny",
          reason_code: "REGION_BLOCKED",
          detail: "Region compliance policy blocked this request.",
          state_code: "blocked",
          backend_env: "browser-smoke",
          unknown_policy: "deny"
        }
      })
    });
  });

  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Service Restricted" })).toBeVisible();
  await expect(page.getByText("Region compliance policy blocked this request.")).toBeVisible();
  await expect(page.getByRole("button", { name: "Retry Check" })).toBeVisible();
});
