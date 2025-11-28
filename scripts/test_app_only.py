#!/usr/bin/env python3
"""
Test only the app package
"""

import sys
import os

# Add app to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_path = os.path.join(project_root, 'app', 'src')
sys.path.insert(0, app_path)

print(f"Testing app package from: {app_path}")

try:
    # Test importing the package
    import krystal_app
    print("✅ krystal_app package imported successfully")
    
    # Test importing the specific class
    from krystal_app.main import KrystalApp
    print("✅ KrystalApp class imported successfully")
    
    # Test instantiation
    app = KrystalApp()
    print("✅ KrystalApp instantiated successfully")
    
    # Test basic functionality
    result = app.run()
    print(f"✅ KrystalApp.run() works: {result}")
    
    analysis_result = app.analyze_article("https://example.com/news")
    print(f"✅ KrystalApp.analyze_article() works: {analysis_result}")
    
    print("\n🎉 APP PACKAGE IS WORKING CORRECTLY!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
    # Debug: List files in app directory
    print("\n📁 Files in app directory:")
    app_dir = os.path.join(project_root, 'app', 'src', 'krystal_app')
    if os.path.exists(app_dir):
        for file in os.listdir(app_dir):
            print(f"  - {file}")
    else:
        print(f"  Directory doesn't exist: {app_dir}")