#!/usr/bin/env bash
set -euo pipefail

mkdir -p /tmp/maildir/{tmp,new,cur}

pymap --host localhost \
  --port 1143 \
  --no-tls \
  maildir /tmp/maildir