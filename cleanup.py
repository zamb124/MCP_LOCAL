#!/usr/bin/env python3
"""
Complete cleanup script for Shopping Assistant MCP Server
- Removes MCP server configuration from Claude Desktop
- Deletes virtual environment
- Cleans up created files
- Preserves other MCP servers
- Creates backup before changes
"""

import os
import sys
import json
import platform
import shutil
from pathlib import Path
from datetime import datetime


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


def backup_claude_config(config_path: Path) -> Path:
    """Create a backup of the existing Claude configuration"""
    if not config_path.exists():
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = config_path.parent / f"claude_desktop_config_cleanup_backup_{timestamp}.json"
    
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
                print(f"⚠️  Warning: Could not parse existing config.")
                return {}
    
    except Exception as e:
        print(f"⚠️  Warning: Could not read existing config: {e}")
        return {}


def remove_mcp_server_config():
    """Remove shopping-assistant MCP server from Claude Desktop configuration"""
    config_path = get_claude_config_path()
    
    if not config_path.exists():
        print("✅ No Claude Desktop configuration found - nothing to clean")
        return True
    
    print("⚙️  Removing MCP server from Claude Desktop configuration...")
    
    # Create backup
    backup_path = backup_claude_config(config_path)
    
    # Read existing configuration
    config = read_claude_config_safely(config_path)
    
    if not config:
        print("⚠️  Could not read configuration file")
        return False
    
    # Check if our server exists
    if "mcpServers" not in config:
        print("✅ No MCP servers section found - nothing to clean")
        return True
    
    if "shopping-assistant" not in config["mcpServers"]:
        print("✅ Shopping Assistant MCP server not found in configuration")
        return True
    
    # Count servers before removal
    servers_before = list(config["mcpServers"].keys())
    print(f"📋 Found MCP servers: {', '.join(servers_before)}")
    
    # Remove our server
    del config["mcpServers"]["shopping-assistant"]
    
    servers_after = list(config["mcpServers"].keys())
    
    # If no servers left, remove the entire mcpServers section
    if not config["mcpServers"]:
        del config["mcpServers"]
        print("✅ Removed shopping-assistant server (no other servers remained)")
    else:
        print(f"✅ Removed shopping-assistant server")
        print(f"📋 Remaining MCP servers: {', '.join(servers_after)}")
    
    # Write updated configuration
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Claude Desktop configuration updated")
        if backup_path:
            print(f"🔒 Backup saved: {backup_path.name}")
        
        return True
    except Exception as e:
        print(f"❌ Error writing configuration: {e}")
        
        # Restore backup if write failed
        if backup_path:
            try:
                shutil.copy2(backup_path, config_path)
                print(f"🔄 Configuration restored from backup")
            except Exception as restore_error:
                print(f"❌ Could not restore backup: {restore_error}")
        
        return False


def remove_virtual_environment():
    """Remove the virtual environment directory"""
    venv_path = Path.cwd() / "venv"
    
    if not venv_path.exists():
        print("✅ Virtual environment not found - nothing to clean")
        return True
    
    print("🗑️  Removing virtual environment...")
    
    try:
        shutil.rmtree(venv_path)
        print("✅ Virtual environment removed successfully")
        return True
    except Exception as e:
        print(f"❌ Error removing virtual environment: {e}")
        print("💡 You may need to remove it manually or restart your terminal")
        return False


def clean_generated_files():
    """Clean up generated files (optional)"""
    current_dir = Path.cwd()
    files_to_clean = [
        "__pycache__",
        "*.pyc",
        ".pytest_cache"
    ]
    
    cleaned_files = []
    
    # Remove __pycache__ directories
    for pycache in current_dir.glob("**/__pycache__"):
        try:
            shutil.rmtree(pycache)
            cleaned_files.append(str(pycache.relative_to(current_dir)))
        except Exception:
            pass
    
    # Remove .pyc files
    for pyc_file in current_dir.glob("**/*.pyc"):
        try:
            pyc_file.unlink()
            cleaned_files.append(str(pyc_file.relative_to(current_dir)))
        except Exception:
            pass
    
    if cleaned_files:
        print(f"🧹 Cleaned up {len(cleaned_files)} cache files")
    else:
        print("✅ No cache files to clean")
    
    return True


def list_remaining_files():
    """List files that remain after cleanup"""
    current_dir = Path.cwd()
    important_files = [
        "shopping_mcp_server.py",
        "setup.py", 
        "cleanup.py",
        "test_server.py",
        "requirements.txt",
        "README.md",
        "QUICKSTART.md",
        "setup.sh",
        "setup.bat",
        ".gitignore"
    ]
    
    existing_files = []
    for file_name in important_files:
        file_path = current_dir / file_name
        if file_path.exists():
            existing_files.append(file_name)
    
    if existing_files:
        print(f"\n📁 Remaining project files ({len(existing_files)}):")
        for file_name in existing_files:
            print(f"   • {file_name}")
        
        print(f"\n💡 To completely remove the project:")
        print(f"   cd .. && rm -rf {current_dir.name}")
        print(f"   (or delete the folder manually)")


def print_cleanup_summary():
    """Print cleanup completion message"""
    print("\n" + "="*60)
    print("🧹 CLEANUP COMPLETED SUCCESSFULLY! 🧹")
    print("="*60)
    print()
    print("✅ MCP server configuration removed from Claude Desktop")
    print("✅ Virtual environment deleted")
    print("✅ Cache files cleaned up")
    print("✅ Other MCP servers preserved")
    print()
    print("🔄 To reinstall:")
    print("   • Run: python setup.py")
    print("   • Or: ./setup.sh (macOS/Linux)")
    print("   • Or: setup.bat (Windows)")
    print()
    print("🔒 Configuration backups are preserved in:")
    config_dir = get_claude_config_path().parent
    print(f"   {config_dir}")
    print()
    print("="*60)


def main():
    """Main cleanup function"""
    print("🧹 Shopping Assistant MCP Server - Complete Cleanup")
    print("=" * 52)
    print()
    
    # Confirm cleanup
    print("⚠️  This will remove:")
    print("   • Shopping Assistant MCP server from Claude Desktop")
    print("   • Virtual environment (venv/ folder)")  
    print("   • Python cache files")
    print()
    print("✅ This will preserve:")
    print("   • Other MCP servers in Claude Desktop")
    print("   • Project source files")
    print("   • Configuration backups")
    print()
    
    try:
        confirm = input("Continue with cleanup? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Cleanup cancelled by user")
            return False
    except KeyboardInterrupt:
        print("\n❌ Cleanup cancelled by user")
        return False
    
    print()
    success = True
    
    # Remove MCP server configuration
    if not remove_mcp_server_config():
        success = False
    
    # Remove virtual environment
    if not remove_virtual_environment():
        success = False
    
    # Clean generated files
    if not clean_generated_files():
        success = False
    
    # Show remaining files
    list_remaining_files()
    
    if success:
        print_cleanup_summary()
        print("🔄 Please restart Claude Desktop to apply configuration changes")
    else:
        print("\n⚠️  Cleanup completed with some errors")
        print("Some items may need to be removed manually")
    
    return success


if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Cleanup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during cleanup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 