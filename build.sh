#!/bin/bash
# Quick build script for News Feed Bundles

set -e

echo "🚀 News Feed Bundle Builder"
echo "============================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import yaml" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Run the build
echo ""
python3 scripts/build_bundles.py "$@"

echo ""
echo "✅ Done! Check the dist/ directory for your bundles."
