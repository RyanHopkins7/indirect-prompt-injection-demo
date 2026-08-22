#!/usr/bin/env bash
set -euo pipefail

# Start the pymap IMAP server and create the demo user.

MAILDIR=/tmp/maildir
mkdir -p "$MAILDIR"/{tmp,new,cur}

pymap --host localhost \
      --port 1143 \
      --no-tls \
      maildir "$MAILDIR" &
PYMAP_PID=$!

sleep 1.0

PASS_FILE="$(mktemp)"
echo "demo" > "$PASS_FILE"
pymap-admin set-user --no-overwrite --password-file "$PASS_FILE" demo
rm -f "$PASS_FILE"

echo "pymap running (pid $PYMAP_PID)"

trap - EXIT
wait "$PYMAP_PID"
