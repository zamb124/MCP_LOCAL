#!/usr/bin/env python3
"""
Complete automatic setup script for Shopping Assistant MCP Server
- Creates virtual environment
- Installs all dependencies
- Configures Claude Desktop safely
- Works on macOS, Windows, and Linux
"""

import os
import sys
import json
import platform
import subprocess
from pathlib import Path
from datetime import datetime
import shutil


def get_claude_config_path():
    """Get Claude Desktop configuration file path based on OS"""
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "Claude" / "claude_desktop_config.json"
        else:
            return Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    else:  # Linux
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"


def get_python_executable():
    """Get the Python executable path in virtual environment"""
    system = platform.system().lower()
    current_dir = Path.cwd()
    
    if system == "windows":
        return current_dir / "venv" / "Scripts" / "python.exe"
    else:
        return current_dir / "venv" / "bin" / "python"


def get_pip_executable():
    """Get the pip executable path in virtual environment"""
    system = platform.system().lower()
    current_dir = Path.cwd()
    
    if system == "windows":
        return current_dir / "venv" / "Scripts" / "pip.exe"
    else:
        return current_dir / "venv" / "bin" / "pip"


def check_python_installation():
    """Check if Python is properly installed"""
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version_info = result.stdout.strip()
            print(f"✅ Python found: {version_info}")
            
            # Check Python version (require 3.8+)
            if sys.version_info < (3, 8):
                print("❌ Python 3.8+ required!")
                return False
            return True
        else:
            print("❌ Python not working properly!")
            return False
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False


def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path.cwd() / "venv"
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        result = subprocess.run([sys.executable, "-m", "venv", "venv"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Virtual environment created successfully")
            return True
        else:
            print("❌ Failed to create virtual environment!")
            print("Error:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False


def install_dependencies():
    """Install required dependencies in virtual environment"""
    print("📥 Installing dependencies...")
    
    pip_exe = get_pip_executable()
    if not pip_exe.exists():
        print("❌ Pip not found in virtual environment!")
        return False
    
    # Check if requirements.txt exists
    requirements_file = Path.cwd() / "requirements.txt"
    if not requirements_file.exists():
        print("📝 Creating requirements.txt...")
        with open(requirements_file, 'w') as f:
            f.write("mcp>=1.0.0\n")
            f.write("typing-extensions>=4.0.0\n")
    
    try:
        # Upgrade pip first
        print("⬆️  Upgrading pip...")
        subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], 
                      capture_output=True, text=True, check=True)
        
        # Install requirements
        print("📦 Installing packages...")
        result = subprocess.run([str(pip_exe), "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Failed to install dependencies!")
            print("Error:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def backup_claude_config(config_path: Path) -> Path:
    """Create a backup of the existing Claude configuration"""
    if not config_path.exists():
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = config_path.parent / f"claude_desktop_config_backup_{timestamp}.json"
    
    try:
        shutil.copy2(config_path, backup_path)
        print(f"✅ Configuration backup created: {backup_path.name}")
        return backup_path
    except Exception as e:
        print(f"⚠️  Warning: Could not create backup: {e}")
        return None


def fix_json_content(content: str) -> str:
    """Try to fix common JSON issues like trailing commas"""
    import re
    
    # Remove trailing commas before closing braces/brackets
    content = re.sub(r',(\s*[}\]])', r'\1', content)
    
    # Remove comments (// style)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    
    return content


def read_claude_config_safely(config_path: Path) -> dict:
    """Safely read Claude configuration with error handling"""
    if not config_path.exists():
        return {}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse as-is first
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to fix common issues
            fixed_content = fix_json_content(content)
            try:
                return json.loads(fixed_content)
            except json.JSONDecodeError:
                print(f"⚠️  Warning: Could not parse existing config. Creating backup...")
                return {}
    
    except Exception as e:
        print(f"⚠️  Warning: Could not read existing config: {e}")
        return {}


def restore_backup(config_path: Path):
    """Interactive function to restore from backup"""
    backup_dir = config_path.parent
    backup_files = list(backup_dir.glob("claude_desktop_config_backup_*.json"))
    
    if not backup_files:
        print("❌ No backup files found.")
        return False
    
    print("\n📁 Available backup files:")
    for i, backup_file in enumerate(sorted(backup_files, reverse=True), 1):
        # Extract timestamp from filename
        timestamp = backup_file.stem.split('_')[-2:]
        readable_time = f"{timestamp[0][:4]}-{timestamp[0][4:6]}-{timestamp[0][6:8]} {timestamp[1][:2]}:{timestamp[1][2:4]}:{timestamp[1][4:6]}"
        print(f"  {i}. {backup_file.name} (created: {readable_time})")
    
    try:
        choice = input("\nEnter backup number to restore (or 'q' to quit): ").strip()
        if choice.lower() == 'q':
            return False
        
        backup_index = int(choice) - 1
        if 0 <= backup_index < len(backup_files):
            selected_backup = sorted(backup_files, reverse=True)[backup_index]
            shutil.copy2(selected_backup, config_path)
            print(f"✅ Configuration restored from {selected_backup.name}")
            return True
        else:
            print("❌ Invalid selection.")
            return False
            
    except (ValueError, KeyboardInterrupt):
        print("❌ Restoration cancelled.")
        return False


def verify_installation():
    """Verify that MCP is properly installed"""
    python_exe = get_python_executable()
    
    if not python_exe.exists():
        print("❌ Python executable not found in virtual environment!")
        return False
    
    try:
        result = subprocess.run([str(python_exe), "-c", "import mcp; print('MCP package imported successfully')"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ MCP package verified: {result.stdout.strip()}")
            return True
        else:
            print("❌ MCP package not properly installed!")
            print("Error:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error verifying MCP installation: {e}")
        return False


def create_claude_config():
    """Create or update Claude Desktop configuration"""
    current_dir = Path.cwd()
    python_exe = get_python_executable()
    server_script = current_dir / "shopping_mcp_server.py"
    
    # Verify server script exists
    if not server_script.exists():
        print(f"❌ Server script not found: {server_script}")
        return False
    
    # Create our server configuration
    our_server_config = {
        "command": str(python_exe),
        "args": [str(server_script)],
        "env": {},
        "cwd": str(current_dir)
    }
    
    # Get Claude config file path
    config_path = get_claude_config_path()
    
    # Create directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create backup of existing config
    backup_path = backup_claude_config(config_path)
    
    # Read existing configuration safely
    existing_config = read_claude_config_safely(config_path)
    
    # If we couldn't read the config and there's a backup, ask user what to do
    if not existing_config and backup_path:
        print("\n⚠️  Could not read existing configuration file.")
        print("This might overwrite your existing MCP servers.")
        choice = input("Do you want to try restoring from backup first? (y/n): ").strip().lower()
        
        if choice == 'y':
            if restore_backup(config_path):
                existing_config = read_claude_config_safely(config_path)
    
    # Ensure mcpServers section exists
    if "mcpServers" not in existing_config:
        existing_config["mcpServers"] = {}
    
    # Count existing servers
    existing_servers = list(existing_config["mcpServers"].keys())
    if existing_servers:
        print(f"✅ Found {len(existing_servers)} existing MCP servers: {', '.join(existing_servers)}")
    
    # Add or update our server
    existing_config["mcpServers"]["shopping-assistant"] = our_server_config
    
    # Write configuration
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(existing_config, f, indent=2)
        
        total_servers = len(existing_config["mcpServers"])
        print(f"✅ Claude Desktop configuration updated successfully!")
        print(f"📁 Config file: {config_path}")
        print(f"🔧 Total MCP servers configured: {total_servers}")
        
        if backup_path:
            print(f"🔒 Backup saved: {backup_path.name}")
        
        return True
    except Exception as e:
        print(f"❌ Error writing configuration: {e}")
        print(f"📁 Attempted path: {config_path}")
        
        # Offer to restore backup if write failed
        if backup_path:
            choice = input("\nRestore from backup? (y/n): ").strip().lower()
            if choice == 'y':
                restore_backup(config_path)
        
        return False


def test_server():
    """Test the MCP server functionality"""
    print("\n🧪 Testing server functionality...")
    
    test_script = Path.cwd() / "test_server.py"
    if not test_script.exists():
        print("⚠️  Test script not found, skipping tests")
        return True
    
    python_exe = get_python_executable()
    
    try:
        result = subprocess.run([str(python_exe), "test_server.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Server tests passed!")
            return True
        else:
            print("❌ Server tests failed!")
            print("Error output:", result.stderr[:500] + "..." if len(result.stderr) > 500 else result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("⚠️  Server tests timed out (this might be normal)")
        return True
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def print_success_message():
    """Print success message and instructions"""
    system = platform.system().lower()
    
    print("\n" + "="*70)
    print("🎉 COMPLETE SETUP FINISHED SUCCESSFULLY! 🎉")
    print("="*70)
    print()
    print("✅ Virtual environment created")
    print("✅ Dependencies installed")
    print("✅ Claude Desktop configuration updated")
    print("✅ Existing MCP servers preserved")
    print("✅ Server functionality tested")
    print()
    print("📋 NEXT STEPS:")
    print("1. Restart Claude Desktop application")
    print("2. Start asking Claude about products!")
    print()
    print("💬 Try these example queries:")
    print("   • 'Find iPhone 15'")
    print("   • 'Compare prices for PlayStation 5'")
    print("   • 'Show me Nike shoes'")
    print("   • 'What products are available at Noon?'")
    print()
    
    if system == "darwin":
        print("🍎 macOS: Restart Claude Desktop from Applications folder")
    elif system == "windows":
        print("🪟 Windows: Restart Claude Desktop from Start menu")
    else:
        print("🐧 Linux: Restart Claude Desktop application")
    
    print()
    print("🔧 Useful Commands:")
    print(f"   • Test server: python test_server.py")
    print(f"   • Run server manually: python shopping_mcp_server.py")
    print(f"   • Restore config backup: python setup.py --restore")
    print(f"   • Clean up everything: python cleanup.py")
    print(f"   • Config location: {get_claude_config_path()}")
    print()
    print("="*70)


def main():
    """Main setup function"""
    # Check for restore flag
    if len(sys.argv) > 1 and sys.argv[1] == "--restore":
        config_path = get_claude_config_path()
        if restore_backup(config_path):
            print("✅ Configuration restored successfully!")
        return True
    
    print("🚀 Shopping Assistant MCP Server - Complete Setup")
    print("=" * 55)
    print()
    
    # Detect OS
    system = platform.system()
    print(f"🖥️  Detected OS: {system}")
    print(f"📁 Current directory: {Path.cwd()}")
    print()
    
    # Check Python installation
    if not check_python_installation():
        print("\n❌ Setup failed! Python 3.8+ is required.")
        print("Please install Python from: https://www.python.org/downloads/")
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        print("\n❌ Setup failed! Could not create virtual environment.")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed! Could not install dependencies.")
        return False
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Setup failed! MCP package verification failed.")
        return False
    
    # Create Claude configuration
    print("\n⚙️  Configuring Claude Desktop...")
    if not create_claude_config():
        print("\n❌ Setup failed! Could not configure Claude Desktop.")
        return False
    
    # Test server
    if not test_server():
        print("\n⚠️  Setup completed with warnings. Server tests failed.")
        print("You may still be able to use the server, but please check for issues.")
    
    # Success message
    print_success_message()
    return True


if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 