#!/usr/bin/env python3
"""
Final comprehensive test of both packages
"""

import sys
import os

# Get project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
core_path = os.path.join(project_root, 'core', 'src')
app_path = os.path.join(project_root, 'app', 'src')

sys.path.insert(0, core_path)
sys.path.insert(0, app_path)

print("🎯 FINAL KRYSTAL DEVELOPMENT TEST")
print("=" * 50)

# Test 1: Core Package
print("\n1. TESTING CORE PACKAGE...")
try:
    from krystal.power_mapper import PowerMapper
    from krystal.data_sources import LittleSisClient
    
    mapper = PowerMapper()
    ls_client = LittleSisClient()
    
    # Test with sample data
    entities = [{"id": 1, "name": "Test Corporation", "type": "corporation"}]
    relationships = [{"source": 1, "target": 2, "type": "board_member"}]
    
    analysis = mapper.analyze_network(entities, relationships)
    search_results = ls_client.search_entities("test")
    
    print("✅ CORE: All tests passed!")
    print(f"   - PowerMapper: {analysis}")
    print(f"   - LittleSisClient: {len(search_results)} results")
    
except Exception as e:
    print(f"❌ CORE FAILED: {e}")

# Test 2: App Package  
print("\n2. TESTING APP PACKAGE...")
try:
    from krystal_app.main import KrystalApp
    
    app = KrystalApp()
    run_result = app.run()
    analysis_result = app.analyze_article("https://example.com")
    
    print("✅ APP: All tests passed!")
    print(f"   - App run: {run_result}")
    print(f"   - Article analysis: {analysis_result}")
    
except Exception as e:
    print(f"❌ APP FAILED: {e}")

# Test 3: Integration
print("\n3. TESTING INTEGRATION...")
try:
    from krystal.power_mapper import PowerMapper
    from krystal_app.main import KrystalApp
    
    # Create instances of both
    mapper = PowerMapper()
    app = KrystalApp()
    
    print("✅ INTEGRATION: Core and App can be used together!")
    
except Exception as e:
    print(f"❌ INTEGRATION FAILED: {e}")

print("\n" + "=" * 50)
print("📊 TEST SUMMARY:")
print("If you see all green checkmarks above, your development")
print("environment is ready for Krystal development!")
print("\n🚀 NEXT: Start enhancing the PowerMapper with real algorithms!")