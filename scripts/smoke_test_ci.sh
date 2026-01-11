#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${1:-hcps:ci}"
PORT="${2:-8000}"

CID=""
cleanup() {
  if [[ -n "${CID}" ]]; then
    docker rm -f "${CID}" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

echo "Starting container from ${IMAGE_NAME}..."
CID="$(docker run -d -p "${PORT}:8000" "${IMAGE_NAME}")"

echo "Waiting for service..."
for i in {1..30}; do
  if curl -fsS "http://localhost:${PORT}/health" >/dev/null; then
    break
  fi
  sleep 1
done

echo "Smoke: /health"
curl -fsS "http://localhost:${PORT}/health" | grep -q '"ok"' || (echo "Health failed" && exit 1)

echo "Smoke: /predict"
HTTP_CODE="$(curl -s -o /tmp/predict_out.json -w "%{http_code}"   -H "Content-Type: application/json"   -d '{"user_id":"user_123"}'   "http://localhost:${PORT}/predict")"

cat /tmp/predict_out.json

if [[ "${HTTP_CODE}" != "200" ]]; then
  echo "Predict failed with HTTP ${HTTP_CODE}"
  exit 1
fi

echo "Smoke test passed."
