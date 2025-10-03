#!/bin/bash

echo "🎨 Starting Vibe Marketing Frontend..."

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "⚠️  .env.local file not found! Copying from .env.local.example..."
    cp .env.local.example .env.local
    echo "⚠️  Please edit frontend/.env.local with your API keys before running again!"
    exit 1
fi

# Start the dev server
echo "✅ Starting Next.js dev server on http://localhost:4000"
NEXT_DISABLE_FILE_SYSTEM_CACHE=1 npm run dev -- -p 4000
