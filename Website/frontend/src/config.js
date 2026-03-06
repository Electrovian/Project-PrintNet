export const API_DEFAULTS = Object.freeze({
  protocol: "http",
  host: "127.0.0.1",
  port: 8000,
  prefix: "/api/v1"
});

export const DEFAULT_CONTACT_FORM = Object.freeze({
  name: "",
  email: "",
  phone: ""
});

export const DEFAULT_PRINT_OPTIONS = Object.freeze({
  material: "PLA",
  color: "Black",
  colors: ["Black"],
  infillDensityPct: 25,
  layerHeightMm: 0.2,
  supports: "On (Default)",
  projectNotes: "",
  printerId: ""
});

export const UI_THEME = Object.freeze({
  background: "#05070c",
  panel: "#0f1219",
  panelSoft: "#111723",
  border: "#273449",
  text: "#f1f6ff",
  mutedText: "#9aa7bf",
  accent: "#2d75ff",
  accentSoft: "#0f2a57",
  danger: "#e54949",
  dropZoneBorder: "#38516f"
});

export function resolveApiBaseUrl(explicitBaseUrl = "", locationLike = null) {
  const normalizedExplicit = String(explicitBaseUrl || "").trim();
  if (normalizedExplicit) {
    return normalizedExplicit.replace(/\/+$/, "");
  }
  const runtimeOverride =
    typeof globalThis === "object" && globalThis !== null
      ? String(globalThis.__PRINTNET_API_BASE_URL || "").trim()
      : "";
  if (runtimeOverride) {
    return runtimeOverride.replace(/\/+$/, "");
  }
  if (locationLike && typeof locationLike === "object") {
    const protocol = String(locationLike.protocol || API_DEFAULTS.protocol + ":")
      .replace(/:$/, "")
      .trim();
    const hostname = String(locationLike.hostname || API_DEFAULTS.host).trim();
    const currentPort = String(locationLike.port || "").trim();
    const isLocalHost = hostname === "localhost" || hostname === "127.0.0.1";
    if (!isLocalHost) {
      const maybePort = currentPort ? `:${currentPort}` : "";
      return `${protocol}://${hostname}${maybePort}${API_DEFAULTS.prefix}`;
    }
    const port = currentPort && currentPort !== String(API_DEFAULTS.port)
      ? String(API_DEFAULTS.port)
      : (currentPort || String(API_DEFAULTS.port));
    const maybePort = port ? `:${port}` : "";
    return `${protocol}://${hostname}${maybePort}${API_DEFAULTS.prefix}`;
  }
  return `${API_DEFAULTS.protocol}://${API_DEFAULTS.host}:${API_DEFAULTS.port}${API_DEFAULTS.prefix}`;
}
