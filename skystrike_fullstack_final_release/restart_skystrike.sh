#!/bin/bash

echo "🔄 Restarting SkyStrike API with updated backend..."

cd ~/skystrike_fullstack_final_release/backend || {
    echo "❌ Failed to enter backend directory"; exit 1;
}

export $(grep -v '^#' ../.env | xargs)

pm2 stop skystrike-api || echo "⚠️ skystrike-api was not running"

pm2 start uvicorn \
  --name skystrike-api \
  --interpreter python3 \
  --output ~/.pm2/logs/skystrike-api-out.log \
  --error ~/.pm2/logs/skystrike-api-error.log \
  -- uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

pm2 status skystrike-api

echo "📋 Tailing logs..."
pm2 logs skystrike-api --lines 30
