#!/bin/sh
set -eu

TLS_DIR="/etc/nginx/tls"
TLS_CERT_PATH="${PRINTNET_TLS_CERT_PATH:-$TLS_DIR/printnet.crt}"
TLS_KEY_PATH="${PRINTNET_TLS_KEY_PATH:-$TLS_DIR/printnet.key}"
TLS_COMMON_NAME="${PRINTNET_TLS_COMMON_NAME:-localhost}"
TLS_ALT_IP="${PRINTNET_TLS_ALT_IP:-127.0.0.1}"
TLS_ALT_DNS="${PRINTNET_TLS_ALT_DNS:-localhost}"
PRINTNET_API_BASE_URL="${PRINTNET_API_BASE_URL:-/api/v1}"
PRINTNET_FRONTEND_SHARE_URL="${PRINTNET_FRONTEND_SHARE_URL:-}"

mkdir -p "$TLS_DIR"

cat > /tmp/printnet-openssl.cnf <<EOF
[ req ]
default_bits = 2048
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[ req_distinguished_name ]
CN = ${TLS_COMMON_NAME}

[ v3_req ]
subjectAltName = @alt_names
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth

[ alt_names ]
DNS.1 = ${TLS_ALT_DNS}
IP.1 = ${TLS_ALT_IP}
EOF

openssl req \
  -x509 \
  -nodes \
  -newkey rsa:2048 \
  -days 30 \
  -keyout "$TLS_KEY_PATH" \
  -out "$TLS_CERT_PATH" \
  -config /tmp/printnet-openssl.cnf \
  -extensions v3_req >/dev/null 2>&1

envsubst '${PRINTNET_API_BASE_URL} ${PRINTNET_FRONTEND_SHARE_URL}' \
  < /etc/printnet/runtime-config.js.template \
  > /usr/share/nginx/html/runtime-config.js

envsubst '' < /etc/printnet/nginx.conf.template > /etc/nginx/conf.d/default.conf
