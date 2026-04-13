export const API_DEFAULTS = Object.freeze({
  protocol: "http",
  host: "127.0.0.1",
  port: 8000,
  prefix: "/api/v1"
});

export const FRONTEND_SHARE_DEFAULTS = Object.freeze({
  protocol: "http",
  host: "127.0.0.1",
  port: 8080,
  entryPath: "/signin"
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

function trimTrailingSlash(value) {
  return String(value || "").trim().replace(/\/+$/, "");
}

function trimLeadingSlash(value) {
  return String(value || "").trim().replace(/^\/+/, "");
}

function resolveRuntimeOverride(name) {
  if (typeof globalThis !== "object" || globalThis === null) {
    return "";
  }
  return String(globalThis[name] || "").trim();
}

function resolveEnvOverride(name) {
  try {
    return String(import.meta?.env?.[name] || "").trim();
  } catch (_err) {
    return "";
  }
}

function buildOriginFromLocationLike(locationLike) {
  if (!locationLike || typeof locationLike !== "object") {
    return "";
  }
  const explicitOrigin = trimTrailingSlash(locationLike.origin);
  if (explicitOrigin) {
    return explicitOrigin;
  }
  const protocol = String(locationLike.protocol || `${FRONTEND_SHARE_DEFAULTS.protocol}:`)
    .replace(/:$/, "")
    .trim() || FRONTEND_SHARE_DEFAULTS.protocol;
  const hostname = String(locationLike.hostname || FRONTEND_SHARE_DEFAULTS.host).trim() || FRONTEND_SHARE_DEFAULTS.host;
  const port = String(locationLike.port || "").trim();
  return `${protocol}://${hostname}${port ? `:${port}` : ""}`;
}

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
    const targetPort = Number(API_DEFAULTS.port);
    const normalizedPort = Number.isFinite(targetPort) && targetPort > 0 ? `:${targetPort}` : "";
    return `${protocol}://${hostname}${normalizedPort}${API_DEFAULTS.prefix}`;
  }
  return `${API_DEFAULTS.protocol}://${API_DEFAULTS.host}:${API_DEFAULTS.port}${API_DEFAULTS.prefix}`;
}

export function resolveFrontendShareUrl(explicitShareUrl = "", locationLike = null) {
  const normalizedExplicit = trimTrailingSlash(explicitShareUrl);
  if (normalizedExplicit) {
    return normalizedExplicit;
  }
  const runtimeOverride = trimTrailingSlash(resolveRuntimeOverride("__PRINTNET_FRONTEND_SHARE_URL"));
  if (runtimeOverride) {
    return runtimeOverride;
  }
  const envOverride = trimTrailingSlash(resolveEnvOverride("VITE_PRINTNET_FRONTEND_SHARE_URL"));
  if (envOverride) {
    return envOverride;
  }
  const targetLocation =
    locationLike ||
    (typeof window !== "undefined" && window.location ? window.location : null);
  const origin = trimTrailingSlash(buildOriginFromLocationLike(targetLocation));
  if (origin) {
    return `${origin}/${trimLeadingSlash(FRONTEND_SHARE_DEFAULTS.entryPath)}`;
  }
  return `${FRONTEND_SHARE_DEFAULTS.protocol}://${FRONTEND_SHARE_DEFAULTS.host}:${FRONTEND_SHARE_DEFAULTS.port}${FRONTEND_SHARE_DEFAULTS.entryPath}`;
}

export function inspectFrontendShareUrl(shareUrl = "") {
  const normalized = String(shareUrl || "").trim();
  if (!normalized) {
    return {
      hostname: "",
      isLoopback: false,
      isPrivateNetwork: false,
      supportsLanSharing: false,
      message: "Share link unavailable."
    };
  }

  try {
    const parsed = new URL(normalized);
    const hostname = String(parsed.hostname || "").trim().toLowerCase();
    const isLoopback =
      hostname === "localhost" ||
      hostname === "::1" ||
      hostname === "[::1]" ||
      hostname.startsWith("127.");
    const isPrivateNetwork =
      hostname.startsWith("10.") ||
      hostname.startsWith("192.168.") ||
      /^172\.(1[6-9]|2\d|3[0-1])\./.test(hostname) ||
      hostname.endsWith(".local");
    if (isLoopback) {
      return {
        hostname,
        isLoopback: true,
        isPrivateNetwork: false,
        supportsLanSharing: false,
        message: "This QR uses a local-only host. Open the frontend through its LAN URL before scanning on a phone."
      };
    }
    if (isPrivateNetwork) {
      return {
        hostname,
        isLoopback: false,
        isPrivateNetwork: true,
        supportsLanSharing: true,
        message: "Scan from a device on the same private network to open this frontend."
      };
    }
    return {
      hostname,
      isLoopback: false,
      isPrivateNetwork: false,
      supportsLanSharing: true,
      message: "Share this QR with any device that can reach the published frontend URL."
    };
  } catch (_err) {
    return {
      hostname: "",
      isLoopback: false,
      isPrivateNetwork: false,
      supportsLanSharing: false,
      message: "Share link is not a valid URL."
    };
  }
}
