#!/bin/sh
set -e

AUTOMATION_DIR=/app/social-automation
LOCK_STAMP="$AUTOMATION_DIR/node_modules/.package-lock.sha256"

# node_modules lives in a named volume, so reinstall whenever the lockfile changes
if [ ! -x "$AUTOMATION_DIR/node_modules/.bin/tsx" ] || ! sha256sum -c --status "$LOCK_STAMP" 2>/dev/null; then
  echo "[entrypoint] Installing social-automation node dependencies..."
  npm ci --prefix "$AUTOMATION_DIR"
  sha256sum "$AUTOMATION_DIR/package-lock.json" > "$LOCK_STAMP"
fi

exec "$@"
