#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
APP_BINARY="${1:-$ROOT_DIR/dist/EON-OpenSlicer}"
APP_VERSION="${2:-1.0.0}"
APP_ARCH="${3:-amd64}"

if [[ ! -f "$APP_BINARY" ]]; then
  echo "missing app binary: $APP_BINARY" >&2
  exit 1
fi

PKG_ROOT="$ROOT_DIR/dist/deb_pkg"
OUTPUT_DEB="$ROOT_DIR/dist/eon-openslicer_${APP_VERSION}_${APP_ARCH}.deb"

rm -rf "$PKG_ROOT"
mkdir -p "$PKG_ROOT/DEBIAN" "$PKG_ROOT/usr/local/bin" "$PKG_ROOT/usr/share/applications"

cat > "$PKG_ROOT/DEBIAN/control" <<EOF
Package: eon-openslicer
Version: ${APP_VERSION}
Section: graphics
Priority: optional
Architecture: ${APP_ARCH}
Maintainer: EON <support@printnet.local>
Depends: libgl1, libxkbcommon0
Description: EON OpenSlicer desktop application
  Includes first-launch setup wizard for language and region bootstrap.
EOF

install -m 0755 "$APP_BINARY" "$PKG_ROOT/usr/local/bin/eon-openslicer"

cat > "$PKG_ROOT/usr/share/applications/eon-openslicer.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=EON OpenSlicer
Exec=/usr/local/bin/eon-openslicer
Terminal=false
Categories=Graphics;Utility;
EOF

dpkg-deb --build "$PKG_ROOT" "$OUTPUT_DEB"
echo "built: $OUTPUT_DEB"
