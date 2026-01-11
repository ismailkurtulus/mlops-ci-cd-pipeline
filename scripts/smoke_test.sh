#!/usr/bin/env bash
set -e

IMAGE_NAME=${1:-mlops-service:ci}
CONTAINER_NAME=mlops_smoke

docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
docker run -d --name "$CONTAINER_NAME" -p 8000:8000 "$IMAGE_NAME"

# Servisin ayağa kalkması için kısa bekleme
sleep 3

STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u1","item_id":"i1"}')

docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

if [ "$STATUS" != "200" ]; then
  echo "Smoke test failed"
  exit 1
fi

echo "Smoke test passed"
