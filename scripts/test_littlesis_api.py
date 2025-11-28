#!/usr/bin/env python3
"""
LittleSis Real API Usage Examples
Demonstrates the actual LittleSis API integration
"""

import sys
import time
from krystal.data_sources import LittleSisClient

def demonstrate_real_littlesis_api():
    """Demonstrate real LittleSis API functionality"""
    
    print("🔍 LittleSis Real API Demo")
    print("=" * 50)
    print("Using public LittleSis API (no authentication required)")
    print("Rate limiting: ~2 requests per second")
    print()
    
    # Initialize the client
    ls_client = LittleSisClient()
    
    # Example 1: Search for real entities
    print("1. 🔎 Real Entity Search")
    print("-" * 30)
    
    search_queries = ["Google", "Microsoft", "Apple", "Amazon"]
    
    for query in search_queries:
        print(f"\nSearching for real entities: '{query}'")
        entities = ls_client.search_entities(query, per_page=3)
        
        print(f"Found {len(entities)} entities:")
        for i, entity in enumerate(entities, 1):
            print(f"  {i}. {entity['name']}")
            print(f"     Type: {entity['type']} | Influence: {entity['influence_score']}")
            print(f"     Description: {entity['description'][:100]}...")
        
        time.sleep(1)  # Respect rate limits
    
    print("\n" + "="*50)
    
    # Example 2: Get real entity connections
    print("\n2. 🔗 Real Entity Connections")
    print("-" * 30)
    
    if entities:
        # Use the first real entity found
        sample_entity = entities[0]
        entity_id = sample_entity['id']
        
        print(f"Getting real connections for: {sample_entity['name']} (ID: {entity_id})")
        
        connections = ls_client.get_entity_connections(entity_id, max_connections=5)
        
        if connections:
            print(f"Found {len(connections)} real connections:")
            for i, conn in enumerate(connections, 1):
                print(f"  {i}. {conn['entity2_name']}")
                print(f"     Relationship: {conn['relationship_type']}")
                print(f"     Strength: {conn['strength']:.2f}")
                if conn['description']:
                    print(f"     Details: {conn['description'][:80]}...")
        else:
            print("  No connections found in API")
        
        time.sleep(1)  # Respect rate limits
    
    print("\n" + "="*50)
    
    # Example 3: Get detailed entity information
    print("\n3. 📋 Real Entity Details")
    print("-" * 30)
    
    if entities:
        entity_id = entities[0]['id']
        print(f"Getting detailed info for entity ID: {entity_id}")
        
        details = ls_client.get_entity_details(entity_id)
        if details:
            print(f"Name: {details['name']}")
            print(f"Type: {details['type']}")
            print(f"Description: {details['description']}")
            print(f"Sector: {details.get('sector', 'N/A')}")
            print(f"Website: {details.get('website', 'N/A')}")
            print(f"Founded: {details.get('founded_year', 'N/A')}")
            
            if details.get('metadata', {}).get('summary'):
                print(f"Summary: {details['metadata']['summary'][:200]}...")
        
        time.sleep(1)  # Respect rate limits
    
    print("\n" + "="*50)
    
    # Example 4: Batch analysis with real data
    print("\n4. 📊 Real Data Network Analysis")
    print("-" * 30)
    
    analysis_targets = ["technology", "banking", "energy"]
    network_stats = []
    
    for target in analysis_targets:
        print(f"\nAnalyzing network for: {target}")
        target_entities = ls_client.search_entities(target, per_page=2)
        
        if target_entities:
            total_connections = 0
            for entity in target_entities:
                connections = ls_client.get_entity_connections(entity['id'], max_connections=2)
                total_connections += len(connections)
                print(f"  {entity['name']}: {len(connections)} connections")
            
            network_stats.append({
                'sector': target,
                'entities': len(target_entities),
                'connections': total_connections
            })
        
        time.sleep(2)  # Respect rate limits between sectors
    
    # Display network analysis summary
    print(f"\n📈 Real Network Analysis Summary:")
    for stats in network_stats:
        avg_connections = stats['connections'] / stats['entities'] if stats['entities'] > 0 else 0
        print(f"  {stats['sector']}: {stats['entities']} entities, {stats['connections']} connections "
              f"(avg: {avg_connections:.1f} per entity)")

def test_api_limits():
    """Test API rate limiting and error handling"""
    print("\n" + "="*50)
    print("5. 🧪 API Limit Testing")
    print("-" * 30)
    
    ls_client = LittleSisClient()
    
    # Test with various entity IDs
    test_ids = [1, 2, 3, 999999]  # Last one should be invalid
    
    for entity_id in test_ids:
        print(f"\nTesting entity ID: {entity_id}")
        try:
            details = ls_client.get_entity_details(entity_id)
            if details:
                print(f"  ✅ Success: {details['name']}")
            else:
                print("  ❌ No data returned")
        except Exception as e:
            print(f"  ⚠️  Error: {e}")
        
        time.sleep(1)  # Always respect rate limits

if __name__ == "__main__":
    print("🚀 Starting LittleSis Real API Demonstration")
    print("=" * 60)
    print("Note: Using public LittleSis API - be respectful of rate limits!")
    print()
    
    try:
        # Main real API demonstration
        demonstrate_real_littlesis_api()
        
        # API limit testing
        test_api_limits()
        
        print("\n" + "=" * 60)
        print("✅ LittleSis Real API Demo Completed Successfully!")
        print("\nReal API Features Demonstrated:")
        print("  ✓ Real entity search with actual LittleSis data")
        print("  ✓ Real relationship networks and connections") 
        print("  ✓ Detailed entity information from LittleSis database")
        print("  ✓ Sector-based network analysis")
        print("  ✓ Proper rate limiting and error handling")
        print("  ✓ No authentication required - completely open API")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()