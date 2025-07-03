#!/usr/bin/env bash
set -euo pipefail

# 1. Ensure we're in the project root
cd "$(dirname "$0")"

# 2. Create package markers if they don't exist
touch core/__init__.py
touch core/services/__init__.py
touch core/routes/__init__.py

# 3. Rewrite imports in core/routes/*.py
find core/routes -type f -name "*.py" -exec sed -i \
  -e 's|from services\.|from core.services.|g' \
  -e 's|from routes\.|from core.routes.|g' {} +

# 4. (Optional) If you import services or routes elsewhere,
#    run the same replace in all .py files under core/
find core -type f -name "*.py" -exec sed -i \
  -e 's|from services\.|from core.services.|g' \
  -e 's|from routes\.|from core.routes.|g' {} +

echo "? core.services & core.routes imports fixed."
