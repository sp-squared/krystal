#!/usr/bin/env python3
"""
LittleSis Client Usage Examples
Demonstrates all the functionality of the enhanced LittleSis client
"""

import os
import sys
from datetime import datetime

# Add the path to your data_sources module
sys.path.append('/path/to/your/krystal/core/src')

from krystal.data_sources import LittleSisClient

def demonstrate_littlesis_functionality():
    """Demonstrate all LittleSis client features"""
    
    print("🔍 LittleSis Client Demo")
    print("=" * 50)
    
    # Initialize the client
    ls_client = LittleSisClient()
    
    # Check API availability
    api_status = "🟢 Available" if ls_client.is_api_available() else "🟡 Mock Data"
    print(f"API Status: {api_status}")
    print()
    
    # Example 1: Search for entities
    print("1. 🔎 Entity Search")
    print("-" * 30)
    
    search_queries = ["technology", "finance", "energy", "pharmaceutical"]
    
    for query in search_queries:
        print(f"\nSearching for: '{query}'")
        entities = ls_client.search_entities(query, per_page=3)
        
        print(f"Found {len(entities)} entities:")
        for i, entity in enumerate(entities, 1):
            print(f"  {i}. {entity['name']} ({entity['type']})")
            print(f"     Influence: {entity['influence_score']} | Sector: {entity.get('sector', 'N/A')}")
    
    print("\n" + "="*50)
    
    # Example 2: Get entity details
    print("\n2. 📋 Entity Details")
    print("-" * 30)
    
    # Get details for the first entity from search
    if entities:
        sample_entity = entities[0]
        entity_id = sample_entity['id']
        
        print(f"Getting details for: {sample_entity['name']} (ID: {entity_id})")
        
        details = ls_client.get_entity_details(entity_id)
        if details:
            print(f"Name: {details['name']}")
            print(f"Type: {details['type']}")
            print(f"Description: {details['description']}")
            print(f"Influence Score: {details['influence_score']}")
            print(f"Sector: {details.get('sector', 'N/A')}")
            print(f"Founded: {details.get('founded_year', 'N/A')}")
            print(f"Website: {details.get('website', 'N/A')}")
            
            if details.get('metadata'):
                print("Additional Metadata:")
                for key, value in details['metadata'].items():
                    print(f"  {key}: {value}")
    
    print("\n" + "="*50)
    
    # Example 3: Get entity connections
    print("\n3. 🔗 Entity Connections")
    print("-" * 30)
    
    if entities:
        # Test with different entity types
        test_entities = entities[:3]  # Test first 3 entities
        
        for entity in test_entities:
            print(f"\nConnections for: {entity['name']} (ID: {entity['id']})")
            
            connections = ls_client.get_entity_connections(
                entity['id'], 
                max_connections=5
            )
            
            if connections:
                print(f"Found {len(connections)} connections:")
                for i, conn in enumerate(connections, 1):
                    print(f"  {i}. {conn['entity2_name']}")
                    print(f"     Relationship: {conn['relationship_type']}")
                    print(f"     Strength: {conn['strength']:.2f}")
                    print(f"     Description: {conn['description']}")
            else:
                print("  No connections found")
    
    print("\n" + "="*50)
    
    # Example 4: Directional relationships
    print("\n4. 🧭 Directional Relationships")
    print("-" * 30)
    
    if entities:
        entity_id = entities[0]['id']
        
        print(f"Relationship directions for: {entities[0]['name']}")
        
        # Outgoing relationships (entity -> others)
        outgoing = ls_client.get_entity_relationships(entity_id, direction="outgoing")
        print(f"Outgoing relationships: {len(outgoing)}")
        
        # Incoming relationships (others -> entity)
        incoming = ls_client.get_entity_relationships(entity_id, direction="incoming")
        print(f"Incoming relationships: {len(incoming)}")
        
        # Both directions
        both = ls_client.get_entity_relationships(entity_id, direction="both")
        print(f"Total relationships: {len(both)}")
    
    print("\n" + "="*50)
    
    # Example 5: Search specific relationships
    print("\n5. 🎯 Specific Relationship Search")
    print("-" * 30)
    
    if len(entities) >= 2:
        entity1_id = entities[0]['id']
        entity2_id = entities[1]['id']
        
        print(f"Searching relationships between:")
        print(f"  {entities[0]['name']} (ID: {entity1_id})")
        print(f"  {entities[1]['name']} (ID: {entity2_id})")
        
        specific_relationships = ls_client.search_relationships(entity1_id, entity2_id)
        
        if specific_relationships:
            print("Found direct relationships:")
            for rel in specific_relationships:
                print(f"  Type: {rel['relationship_type']}")
                print(f"  Strength: {rel['strength']:.2f}")
                print(f"  Description: {rel['description']}")
        else:
            print("No direct relationships found")
    
    print("\n" + "="*50)
    
    # Example 6: Filter by relationship types
    print("\n6. 🎚️ Filtered Connections")
    print("-" * 30)
    
    if entities:
        entity_id = entities[0]['id']
        
        # Define relationship types to filter for
        relationship_types = ['board_member', 'executive', 'ownership']
        
        print(f"Filtering connections for {entities[0]['name']} by types: {relationship_types}")
        
        filtered_connections = ls_client.get_entity_connections(
            entity_id, 
            relationship_types=relationship_types,
            max_connections=10
        )
        
        if filtered_connections:
            print(f"Found {len(filtered_connections)} filtered connections:")
            for conn in filtered_connections:
                print(f"  - {conn['entity2_name']}: {conn['relationship_type']} (strength: {conn['strength']:.2f})")
        else:
            print("No connections match the filter criteria")
    
    print("\n" + "="*50)
    
    # Example 7: Batch processing multiple entities
    print("\n7. 📊 Batch Entity Analysis")
    print("-" * 30)
    
    analysis_queries = ["tech", "bank", "oil"]
    all_entities = []
    
    for query in analysis_queries:
        print(f"\nProcessing query: '{query}'")
        batch_entities = ls_client.search_entities(query, per_page=2)
        all_entities.extend(batch_entities)
        
        # Get connections for each entity in batch
        for entity in batch_entities:
            connections = ls_client.get_entity_connections(entity['id'], max_connections=2)
            print(f"  {entity['name']}: {len(connections)} connections")
    
    # Summary statistics
    print(f"\n📈 Batch Analysis Summary:")
    print(f"Total entities processed: {len(all_entities)}")
    
    # Count by type
    type_count = {}
    for entity in all_entities:
        entity_type = entity['type']
        type_count[entity_type] = type_count.get(entity_type, 0) + 1
    
    print("Entities by type:")
    for entity_type, count in type_count.items():
        print(f"  {entity_type}: {count}")
    
    # Average influence score
    if all_entities:
        avg_influence = sum(e['influence_score'] for e in all_entities) / len(all_entities)
        print(f"Average influence score: {avg_influence:.1f}")

def demonstrate_error_handling():
    """Demonstrate error handling and edge cases"""
    
    print("\n" + "="*50)
    print("8. 🛡️ Error Handling Examples")
    print("-" * 30)
    
    ls_client = LittleSisClient()
    
    # Test with invalid entity ID
    print("Testing with invalid entity ID...")
    invalid_connections = ls_client.get_entity_connections(-999)
    print(f"Result: {len(invalid_connections)} connections (should handle gracefully)")
    
    # Test with string ID that needs conversion
    print("\nTesting with string ID conversion...")
    string_id_connections = ls_client.get_entity_connections("123")
    print(f"Result: {len(string_id_connections)} connections")
    
    # Test empty search
    print("\nTesting empty search query...")
    empty_results = ls_client.search_entities("")
    print(f"Result: {len(empty_results)} entities")
    
    # Test with very specific relationship types that might not exist
    print("\nTesting with non-existent relationship types...")
    if empty_results:
        rare_connections = ls_client.get_entity_connections(
            empty_results[0]['id'],
            relationship_types=['space_alien', 'time_traveler']  # These shouldn't exist
        )
        print(f"Result: {len(rare_connections)} connections found")

if __name__ == "__main__":
    print("🚀 Starting LittleSis Client Demonstration")
    print("=" * 60)
    
    try:
        # Main demonstration
        demonstrate_littlesis_functionality()
        
        # Error handling demonstration
        demonstrate_error_handling()
        
        print("\n" + "=" * 60)
        print("✅ LittleSis Client Demo Completed Successfully!")
        print("\nSummary of features demonstrated:")
        print("  ✓ Entity search with pagination")
        print("  ✓ Detailed entity information")
        print("  ✓ Entity connection networks")
        print("  ✓ Directional relationship analysis")
        print("  ✓ Specific relationship searches")
        print("  ✓ Relationship type filtering")
        print("  ✓ Batch processing capabilities")
        print("  ✓ Robust error handling")
        print("  ✓ Graceful fallback to mock data")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()