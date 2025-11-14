#!/bin/sh
set -e

# Entrypoint to fix permissions on mounted volumes and ensure DB path exists
# This runs before the main CMD. It is safe to run as root or non-root.

echo "[entrypoint] ensuring directories exist: /app/instance and /app/logs"
mkdir -p /app/instance /app/logs || true

# If stat is available, try to use the owner of /app as the target uid:gid to chown files.
if command -v stat >/dev/null 2>&1; then
  APP_UID=$(stat -c %u /app 2>/dev/null || echo 0)
  APP_GID=$(stat -c %g /app 2>/dev/null || echo 0)
else
  APP_UID=0
  APP_GID=0
fi

# If running as root, attempt to chown the mounted dirs to the app owner (useful if compose runs app as non-root later)
if [ "$(id -u)" = "0" ]; then
  echo "[entrypoint] running as root, attempting chown of /app/instance and /app/logs to ${APP_UID}:${APP_GID}"
  chown -R ${APP_UID}:${APP_GID} /app/instance /app/logs || true
fi

# If DATABASE_URI is sqlite, try to touch the DB file to ensure it can be created
if [ -n "${DATABASE_URI}" ]; then
  case "${DATABASE_URI}" in
    sqlite:/*)
      # Strip leading sqlite:/// or sqlite:////
      DB_PATH=$(echo "${DATABASE_URI}" | sed -E 's#^sqlite:/{3,4}##')
      # If DB_PATH is relative (no leading /), make it relative to /app
      case "${DB_PATH}" in
        /*) DB_FILE="${DB_PATH}" ;;
        *) DB_FILE="/app/${DB_PATH}" ;;
      esac
      echo "[entrypoint] computed DB file path: ${DB_FILE}"
      mkdir -p "$(dirname "${DB_FILE}")" || true
      # Touch and set permissive permissions so the runtime can open/create it
      touch "${DB_FILE}" || true
      chmod 664 "${DB_FILE}" || true
      if [ "$(id -u)" = "0" ]; then
        chown ${APP_UID}:${APP_GID} "${DB_FILE}" || true
      fi
      ;;
  esac
fi

# Ensure permissive mode on directories as a fallback
chmod 775 /app/instance /app/logs || true

# Exec the original CMD
exec "$@"
