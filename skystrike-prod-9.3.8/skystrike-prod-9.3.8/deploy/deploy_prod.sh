#!/bin/bash
echo "🔁 Building SkyStrike Docker container..."
docker build -t skystrike-app ./skystrike-stackblitz-Test1

echo "🚀 Running SkyStrike app on port 8501..."
docker run -d --name skystrike-prod \
  --env-file ./skystrike-stackblitz-Test1/.env \
  -p 8501:8501 skystrike-app

echo "✅ SkyStrike is now running at http://localhost:8501"
