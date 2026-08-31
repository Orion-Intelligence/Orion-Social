#!/bin/sh
set -e

if [ ! -x /app/social-automation/node_modules/.bin/tsx ]; then
  echo "[entrypoint] Installing social-automation node dependencies..."
  npm ci --prefix /app/social-automation
fi

exec "$@"
