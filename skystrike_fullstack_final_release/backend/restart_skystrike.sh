#!/bin/bash

echo "?? Restarting SkyStrike API with updated backend..."

# Navigate to the backend directory
cd ~/skystrike_fullstack_final_release/backend || {
    echo "? Failed to enter backend directory"; exit 1;
}

# Reload environment variables
export $(grep -v '^#' ../.env | xargs)

# Stop existing PM2 process
pm2 stop skystrike-api || echo "?? skystrike-api was not running"

# Restart the FastAPI app with fixed main path
pm2 start uvicorn \
  --name skystrike-api \
  --interpreter python3 \
  --output ~/.pm2/logs/skystrike-api-out.log \
  --error ~/.pm2/logs/skystrike-api-error.log \
  -- uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Show PM2 status
pm2 status skystrike-api

# Tail logs for real-time monitoring
echo "?? Tailing logs..."
pm2 logs skystrike-api --lines 30
