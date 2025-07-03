#!/bin/bash

# Set this to your base directory (backend root)
ROOT_DIR="./"

echo "?? Scanning for invalid or non-existent imports in Python files..."

# Grep for all import statements and clean them up
grep -r --include="*.py" -E "^(from|import) " "$ROOT_DIR" | while read -r line; do
    file=$(echo "$line" | cut -d: -f1)
    import_line=$(echo "$line" | cut -d: -f2-)

    # Extract module name
    module=$(echo "$import_line" | sed -E 's/^(from|import) ([^ ]+).*/\2/' | cut -d. -f1)

    # Convert dot notation to path
    path="$ROOT_DIR/$(echo "$module" | tr '.' '/')"

    # Check if file or directory exists
    if [ ! -e "$path.py" ] && [ ! -d "$path" ]; then
        echo "? Broken import in $file: $import_line"
    fi
done

echo "? Scan complete."
