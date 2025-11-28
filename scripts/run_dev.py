#!/usr/bin/env python3
"""
Development runner - use this for all development
"""

# First activate the development environment
from activate_dev import activate_development
project_root = activate_development()

# Now you can import and use your packages
from krystal.power_mapper import PowerMapper
from krystal_app.main import KrystalApp

def main():
    """Main development test function"""
    print("\n🧪 Testing Krystal Development Environment...")
    
    # Test core functionality
    mapper = PowerMapper()
    test_data = {
        "entities": [{"id": 1, "name": "Test"}],
        "relationships": []
    }
    result = mapper.analyze_network(test_data["entities"], test_data["relationships"])
    print(f"✅ Core analysis: {result}")
    
    # Test app functionality
    app = KrystalApp()
    print("✅ App initialized successfully")
    
    print("\n🎉 Development environment is working correctly!")
    print("You can now start developing Krystal!")

if __name__ == "__main__":
    main()