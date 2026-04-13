import { useEffect, useMemo, useState } from "react";
import QRCode from "qrcode";

import { inspectFrontendShareUrl, resolveFrontendShareUrl } from "../config.js";

export function FrontendShareCard({ shareUrl = "" }) {
  const resolvedShareUrl = useMemo(() => {
    const locationLike = typeof window !== "undefined" && window.location ? window.location : null;
    return resolveFrontendShareUrl(shareUrl, locationLike);
  }, [shareUrl]);
  const shareMeta = useMemo(() => inspectFrontendShareUrl(resolvedShareUrl), [resolvedShareUrl]);
  const [qrMarkup, setQrMarkup] = useState("");
  const [copyStatus, setCopyStatus] = useState("");

  useEffect(() => {
    let active = true;

    async function renderQr() {
      if (!resolvedShareUrl) {
        setQrMarkup("");
        return;
      }
      try {
        const svgMarkup = await QRCode.toString(resolvedShareUrl, {
          type: "svg",
          errorCorrectionLevel: "M",
          margin: 1,
          color: {
            dark: "#081120",
            light: "#ffffffff"
          }
        });
        if (active) {
          setQrMarkup(svgMarkup);
        }
      } catch (_err) {
        if (active) {
          setQrMarkup("");
        }
      }
    }

    void renderQr();
    return () => {
      active = false;
    };
  }, [resolvedShareUrl]);

  useEffect(() => {
    if (!copyStatus || typeof window === "undefined") {
      return undefined;
    }
    const timeoutId = window.setTimeout(() => {
      setCopyStatus("");
    }, 2400);
    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [copyStatus]);

  async function copyLink() {
    if (!resolvedShareUrl) {
      setCopyStatus("Link unavailable");
      return;
    }
    try {
      if (!navigator?.clipboard?.writeText) {
        throw new Error("Clipboard unavailable");
      }
      await navigator.clipboard.writeText(resolvedShareUrl);
      setCopyStatus("Link copied");
    } catch (_err) {
      setCopyStatus("Copy unavailable");
    }
  }

  function openLink() {
    if (!resolvedShareUrl || typeof window === "undefined") {
      return;
    }
    window.open(resolvedShareUrl, "_blank", "noopener,noreferrer");
  }

  return (
    <aside className="frontend-share-card" aria-label="Frontend mobile access">
      <div className="share-card-kicker">Mobile Access</div>
      <h2>Scan To Open PrintNet</h2>
      <p className="share-card-copy">Use your phone camera to jump into the same frontend entry point.</p>

      <div className="share-qr-shell">
        {qrMarkup ? (
          <div
            className="share-qr-markup"
            aria-label="QR code for frontend access"
            dangerouslySetInnerHTML={{ __html: qrMarkup }}
          />
        ) : (
          <div className="share-qr-placeholder">Generating QR...</div>
        )}
      </div>

      <div className="share-link-block">
        <span className="share-link-label">Share URL</span>
        <code>{resolvedShareUrl}</code>
      </div>

      <div className="share-card-actions">
        <button type="button" className="share-card-btn" onClick={copyLink}>
          Copy Link
        </button>
        <button type="button" className="share-card-btn share-card-btn-accent" onClick={openLink}>
          Open Link
        </button>
      </div>

      <p className={shareMeta.supportsLanSharing ? "share-card-note" : "share-card-note is-warning"}>
        {shareMeta.message}
      </p>
      {copyStatus ? <div className="share-copy-status" role="status">{copyStatus}</div> : null}
    </aside>
  );
}
