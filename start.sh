#!/usr/bin/env bash
set -euo pipefail

# Start script used by Render and local runs. Uses Uvicorn worker for ASGI apps.
: "${PORT:=8000}"

exec gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT}
