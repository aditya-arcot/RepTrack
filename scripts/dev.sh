#!/bin/bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$SCRIPT_DIR/.."
SERVER_DIR="$BASE_DIR/server"
CLIENT_DIR="$BASE_DIR/client"

cd "$SERVER_DIR"
uv sync

cd "$CLIENT_DIR"
npm i

watchexec -r -w "$SERVER_DIR" -e py "$SCRIPT_DIR/generate_api.sh" &
WATCHEXEC_PID=$!

cleanup() {
    echo "Stopping watchexec (PID: $WATCHEXEC_PID)"
    kill $WATCHEXEC_PID
}
trap cleanup EXIT

cd "$BASE_DIR"
docker compose up --watch &

wait
