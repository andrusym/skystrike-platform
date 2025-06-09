#!/bin/bash

# SkyStrike v7 Frontend Deployment Script

echo "🚀 Starting SkyStrike Frontend Deployment..."

# Ensure correct directory
cd "$(dirname "$0")"

# Build frontend
echo "🔧 Installing dependencies..."
npm install

echo "📦 Building project..."
npm run build

echo "✅ Frontend built successfully."
echo "🌐 Your app is ready at http://localhost:3000"