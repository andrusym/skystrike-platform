#!/bin/bash
# Build and deploy SkyStrike frontend

echo "Cleaning previous builds..."
rm -rf dist

echo "Installing dependencies..."
npm install

echo "Running build..."
npm run build

echo "Copying to /usr/share/nginx/html/..."
sudo cp -r dist/* /usr/share/nginx/html/
sudo systemctl restart nginx

echo "✅ Deployment complete"
