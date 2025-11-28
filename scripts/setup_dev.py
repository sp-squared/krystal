#!/usr/bin/env python3
"""
Quick development setup script
"""
import sys
import os
import subprocess

def setup_development():
    """Set up development environment without complex packaging"""
    
    # Install base dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", 
                   "requests", "networkx", "pandas", "numpy",
                   "kivy", "kivymd", "Pillow",
                   "pytest", "jupyter"])
    
    # Add to Python path
    core_path = os.path.join(os.path.dirname(__file__), "core", "src")
    app_path = os.path.join(os.path.dirname(__file__), "app", "src")
    
    if core_path not in sys.path:
        sys.path.insert(0, core_path)
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    
    print("✅ Development environment ready!")
    print(f"Core path: {core_path}")
    print(f"App path: {app_path}")

if __name__ == "__main__":
    setup_development()