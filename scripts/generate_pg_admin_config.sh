#!/bin/bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$SCRIPT_DIR/.."
SERVERS_FILE="$BASE_DIR/servers.json"
PGPASS_FILE="$BASE_DIR/pgpass"

cd "$BASE_DIR"
export $(grep -v '^#' ".env" | xargs)
envsubst < "$SERVERS_FILE".template > "$SERVERS_FILE"
envsubst < "$PGPASS_FILE".template > "$PGPASS_FILE"
chmod 600 "$PGPASS_FILE"
