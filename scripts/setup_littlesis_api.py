# Initialize the client
ls_client = LittleSisClient()

# Check if API is available
if ls_client.is_api_available():
    print("✅ LittleSis API is configured and ready")
else:
    print("⚠️ Using enhanced mock data for LittleSis")

# Search for entities
entities = ls_client.search_entities("technology", per_page=10)

# Get entity connections
if entities:
    connections = ls_client.get_entity_connections(entities[0]['id'])
    
# Get specific relationship types
board_connections = ls_client.get_entity_connections(
    entity_id=123, 
    relationship_types=['board_member', 'executive']
)