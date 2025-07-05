#!/bin/bash

# Activate virtualenv if needed
source ~/skystrike_fullstack_final_release/venv/bin/activate

# Navigate to backend dir
cd ~/skystrike_fullstack_final_release/backend

# Set a timestamp
echo "🔁 Running Midday Bot Runner at $(date)"

# Call your 0DTE bots (adjust as needed)
curl -X POST http://localhost:8000/api/orders/place \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"bot": "ironcondor", "ticker": "SPX", "contracts": 2, "dte": 0}'

curl -X POST http://localhost:8000/api/orders/place \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"bot": "kingcondor", "ticker": "SPX", "contracts": 2, "dte": 0}'

# Optionally run Copilot instead
# python3 -c 'from copilot_engine import get_top_recommendation; print(get_top_recommendation("SPX"))'