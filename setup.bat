@echo off
REM Shopping Assistant MCP Server - Automatic Setup for Windows

echo 🚀 Shopping Assistant MCP Server - Automatic Setup
echo =================================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Run the Python setup script which does everything
echo 🐍 Running complete setup...
python setup.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ Setup completed! Run 'python cleanup.py' to remove everything later.
    echo.
    echo 🔄 Please restart Claude Desktop to apply changes
    pause
) else (
    echo.
    echo ❌ Setup failed. Check the error messages above.
    pause
    exit /b 1
) 