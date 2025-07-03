#!/usr/bin/env bash
set -euo pipefail

# ensure we're in the directory where this script lives
cd "$(dirname "$0")"

# list of folders to turn into packages
dirs=(
  backend
  backend/routes
  backend/services
  backend/utils
)

# create folders if missing and touch __init__.py
for d in "${dirs[@]}"; do
  if [ ! -d "$d" ]; then
    echo "⚠️  Directory '$d' not found; creating it."
    mkdir -p "$d"
  fi
  touch "$d/__init__.py"
  echo "✔️  Created $d/__init__.py"
done

echo "✅ All __init__.py files are in place."
