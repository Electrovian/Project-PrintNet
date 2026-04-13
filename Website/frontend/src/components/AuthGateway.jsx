import { useEffect, useMemo, useState } from "react";
import { FrontendShareCard } from "./FrontendShareCard.jsx";

const HUBS = [
  { x: 20, y: 38, spreadX: 10, spreadY: 8, weight: 36 }, // North America
  { x: 27, y: 70, spreadX: 8, spreadY: 9, weight: 16 }, // South America
  { x: 49, y: 34, spreadX: 8, spreadY: 6, weight: 34 }, // Europe
  { x: 50, y: 56, spreadX: 10, spreadY: 9, weight: 20 }, // Africa
  { x: 66, y: 43, spreadX: 12, spreadY: 10, weight: 38 }, // Asia
  { x: 82, y: 72, spreadX: 9, spreadY: 8, weight: 14 }, // Australia
  { x: 64, y: 80, spreadX: 6, spreadY: 4, weight: 6 } // South Asia / Indian Ocean
];

const CONTINENTS = [
  "M82 112 L180 64 L268 78 L330 116 L350 172 L332 236 L286 266 L210 248 L156 206 L102 146 Z",
  "M246 276 L288 298 L326 350 L318 410 L288 470 L238 454 L212 390 L226 330 Z",
  "M420 92 L478 76 L552 98 L574 132 L548 166 L492 170 L444 154 L408 126 Z",
  "M454 178 L516 194 L560 238 L548 326 L504 394 L456 356 L434 286 L438 226 Z",
  "M566 106 L676 118 L760 164 L828 236 L786 304 L712 308 L660 262 L602 246 L556 196 Z",
  "M778 326 L860 344 L910 390 L900 450 L834 466 L768 426 L748 366 Z",
  "M344 154 L402 144 L426 164 L398 192 L350 194 Z"
];

const CORE_LINKS = [
  [0, 2],
  [0, 4],
  [2, 4],
  [2, 3],
  [4, 5],
  [1, 0],
  [1, 3],
  [3, 4],
  [6, 4],
  [6, 3]
];

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function seededRng(seed) {
  let state = seed >>> 0;
  return () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 0xffffffff;
  };
}

function buildGraph() {
  const rand = seededRng(980421);
  const nodes = [];
  const hubStart = [];

  HUBS.forEach((hub) => {
    hubStart.push(nodes.length);
    for (let i = 0; i < hub.weight; i += 1) {
      const driftX = (rand() - 0.5) * hub.spreadX * 2;
      const driftY = (rand() - 0.5) * hub.spreadY * 2;
      nodes.push({
        x: clamp(hub.x + driftX, 3, 97),
        y: clamp(hub.y + driftY, 6, 94),
        phase: rand(),
        radius: rand() < 0.24 ? 0.44 : 0.33
      });
    }
  });

  const links = [];

  CORE_LINKS.forEach(([a, b]) => {
    const fromIndex = hubStart[a] + Math.floor(rand() * HUBS[a].weight);
    const toIndex = hubStart[b] + Math.floor(rand() * HUBS[b].weight);
    links.push({
      a: nodes[fromIndex],
      b: nodes[toIndex],
      delay: rand() * 4
    });
  });

  for (let i = 0; i < 96; i += 1) {
    const hubA = Math.floor(rand() * HUBS.length);
    const shift = rand() < 0.72 ? 1 : 2 + Math.floor(rand() * 4);
    const hubB = (hubA + shift) % HUBS.length;
    const fromIndex = hubStart[hubA] + Math.floor(rand() * HUBS[hubA].weight);
    const toIndex = hubStart[hubB] + Math.floor(rand() * HUBS[hubB].weight);
    links.push({
      a: nodes[fromIndex],
      b: nodes[toIndex],
      delay: rand() * 5
    });
  }

  return { nodes, links };
}

function normalizeUserId({ email, org, username }) {
  const trimmedEmail = String(email || "").trim().toLowerCase();
  if (trimmedEmail) {
    return trimmedEmail.replace(/\s+/g, "");
  }
  const trimmedUser = String(username || "").trim().toLowerCase();
  if (trimmedUser) {
    const cleanedUser = trimmedUser.replace(/\s+/g, ".").replace(/[^a-z0-9._@+\-]/g, "");
    if (cleanedUser) {
      return cleanedUser;
    }
  }
  const trimmedOrg = String(org || "").trim().replace(/\s+/g, "-").toLowerCase();
  return trimmedOrg ? `user@${trimmedOrg}.local` : "web-user";
}

function ConnectionMapBackdrop({ graph }) {
  return (
    <div className="auth-map-shell" aria-hidden="true">
      <svg className="auth-map-svg" viewBox="0 0 1000 520" preserveAspectRatio="xMidYMid slice">
        <defs>
          <linearGradient id="oceanGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#07182f" />
            <stop offset="45%" stopColor="#0b2f57" />
            <stop offset="100%" stopColor="#081e3f" />
          </linearGradient>
          <radialGradient id="nodeGlow" cx="50%" cy="50%" r="60%">
            <stop offset="0%" stopColor="rgba(255, 240, 97, 0.95)" />
            <stop offset="100%" stopColor="rgba(255, 240, 97, 0)" />
          </radialGradient>
        </defs>

        <rect x="0" y="0" width="1000" height="520" fill="url(#oceanGradient)" />

        <g className="auth-map-continents">
          {CONTINENTS.map((path) => (
            <path key={path} d={path} />
          ))}
        </g>

        <g className="auth-map-links">
          {graph.links.map((link, index) => (
            <line
              // eslint-disable-next-line react/no-array-index-key
              key={`link-${index}`}
              x1={link.a.x * 10}
              y1={link.a.y * 5.2}
              x2={link.b.x * 10}
              y2={link.b.y * 5.2}
              style={{ "--delay": `${link.delay}s` }}
            />
          ))}
        </g>

        <g className="auth-map-glow">
          {graph.nodes.map((node, index) => (
            <circle
              // eslint-disable-next-line react/no-array-index-key
              key={`glow-${index}`}
              cx={node.x * 10}
              cy={node.y * 5.2}
              r={node.radius * 10}
              fill="url(#nodeGlow)"
              style={{ "--delay": `${node.phase * 3.5}s` }}
            />
          ))}
        </g>

        <g className="auth-map-nodes">
          {graph.nodes.map((node, index) => (
            <circle
              // eslint-disable-next-line react/no-array-index-key
              key={`node-${index}`}
              cx={node.x * 10}
              cy={node.y * 5.2}
              r={node.radius * 2.2}
              style={{ "--delay": `${node.phase * 3.5}s` }}
            />
          ))}
        </g>
      </svg>
      <div className="auth-map-vignette" />
    </div>
  );
}

export function AuthGateway({ onAuthenticate, statusLine }) {
  const graph = useMemo(() => buildGraph(), []);
  const [mode, setMode] = useState("signin");
  const [form, setForm] = useState({
    username: "",
    email: "",
    org: "",
    password: "",
    confirmPassword: "",
    verificationCode: ""
  });
  const [pendingVerification, setPendingVerification] = useState(null);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    const syncModeFromPath = () => {
      const pathname = String(window.location?.pathname || "/").toLowerCase();
      if (pathname === "/register") {
        setMode("signup");
        return;
      }
      if (pathname === "/verify") {
        setMode("verify");
        return;
      }
      if (pathname === "/sso") {
        setMode("sso");
        return;
      }
      setMode("signin");
    };
    syncModeFromPath();
    window.addEventListener("popstate", syncModeFromPath);
    return () => {
      window.removeEventListener("popstate", syncModeFromPath);
    };
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") {
      return;
    }
    let targetPath = "/signin";
    if (mode === "signup") {
      targetPath = "/register";
    } else if (mode === "verify") {
      targetPath = "/verify";
    } else if (mode === "sso") {
      targetPath = "/sso";
    }
    const currentPath = String(window.location?.pathname || "/");
    if (currentPath !== targetPath) {
      window.history.replaceState({}, "", targetPath);
    }
  }, [mode]);

  function setField(key, value) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  function switchMode(nextMode) {
    setMode(nextMode);
    if (nextMode !== "verify") {
      setPendingVerification(null);
      setField("verificationCode", "");
    }
  }

  const isSignUp = mode === "signup";
  const isVerify = mode === "verify";
  const submitLabel = isSignUp ? "Create Account" : isVerify ? "Verify Code" : "Sign In";

  useEffect(() => {
    setMessage("");
  }, [mode]);

  async function submitAuth(event) {
    event.preventDefault();
    if (busy) {
      return;
    }
    setBusy(true);
    setMessage("");
    try {
      if (isVerify) {
        const challengeId = String(pendingVerification?.challengeId || "").trim();
        const verificationCode = String(form.verificationCode || "").trim();
        if (!challengeId) {
          throw new Error("Verification session expired. Sign in again.");
        }
        if (!verificationCode) {
          throw new Error("Verification code is required.");
        }
        await onAuthenticate({
          mode: "signin",
          step: "verify",
          userId: String(pendingVerification?.userId || "").trim(),
          challengeId,
          verificationCode
        });
        setPendingVerification(null);
        return;
      }
      if (isSignUp && String(form.password || "") !== String(form.confirmPassword || "")) {
        setMessage("Passwords do not match.");
        return;
      }
      const userId = normalizeUserId(form);
      const result = await onAuthenticate({
        mode: isSignUp ? "signup" : "signin",
        step: isSignUp ? "signup" : "password",
        userId,
        password: String(form.password || "")
      });
      if (!isSignUp && result?.requiresVerification) {
        const challengeId = String(result?.challengeId || "").trim();
        if (!challengeId) {
          throw new Error("Verification challenge is missing.");
        }
        setPendingVerification({
          challengeId,
          userId,
          delivery: result?.delivery || null,
          debugCode: String(result?.debugCode || "")
        });
        switchMode("verify");
        const destination = String(result?.delivery?.destination || "").trim();
        const debugCode = String(result?.debugCode || "").trim();
        const pieces = [];
        pieces.push(
          destination
            ? `Verification code sent to ${destination}.`
            : "Verification code sent."
        );
        if (debugCode) {
          pieces.push(`Dev code: ${debugCode}`);
        }
        setMessage(pieces.join(" "));
      }
    } catch (err) {
      setMessage(String(err?.message || err || "Unable to authenticate."));
    } finally {
      setBusy(false);
    }
  }

  async function signInWith(provider) {
    void provider;
    setMessage("SSO is disabled until a provider is configured. Use Sign In or Sign Up.");
  }

  return (
    <div className="auth-scene">
      <ConnectionMapBackdrop graph={graph} />

      <div className="auth-stage">
        <section className="auth-card" aria-label="Authentication">
          <div className="auth-brand">
            <h1>EON PrintNet</h1>
            <p>Connected print operations across every lab.</p>
          </div>

          <div className="auth-tabs" role="tablist" aria-label="Authentication Modes">
            <button
              className={mode === "signin" || mode === "verify" ? "auth-tab is-active" : "auth-tab"}
              type="button"
              onClick={() => switchMode("signin")}
            >
              Sign In
            </button>
            <button
              className={mode === "signup" ? "auth-tab is-active" : "auth-tab"}
              type="button"
              onClick={() => switchMode("signup")}
            >
              Sign Up
            </button>
            <button
              className={mode === "sso" ? "auth-tab is-active" : "auth-tab"}
              type="button"
              onClick={() => switchMode("sso")}
            >
              SSO
            </button>
          </div>

          {mode === "sso" ? (
            <div className="auth-sso-panel">
              <button type="button" className="sso-btn sso-facebook" onClick={() => signInWith("facebook")}>
                Enter with Facebook
              </button>
              <button type="button" className="sso-btn sso-google" onClick={() => signInWith("google")}>
                Enter with Google
              </button>
              <button type="button" className="sso-btn sso-microsoft" onClick={() => signInWith("microsoft")}>
                Enter with Microsoft
              </button>
            </div>
          ) : (
            <form className="auth-form" onSubmit={submitAuth}>
              {isVerify ? (
                <>
                  <label className="auth-label">
                    <span>Verification Destination</span>
                    <input
                      type="text"
                      value={String(pendingVerification?.delivery?.destination || "")}
                      readOnly
                    />
                  </label>
                  <label className="auth-label">
                    <span>Verification Code</span>
                    <input
                      type="text"
                      value={form.verificationCode}
                      onChange={(event) => setField("verificationCode", event.target.value)}
                      autoComplete="one-time-code"
                      placeholder="6-digit code"
                      required
                    />
                  </label>
                </>
              ) : isSignUp ? (
                <label className="auth-label">
                  <span>Display Name (Optional)</span>
                  <input
                    type="text"
                    value={form.username}
                    onChange={(event) => setField("username", event.target.value)}
                    placeholder="Alex Rivera"
                    autoComplete="name"
                  />
                </label>
              ) : (
                <label className="auth-label">
                  <span>Username or Email</span>
                  <input
                    type="text"
                    value={form.email}
                    onChange={(event) => setField("email", event.target.value)}
                    placeholder="you@school.edu"
                    autoComplete="username"
                    required
                  />
                </label>
              )}

              {isSignUp ? (
                <label className="auth-label">
                  <span>Email</span>
                  <input
                    type="email"
                    value={form.email}
                    onChange={(event) => setField("email", event.target.value)}
                    placeholder="you@school.edu"
                    autoComplete="email"
                    required
                  />
                </label>
              ) : null}

              {isSignUp ? (
                <label className="auth-label">
                  <span>Organization</span>
                  <input
                    type="text"
                    value={form.org}
                    onChange={(event) => setField("org", event.target.value)}
                    placeholder="University Print Lab"
                  />
                </label>
              ) : null}

              <label className="auth-label">
                <span>Password</span>
                <input
                  type="password"
                  value={form.password}
                  onChange={(event) => setField("password", event.target.value)}
                  autoComplete={isSignUp ? "new-password" : "current-password"}
                  required
                />
              </label>

              {isSignUp ? (
                <label className="auth-label">
                  <span>Confirm Password</span>
                  <input
                    type="password"
                    value={form.confirmPassword}
                    onChange={(event) => setField("confirmPassword", event.target.value)}
                    autoComplete="new-password"
                    required
                  />
                </label>
              ) : null}

              <button className="auth-submit" type="submit" disabled={busy}>
                {busy ? "Connecting..." : submitLabel}
              </button>
            </form>
          )}

          <div className="auth-footnote">
            <span>{message || (busy ? statusLine : "Secure session ready.")}</span>
            <a href="#forgot-password" onClick={(event) => event.preventDefault()}>
              Forgot password?
            </a>
          </div>
        </section>

        <FrontendShareCard />
      </div>
    </div>
  );
}
