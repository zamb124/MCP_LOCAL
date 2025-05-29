#!/bin/bash

# Shopping Assistant MCP Server - Automatic Setup for macOS/Linux
echo "🚀 Shopping Assistant MCP Server - Automatic Setup"
echo "================================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8+ from: https://www.python.org/downloads/"
    exit 1
fi

# Make cleanup.py executable if it exists
if [ -f "cleanup.py" ]; then
    chmod +x cleanup.py
fi

# Make setup.py executable
chmod +x setup.py

# Run the Python setup script which does everything
echo "🐍 Running complete setup..."
python3 setup.py

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✅ Setup completed! Run 'python3 cleanup.py' to remove everything later."
else
    echo ""
    echo "❌ Setup failed. Check the error messages above."
fi

exit $exit_code 