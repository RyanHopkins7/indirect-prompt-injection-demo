#!/usr/bin/env bash
set -euo pipefail

# Kill existing pymap and SMTP servers, start pymap and SMTP servers, and create the demo user.

RUNNING_PYMAP_PID="$(lsof -t -i:1143 || true)"
RUNNING_SMTP_PID="$(lsof -t -i:1025 || true)"

if [ -n "$RUNNING_PYMAP_PID" ]; then
    kill $RUNNING_PYMAP_PID
    echo "Killed pymap server on PID $RUNNING_PYMAP_PID"
fi

if [ -n "$RUNNING_SMTP_PID" ]; then
    kill $RUNNING_SMTP_PID
    echo "Killed smtp server on PID $RUNNING_PYMAP_PID"
fi

WD=$(pwd)
source "$WD/venv/bin/activate"

MAILDIR=/tmp/maildir
mkdir -p "$MAILDIR"/{tmp,new,cur}

pymap --host localhost \
      --port 1143 \
      --no-tls \
      maildir "$MAILDIR" &
PYMAP_PID=$!

python smtp_receive.py &
SMTP_SERVER_PID=$!

sleep 1.0

PASS_FILE="$(mktemp)"
echo "demo" > "$PASS_FILE"
pymap-admin set-user --no-overwrite --password-file "$PASS_FILE" demo
rm -f "$PASS_FILE"

echo "pymap running (pid $PYMAP_PID)"
echo "smtp server running (pid $SMTP_SERVER_PID)"
