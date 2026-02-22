import test from "node:test";
import assert from "node:assert/strict";

import {
  FrontendAuthError,
  allowedRoutes,
  canAccessRoute,
  hasRequiredRole,
  normalizeRole
} from "../src/auth/rolePolicy.js";

test("normalizeRole accepts known roles", () => {
  assert.equal(normalizeRole("Student"), "student");
  assert.equal(normalizeRole("operator"), "operator");
  assert.equal(normalizeRole("ADMIN"), "admin");
});

test("normalizeRole rejects unknown role", () => {
  assert.throws(() => normalizeRole("guest"), FrontendAuthError);
});

test("role ordering enforces minimum role requirements", () => {
  assert.equal(hasRequiredRole("student", "student"), true);
  assert.equal(hasRequiredRole("operator", "student"), true);
  assert.equal(hasRequiredRole("admin", "operator"), true);
  assert.equal(hasRequiredRole("student", "operator"), false);
});

test("route access policy enforces printers route role", () => {
  assert.equal(canAccessRoute("student", "submit"), true);
  assert.equal(canAccessRoute("student", "queue"), true);
  assert.equal(canAccessRoute("student", "printers"), false);
  assert.equal(canAccessRoute("operator", "printers"), true);
  assert.equal(canAccessRoute("admin", "printers"), true);
});

test("allowedRoutes returns deterministic route list", () => {
  assert.deepEqual(allowedRoutes("student"), ["submit", "queue"]);
  assert.deepEqual(allowedRoutes("operator"), ["submit", "queue", "printers"]);
  assert.deepEqual(allowedRoutes("admin"), ["submit", "queue", "printers"]);
});
