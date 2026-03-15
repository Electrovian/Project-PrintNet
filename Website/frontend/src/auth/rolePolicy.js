export class FrontendAuthError extends Error {
  constructor(code, detail) {
    super(String(detail || code || "frontend auth error"));
    this.name = "FrontendAuthError";
    this.code = String(code || "FRONTEND_AUTH_ERROR");
  }
}

export const ROLE_ORDER = Object.freeze({
  student: 1,
  operator: 2,
  admin: 3
});

const ROUTE_REQUIREMENTS = Object.freeze({
  submit: "student",
  queue: "student",
  printers: "operator"
});

export function normalizeRole(role) {
  const value = String(role || "").trim().toLowerCase() || "student";
  if (!Object.hasOwn(ROLE_ORDER, value)) {
    throw new FrontendAuthError("ROLE_INVALID", "role must be student/operator/admin.");
  }
  return value;
}

export function hasRequiredRole(currentRole, requiredRole) {
  const current = normalizeRole(currentRole);
  const required = normalizeRole(requiredRole);
  return ROLE_ORDER[current] >= ROLE_ORDER[required];
}

export function canAccessRoute(role, routeKey) {
  const required = ROUTE_REQUIREMENTS[String(routeKey || "").trim()] || "student";
  return hasRequiredRole(role, required);
}

export function allowedRoutes(role) {
  const normalized = normalizeRole(role);
  const result = [];
  for (const routeKey of Object.keys(ROUTE_REQUIREMENTS)) {
    if (canAccessRoute(normalized, routeKey)) {
      result.push(routeKey);
    }
  }
  return result;
}
