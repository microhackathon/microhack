#!/bin/bash

# Google Drive Setup Script for MicroHack
# This script runs the Python setup script with the correct Python interpreter

echo "🔧 Running Google Drive Setup..."

# Try to find the correct Python interpreter
if command -v python3 &> /dev/null; then
    echo "Using python3..."
    python3 setup_google_drive.py
elif command -v python &> /dev/null; then
    echo "Using python..."
    python setup_google_drive.py
else
    echo "❌ Error: Neither 'python' nor 'python3' found in PATH"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi 