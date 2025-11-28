"""
Data source clients for LittleSis and Google News APIs
LGPL v3
"""

import requests
import os
import time
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
import re

# Import NewsAPI for real news data
try:
    from newsapi import NewsApiClient
    NEWSAPI_AVAILABLE = True
except ImportError:
    NEWSAPI_AVAILABLE = False
    print("Warning: newsapi-python not available. Using mock news data.")


class LittleSisClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('LITTLESIS_API_KEY')
        self.base_url = "https://api.littlesis.org"
        self.session = requests.Session()
        self.rate_limit_delay = 0.1  # seconds between API calls
        
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
        else:
            print("⚠️  LittleSis API key not found. Using enhanced mock data.")
    
    def is_api_available(self) -> bool:
        """Check if LittleSis API is properly configured"""
        return bool(self.api_key)
    
    def search_entities(self, query: str, page: int = 1, per_page: int = 20) -> List[Dict]:
        """Search for entities by name in LittleSis with real API integration"""
        try:
            if self.is_api_available():
                params = {
                    'q': query,
                    'page': page,
                    'per_page': per_page
                }
                
                response = self.session.get(f"{self.base_url}/entities", params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                entities = data.get('data', [])
                
                # Format entities to our expected structure
                formatted_entities = []
                for entity in entities:
                    formatted_entity = {
                        "id": entity.get('id'),
                        "name": entity.get('name', 'Unknown'),
                        "type": entity.get('type', 'Entity').lower(),
                        "description": entity.get('description', ''),
                        "influence_score": self._calculate_influence_score(entity),
                        "website": entity.get('website', ''),
                        "sector": entity.get('sector', ''),
                        "founded_year": entity.get('founded_year')
                    }
                    formatted_entities.append(formatted_entity)
                
                print(f"✅ Found {len(formatted_entities)} real entities from LittleSis")
                return formatted_entities
            else:
                # Enhanced mock data when API not available
                return self._get_enhanced_mock_entities(query, per_page)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ LittleSis API request failed: {e}")
            return self._get_enhanced_mock_entities(query, per_page)
        except Exception as e:
            print(f"❌ Error searching LittleSis: {e}")
            return self._get_enhanced_mock_entities(query, per_page)
    
    def get_entity_connections(self, entity_id: int, relationship_types: List[str] = None, max_connections: int = 20) -> List[Dict]:
        """Fetch connections for a given entity from LittleSis with real API integration"""
        try:
            # Ensure entity_id is integer for API calls
            if isinstance(entity_id, str) and entity_id.isdigit():
                entity_id = int(entity_id)
            
            if self.is_api_available():
                url = f"{self.base_url}/entity/{entity_id}/relationships"
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                connections = data.get('data', [])
                
                # Format connections to our expected structure
                formatted_connections = []
                for conn in connections[:max_connections]:
                    # Determine which entity is the target (not the one we queried)
                    entity1 = conn.get('entity1', {})
                    entity2 = conn.get('entity2', {})
                    
                    if entity1.get('id') == entity_id:
                        target_entity = entity2
                    else:
                        target_entity = entity1
                    
                    formatted_conn = {
                        "id": conn.get('id'),
                        "entity1_id": entity1.get('id'),
                        "entity2_id": entity2.get('id'),
                        "entity2_name": target_entity.get('name', 'Unknown'),
                        "relationship_type": conn.get('relationship_type', 'connected_to'),
                        "description": conn.get('description', ''),
                        "strength": self._calculate_relationship_strength(conn),
                        "start_date": conn.get('start_date'),
                        "end_date": conn.get('end_date')
                    }
                    
                    # Filter by relationship type if specified
                    if not relationship_types or formatted_conn['relationship_type'] in relationship_types:
                        formatted_connections.append(formatted_conn)
                
                print(f"✅ Found {len(formatted_connections)} real connections for entity {entity_id}")
                return formatted_connections
            else:
                # Enhanced mock data
                return self._get_enhanced_mock_connections(entity_id, max_connections)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ LittleSis connections API failed: {e}")
            return self._get_enhanced_mock_connections(entity_id, max_connections)
        except Exception as e:
            print(f"❌ Error fetching entity connections: {e}")
            return self._get_enhanced_mock_connections(entity_id, max_connections)
    
    def get_entity_details(self, entity_id: int) -> Optional[Dict]:
        """Get detailed information about a specific entity with real API integration"""
        try:
            if isinstance(entity_id, str) and entity_id.isdigit():
                entity_id = int(entity_id)
                
            if self.is_api_available():
                response = self.session.get(f"{self.base_url}/entity/{entity_id}", timeout=10)
                response.raise_for_status()
                
                data = response.json()
                entity = data.get('data', {})
                
                detailed_entity = {
                    "id": entity.get('id'),
                    "name": entity.get('name', 'Unknown'),
                    "type": entity.get('type', 'Entity').lower(),
                    "description": entity.get('description', ''),
                    "website": entity.get('website', ''),
                    "influence_score": self._calculate_influence_score(entity),
                    "sector": entity.get('sector', ''),
                    "founded_year": entity.get('founded_year'),
                    "address": entity.get('address', ''),
                    "phone": entity.get('phone', ''),
                    "email": entity.get('email', ''),
                    "metadata": entity.get('metadata', {})
                }
                
                return detailed_entity
            else:
                return self._get_enhanced_mock_entity_details(entity_id)
                
        except Exception as e:
            print(f"❌ Error fetching entity details: {e}")
            return self._get_enhanced_mock_entity_details(entity_id)
    
    def get_entity_relationships(self, entity_id: int, direction: str = "both") -> List[Dict]:
        """Get relationships with more control over direction (outgoing, incoming, both)"""
        try:
            connections = self.get_entity_connections(entity_id)
            
            if direction == "outgoing":
                return [conn for conn in connections if conn.get('entity1_id') == entity_id]
            elif direction == "incoming":
                return [conn for conn in connections if conn.get('entity2_id') == entity_id]
            else:  # both
                return connections
                
        except Exception as e:
            print(f"Error getting entity relationships: {e}")
            return []
    
    def search_relationships(self, entity1_id: int, entity2_id: int) -> List[Dict]:
        """Find direct relationships between two specific entities"""
        try:
            connections = self.get_entity_connections(entity1_id)
            return [conn for conn in connections 
                   if conn.get('entity2_id') == entity2_id or conn.get('entity1_id') == entity2_id]
        except Exception as e:
            print(f"Error searching relationships: {e}")
            return []
    
    def _calculate_influence_score(self, entity_data: Dict) -> float:
        """Calculate a rough influence score based on entity data"""
        score = 50.0  # Base score
        
        # Adjust based on entity type
        entity_type = entity_data.get('type', '').lower()
        type_multipliers = {
            'corporation': 1.3,
            'government': 1.4,
            'person': 1.2,
            'organization': 1.1
        }
        
        multiplier = type_multipliers.get(entity_type, 1.0)
        score *= multiplier
        
        # Cap at 100
        return min(score, 100.0)
    
    def _calculate_relationship_strength(self, relationship_data: Dict) -> float:
        """Calculate relationship strength based on relationship data"""
        base_strength = 0.5
        
        # Adjust based on relationship type
        rel_type = relationship_data.get('relationship_type', '').lower()
        strength_boosters = {
            'board_member': 0.3,
            'ownership': 0.4,
            'executive': 0.35,
            'donation': 0.25,
            'lobbying': 0.3,
            'family': 0.4
        }
        
        boost = strength_boosters.get(rel_type, 0.1)
        return min(base_strength + boost, 1.0)
    
    def _get_enhanced_mock_entities(self, query: str, count: int) -> List[Dict]:
        """Enhanced mock entities with more realistic data"""
        mock_entities = [
            {
                "id": 1,
                "name": f"{query} Corporation",
                "type": "corporation",
                "description": f"Major multinational corporation focused on {query}",
                "influence_score": 85,
                "website": f"https://{query.lower()}-corp.com",
                "sector": "Technology",
                "founded_year": 1995
            },
            {
                "id": 2, 
                "name": f"{query} Foundation",
                "type": "organization",
                "description": f"Non-profit organization supporting {query} initiatives",
                "influence_score": 65,
                "website": f"https://{query.lower()}-foundation.org",
                "sector": "Philanthropy",
                "founded_year": 2005
            },
            {
                "id": 3,
                "name": f"{query} Government Official",
                "type": "person",
                "description": f"Influential government figure involved with {query} policy",
                "influence_score": 78,
                "website": "",
                "sector": "Government",
                "founded_year": None
            },
            {
                "id": 4,
                "name": f"{query} Industry Association",
                "type": "organization", 
                "description": f"Trade association representing {query} industry interests",
                "influence_score": 72,
                "website": f"https://{query.lower()}-association.org",
                "sector": "Advocacy",
                "founded_year": 1990
            },
            {
                "id": 5,
                "name": f"{query} Research Institute",
                "type": "organization",
                "description": f"Think tank conducting research on {query} topics",
                "influence_score": 68,
                "website": f"https://{query.lower()}-research.edu",
                "sector": "Education",
                "founded_year": 1985
            }
        ]
        
        return mock_entities[:count]
    
    def _get_enhanced_mock_connections(self, entity_id: int, max_connections: int) -> List[Dict]:
        """Enhanced mock connections with more realistic relationship data"""
        # Different connection sets based on entity type patterns
        if entity_id % 3 == 0:  # Person type
            connections = [
                {
                    "id": entity_id * 100 + 1,
                    "entity1_id": entity_id,
                    "entity2_id": entity_id + 100,
                    "entity2_name": "Corporate Board",
                    "relationship_type": "board_member",
                    "description": "Serves as board member",
                    "strength": 0.8,
                    "start_date": "2020-01-15"
                },
                {
                    "id": entity_id * 100 + 2,
                    "entity1_id": entity_id, 
                    "entity2_id": entity_id + 200,
                    "entity2_name": "Political Campaign",
                    "relationship_type": "donation",
                    "description": "Major campaign donor",
                    "strength": 0.6,
                    "start_date": "2022-03-10"
                }
            ]
        elif entity_id % 3 == 1:  # Corporation type
            connections = [
                {
                    "id": entity_id * 100 + 1,
                    "entity1_id": entity_id,
                    "entity2_id": entity_id + 300,
                    "entity2_name": "Industry Association",
                    "relationship_type": "membership",
                    "description": "Executive committee member",
                    "strength": 0.7,
                    "start_date": "2018-05-20"
                },
                {
                    "id": entity_id * 100 + 2,
                    "entity1_id": entity_id,
                    "entity2_id": entity_id + 400,
                    "entity2_name": "Government Agency",
                    "relationship_type": "lobbying",
                    "description": "Registered lobbying activities",
                    "strength": 0.9,
                    "start_date": "2021-11-05"
                }
            ]
        else:  # Organization type
            connections = [
                {
                    "id": entity_id * 100 + 1,
                    "entity1_id": entity_id,
                    "entity2_id": entity_id + 500,
                    "entity2_name": "Research Partner",
                    "relationship_type": "partnership",
                    "description": "Research and development partnership",
                    "strength": 0.6,
                    "start_date": "2019-07-12"
                },
                {
                    "id": entity_id * 100 + 2,
                    "entity1_id": entity_id,
                    "entity2_id": entity_id + 600,
                    "entity2_name": "Government Department",
                    "relationship_type": "advisory",
                    "description": "Provides expert advisory services",
                    "strength": 0.75,
                    "start_date": "2020-09-18"
                }
            ]
        
        return connections[:max_connections]
    
    def _get_enhanced_mock_entity_details(self, entity_id: int) -> Dict:
        """Enhanced mock entity details"""
        entity_types = ['corporation', 'organization', 'person', 'government']
        entity_type = entity_types[entity_id % len(entity_types)]
        
        details = {
            "id": entity_id,
            "name": f"Entity {entity_id}",
            "type": entity_type,
            "description": f"A detailed description of {entity_type} entity {entity_id}",
            "website": f"https://entity{entity_id}.com",
            "influence_score": 60 + (entity_id * 5) % 40,
            "sector": ["Technology", "Finance", "Healthcare", "Energy"][entity_id % 4],
            "founded_year": 1980 + (entity_id * 3) % 40,
            "address": f"{entity_id} Main Street, City, State",
            "phone": f"+1-555-{entity_id:04d}",
            "email": f"info@entity{entity_id}.com",
            "metadata": {
                "employee_count": 1000 + (entity_id * 100) % 9000,
                "revenue": f"${(entity_id * 1000000) % 1000000000:,}",
                "last_updated": datetime.now().isoformat()
            }
        }
        
        return details
    
class NewsClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        self.newsapi = None
        self.use_real_api = False
        
        # Initialize NewsAPI client if key is available
        if self.api_key and NEWSAPI_AVAILABLE:
            try:
                self.newsapi = NewsApiClient(api_key=self.api_key)
                self.use_real_api = True
                print("✅ NewsAPI client initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize NewsAPI: {e}")
                self.use_real_api = False
        else:
            print("ℹ️  Using mock news data (no API key or newsapi not available)")
            if not self.api_key:
                print("   Set NEWS_API_KEY environment variable for real news data")
    
    def search_news(self, query: str, max_results: int = 10, language: str = "en", 
                   from_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for news articles using Google News API
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            language: Language code (en, es, fr, etc.)
            from_date: Date in YYYY-MM-DD format (default: 7 days ago)
            
        Returns:
            List of news articles with metadata
        """
        if not from_date:
            # Default to last 7 days
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        if self.use_real_api and self.newsapi:
            try:
                print(f"🔍 Searching real news for: {query}")
                
                # Make API call to NewsAPI
                response = self.newsapi.get_everything(
                    q=query,
                    from_param=from_date,
                    language=language,
                    sort_by='relevancy',
                    page_size=min(max_results, 100)  # API limit is 100
                )
                
                if response['status'] == 'ok':
                    articles = response['articles']
                    print(f"✅ Found {len(articles)} real news articles")
                    
                    # Format articles to match our expected structure
                    formatted_articles = []
                    for article in articles[:max_results]:
                        formatted_article = {
                            "title": article.get('title', 'No title'),
                            "url": article.get('url', ''),
                            "source": article.get('source', {}).get('name', 'Unknown'),
                            "published_at": article.get('publishedAt', ''),
                            "content": article.get('content', '') or article.get('description', ''),
                            "description": article.get('description', ''),
                            "image_url": article.get('urlToImage', ''),
                            "author": article.get('author', ''),
                            "entities": []  # Will be extracted later
                        }
                        formatted_articles.append(formatted_article)
                    
                    return formatted_articles
                else:
                    print(f"❌ NewsAPI error: {response.get('message', 'Unknown error')}")
                    return self._get_mock_news(query, max_results)
                    
            except Exception as e:
                print(f"❌ NewsAPI search error: {e}")
                return self._get_mock_news(query, max_results)
        else:
            # Fall back to mock data
            return self._get_mock_news(query, max_results)
    
    def get_top_headlines(self, category: Optional[str] = None, country: str = "us", 
                         max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Get top headlines using NewsAPI
        """
        if self.use_real_api and self.newsapi:
            try:
                print(f"📰 Fetching top headlines (category: {category})")
                
                response = self.newsapi.get_top_headlines(
                    category=category,
                    country=country,
                    page_size=min(max_results, 100)
                )
                
                if response['status'] == 'ok':
                    articles = response['articles']
                    print(f"✅ Found {len(articles)} top headlines")
                    
                    formatted_articles = []
                    for article in articles[:max_results]:
                        formatted_article = {
                            "title": article.get('title', 'No title'),
                            "url": article.get('url', ''),
                            "source": article.get('source', {}).get('name', 'Unknown'),
                            "published_at": article.get('publishedAt', ''),
                            "content": article.get('content', '') or article.get('description', ''),
                            "description": article.get('description', ''),
                            "image_url": article.get('urlToImage', ''),
                            "author": article.get('author', ''),
                            "category": category,
                            "entities": []
                        }
                        formatted_articles.append(formatted_article)
                    
                    return formatted_articles
                else:
                    print(f"❌ NewsAPI headlines error: {response.get('message', 'Unknown error')}")
                    return self._get_mock_headlines(category, max_results)
                    
            except Exception as e:
                print(f"❌ NewsAPI headlines error: {e}")
                return self._get_mock_headlines(category, max_results)
        else:
            return self._get_mock_headlines(category, max_results)
    
    def _get_mock_news(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Fallback mock news data"""
        return [
            {
                "title": f"Sample: Latest developments in {query}",
                "url": "https://example.com/news/1",
                "source": "Example News",
                "published_at": datetime.now().isoformat(),
                "content": f"This is a sample article about {query}. In a real implementation, this would contain actual news content from the Google News API.",
                "description": f"Sample description about {query}",
                "image_url": "",
                "author": "Sample Author",
                "entities": [f"{query} Corporation", "Industry Expert"]
            },
            {
                "title": f"Analysis: Impact of {query} on markets",
                "url": "https://example.com/news/2", 
                "source": "Business Daily",
                "published_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                "content": f"Market analysis focusing on {query} and its broader implications.",
                "description": f"Analysis of {query} market impact",
                "image_url": "",
                "author": "Business Analyst",
                "entities": [f"{query} Markets", "Financial Sector"]
            }
        ][:max_results]
    
    def _get_mock_headlines(self, category: Optional[str], max_results: int) -> List[Dict[str, Any]]:
        """Fallback mock headlines"""
        base_headlines = [
            {
                "title": "Breaking: Major Political Developments",
                "url": "https://example.com/headline/1",
                "source": "National News",
                "published_at": datetime.now().isoformat(),
                "content": "Important political news affecting current events.",
                "description": "Major political developments unfolding",
                "category": "politics"
            },
            {
                "title": "Technology Sector Reaches New Milestone", 
                "url": "https://example.com/headline/2",
                "source": "Tech Review",
                "published_at": (datetime.now() - timedelta(hours=1)).isoformat(),
                "content": "The technology industry achieves significant growth metrics.",
                "description": "Technology sector milestone reached",
                "category": "technology"
            }
        ]
        
        if category:
            return [h for h in base_headlines if h.get('category') == category][:max_results]
        return base_headlines[:max_results]
    
    def extract_entities(self, article_text: str) -> List[Dict]:
        """Extract named entities from article text"""
        # TODO: Implement proper NLP entity extraction
        # For now, use simple keyword matching
        
        entities = []
        text_lower = article_text.lower()
        
        # Simple entity type detection
        entity_keywords = {
            'corporation': ['corp', 'inc', 'llc', 'company', 'ltd', 'group'],
            'person': ['ceo', 'president', 'director', 'chairman', 'executive', 'senator'],
            'government': ['senate', 'congress', 'white house', 'administration', 'agency', 'federal'],
            'organization': ['foundation', 'institute', 'association', 'committee']
        }
        
        # Mock entity extraction based on common terms
        if any(word in text_lower for word in ['apple', 'google', 'microsoft', 'amazon', 'meta']):
            entities.append({
                "name": "Technology Company",
                "type": "corporation",
                "confidence": 0.85
            })
        
        if any(word in text_lower for word in ['senate', 'congress', 'white house', 'administration']):
            entities.append({
                "name": "Government Entity", 
                "type": "government",
                "confidence": 0.75
            })
            
        if any(word in text_lower for word in ['ceo', 'president', 'director']):
            entities.append({
                "name": "Corporate Executive",
                "type": "person", 
                "confidence": 0.70
            })
            
        return entities
    
    def get_news_categories(self) -> List[str]:
        """Get available news categories for top headlines"""
        return [
            "business", "entertainment", "general", "health", 
            "science", "sports", "technology", "politics"
        ]
    
    def is_api_available(self) -> bool:
        """Check if real NewsAPI is available"""
        return self.use_real_api

class OpenSecretsClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENSECRETS_API_KEY')
        self.base_url = "https://www.opensecrets.org/api"
    
    def get_candidate_funding(self, candidate_id: str, cycle: str = "2024") -> Dict:
        """Get funding information for a political candidate"""
        # TODO: Implement OpenSecrets API integration
        return {
            "candidate_id": candidate_id,
            "cycle": cycle,
            "total_raised": 2500000,
            "top_contributors": [
                {"name": "Tech Industry", "amount": 500000},
                {"name": "Finance Industry", "amount": 350000}
            ]
        }
    
    def get_organization_summary(self, org_id: str) -> Dict:
        """Get summary information for an organization"""
        # TODO: Implement OpenSecrets API integration  
        return {
            "org_id": org_id,
            "name": "Example Organization",
            "total_lobbying": 1500000,
            "total_contributions": 800000
        }
    
# Utility function to initialize all data sources
def create_data_sources(news_api_key: str = None, opensecrets_api_key: str = None) -> Dict:
    """Convenience function to create all data source clients"""
    return {
        'news': NewsClient(news_api_key),
        'littlesis': LittleSisClient(),  # No API key needed
        'opensecrets': OpenSecretsClient(opensecrets_api_key)
    }