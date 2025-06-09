#!/bin/bash

echo "🚀 Deploying SkyStrike v8.8 (Clean Install Build)"

# Stop and remove existing container if any
docker stop skystrike-prod 2>/dev/null || true
docker rm skystrike-prod 2>/dev/null || true

# Remove any old image
docker rmi skystrike-app 2>/dev/null || true

# Clean up and extract the validated clean build
rm -rf skystrike-v8.8
unzip -o skystrike-v8.8-ui-clean-install.zip -d skystrike-v8.8

# Navigate into project directory
cd skystrike-v8.8 || { echo "❌ Could not enter project directory"; exit 1; }

# Build Docker image
docker build -t skystrike-app .

# Run the container with .env file
docker run -d --name skystrike-prod -p 8501:8501 --env-file .env skystrike-app

echo "✅ SkyStrike v8.8 is running at http://localhost:8501"
