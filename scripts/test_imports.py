#!/usr/bin/env python3
"""
Test script to verify imports work
"""

import sys
import os

# Add core and app to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'src'))

try:
    from krystal.power_mapper import PowerMapper
    print("✅ Successfully imported PowerMapper from core")
except ImportError as e:
    print(f"❌ Failed to import from core: {e}")

try:
    from krystal_app.main import KrystalApp
    print("✅ Successfully imported KrystalApp from app")
except ImportError as e:
    print(f"❌ Failed to import from app: {e}")

print("\nPython path:")
for path in sys.path:
    print(f"  {path}")