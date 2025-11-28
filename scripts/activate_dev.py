#!/usr/bin/env python3
"""
Development environment activator
Run this script to set up Python paths for development
"""

import sys
import os

def activate_development():
    """Activate development environment by setting Python paths"""
    
    # Get project root (where this script is located)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Paths to add
    core_path = os.path.join(project_root, 'core', 'src')
    app_path = os.path.join(project_root, 'app', 'src')
    
    # Add to Python path if not already there
    if core_path not in sys.path:
        sys.path.insert(0, core_path)
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    
    print("🚀 Krystal Development Environment Activated!")
    print(f"📁 Project root: {project_root}")
    print(f"🔧 Core path: {core_path}")
    print(f"📱 App path: {app_path}")
    print("✅ Python paths configured for development")
    
    return project_root

if __name__ == "__main__":
    activate_development()
    
    # Test imports
    try:
        from krystal.power_mapper import PowerMapper
        from krystal_app.main import KrystalApp
        print("✅ All imports successful!")
    except ImportError as e:
        print(f"❌ Import error: {e}")