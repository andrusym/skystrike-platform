#!/usr/bin/env bash
set -e

# Replace dashboard_service → dashboard
sed -i 's|from \.\./services/dashboard_service|from \.\./services/dashboard|' backend/routes/dashboard_routes.py

# (Add more sed lines here for other known mismatches)

echo "Imports patched. Restarting server..."
uvicorn backend.main:app --reload
