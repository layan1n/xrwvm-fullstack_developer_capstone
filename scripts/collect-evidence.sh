#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE_URL:-http://127.0.0.1:8000}"
OUT="${OUTPUT_DIR:-submission}"
mkdir -p "$OUT"
: "${DEMO_USER:?Set DEMO_USER to a test account username}"
: "${DEMO_PASSWORD:?Set DEMO_PASSWORD to its password}"
: "${DEALER_ID:=1}"
COOKIE=$(mktemp)
trap 'rm -f "$COOKIE"' EXIT
capture() {
  local file="$1"; shift
  { printf 'curl '; printf '%q ' "$@"; printf '\n'; curl -fsS "$@"; printf '\n'; } > "$OUT/$file"
}
# Use a disposable test account; never submit production credentials.
PAYLOAD=$(python -c 'import os,json;print(json.dumps({"userName":os.environ["DEMO_USER"],"password":os.environ["DEMO_PASSWORD"]}))')
capture loginuser -c "$COOKIE" -H 'Content-Type: application/json' -d "$PAYLOAD" "$BASE/djangoapp/login"
capture logoutuser -b "$COOKIE" "$BASE/djangoapp/logout"
capture getdealerreviews "$BASE/djangoapp/reviews/dealer/$DEALER_ID"
capture getalldealers "$BASE/djangoapp/get_dealers"
capture getdealerbyid "$BASE/djangoapp/dealer/$DEALER_ID"
capture getdealersbyState "$BASE/djangoapp/get_dealers/Kansas"
capture getallcarmakes "$BASE/djangoapp/get_cars"
capture analyzereview "$BASE/djangoapp/analyze/Fantastic%20services"
if [[ -n "${DEPLOYMENT_URL:-}" ]]; then printf '%s\n' "$DEPLOYMENT_URL" > "$OUT/deploymentURL"; fi
