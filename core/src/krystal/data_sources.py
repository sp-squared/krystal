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
    def __init__(self):
        self.base_url = "https://api.littlesis.org"
        self.session = requests.Session()
        self.rate_limit_delay = 0.5  # Be respectful with API calls
        self.session.headers.update({
            'User-Agent': 'Krystal Power Mapper/1.0',
            'Accept': 'application/json'
        })
        print("✅ LittleSis client initialized (public API - no key required)")
    
    def search_entities(self, query: str, page: int = 1, per_page: int = 20) -> List[Dict]:
        """Search for entities by name in LittleSis using real API"""
        try:
            params = {
                'q': query,
                'page': page,
                'per_page': per_page
            }
            
            print(f"🔍 Searching LittleSis for: '{query}'")
            response = self.session.get(f"{self.base_url}/entities", params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            entities = data.get('data', [])
            
            # Format entities to our expected structure
            formatted_entities = []
            for entity in entities:
                attributes = entity.get('attributes', {})
                formatted_entity = {
                    "id": entity.get('id'),
                    "name": attributes.get('name', 'Unknown'),
                    "type": self._normalize_entity_type(attributes.get('primary_type', 'Entity')),
                    "description": attributes.get('blurb', ''),
                    "influence_score": self._calculate_influence_score(attributes),
                    "website": attributes.get('website', ''),
                    "sector": attributes.get('sector', ''),
                    "founded_year": attributes.get('start_date')[:4] if attributes.get('start_date') else None,
                    "metadata": {
                        "summary": attributes.get('summary', ''),
                        "website": attributes.get('website', ''),
                        "parent_id": attributes.get('parent_id'),
                        "created_at": attributes.get('created_at'),
                        "updated_at": attributes.get('updated_at')
                    }
                }
                formatted_entities.append(formatted_entity)
            
            print(f"✅ Found {len(formatted_entities)} entities from LittleSis")
            time.sleep(self.rate_limit_delay)  # Be nice to the API
            return formatted_entities
            
        except requests.exceptions.RequestException as e:
            print(f"❌ LittleSis API request failed: {e}")
            return self._get_fallback_entities(query, per_page)
        except Exception as e:
            print(f"❌ Error searching LittleSis: {e}")
            return self._get_fallback_entities(query, per_page)
    
    def get_entity_connections(self, entity_id: int, relationship_types: List[str] = None, max_connections: int = 20) -> List[Dict]:
        """Fetch connections for a given entity from LittleSis using real API"""
        try:
            # Ensure entity_id is properly formatted
            if isinstance(entity_id, str):
                if entity_id.isdigit():
                    entity_id = int(entity_id)
                else:
                    print(f"⚠️  Invalid entity ID format: {entity_id}")
                    return []
            
            print(f"🔗 Fetching connections for entity ID: {entity_id}")
            url = f"{self.base_url}/entity/{entity_id}/relationships"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            relationships = data.get('data', [])
            
            # Format relationships to our expected structure
            formatted_connections = []
            for rel in relationships[:max_connections]:
                attributes = rel.get('attributes', {})
                related_entities = rel.get('relationships', {}).get('related_entities', {}).get('data', [])
                
                if len(related_entities) >= 2:
                    entity1 = related_entities[0]
                    entity2 = related_entities[1]
                    
                    # Determine which entity is the target (not the one we queried)
                    if str(entity1.get('id')) == str(entity_id):
                        target_entity = entity2
                    else:
                        target_entity = entity1
                    
                    formatted_conn = {
                        "id": rel.get('id'),
                        "entity1_id": entity1.get('id'),
                        "entity2_id": entity2.get('id'),
                        "entity2_name": target_entity.get('attributes', {}).get('name', 'Unknown'),
                        "relationship_type": attributes.get('description1', 'connected_to'),
                        "description": attributes.get('description', ''),
                        "strength": self._calculate_relationship_strength(attributes),
                        "start_date": attributes.get('start_date'),
                        "end_date": attributes.get('end_date'),
                        "is_current": attributes.get('is_current', True),
                        "metadata": {
                            "amount": attributes.get('amount'),
                            "goods": attributes.get('goods'),
                            "notes": attributes.get('notes')
                        }
                    }
                    
                    # Filter by relationship type if specified
                    if not relationship_types or formatted_conn['relationship_type'] in relationship_types:
                        formatted_connections.append(formatted_conn)
            
            print(f"✅ Found {len(formatted_connections)} connections for entity {entity_id}")
            time.sleep(self.rate_limit_delay)  # Be nice to the API
            return formatted_connections
            
        except requests.exceptions.RequestException as e:
            print(f"❌ LittleSis connections API failed: {e}")
            return self._get_fallback_connections(entity_id, max_connections)
        except Exception as e:
            print(f"❌ Error fetching entity connections: {e}")
            return self._get_fallback_connections(entity_id, max_connections)
    
    def get_entity_details(self, entity_id: int) -> Optional[Dict]:
        """Get detailed information about a specific entity using real API"""
        try:
            if isinstance(entity_id, str) and entity_id.isdigit():
                entity_id = int(entity_id)
                
            print(f"📋 Fetching details for entity ID: {entity_id}")
            response = self.session.get(f"{self.base_url}/entity/{entity_id}", timeout=15)
            response.raise_for_status()
            
            data = response.json()
            entity_data = data.get('data', {})
            attributes = entity_data.get('attributes', {})
            
            detailed_entity = {
                "id": entity_data.get('id'),
                "name": attributes.get('name', 'Unknown'),
                "type": self._normalize_entity_type(attributes.get('primary_type', 'Entity')),
                "description": attributes.get('blurb', ''),
                "website": attributes.get('website', ''),
                "influence_score": self._calculate_influence_score(attributes),
                "sector": attributes.get('sector', ''),
                "founded_year": attributes.get('start_date')[:4] if attributes.get('start_date') else None,
                "address": attributes.get('address', ''),
                "phone": attributes.get('phone', ''),
                "email": attributes.get('email', ''),
                "metadata": {
                    "summary": attributes.get('summary', ''),
                    "website": attributes.get('website', ''),
                    "parent_id": attributes.get('parent_id'),
                    "created_at": attributes.get('created_at'),
                    "updated_at": attributes.get('updated_at'),
                    "aliases": attributes.get('aliases', []),
                    "external_links": attributes.get('external_links', [])
                }
            }
            
            time.sleep(self.rate_limit_delay)  # Be nice to the API
            return detailed_entity
                
        except Exception as e:
            print(f"❌ Error fetching entity details: {e}")
            return self._get_fallback_entity_details(entity_id)
    
    def get_entity_relationships(self, entity_id: int, direction: str = "both") -> List[Dict]:
        """Get relationships with more control over direction"""
        try:
            connections = self.get_entity_connections(entity_id)
            
            if direction == "outgoing":
                return [conn for conn in connections if str(conn.get('entity1_id')) == str(entity_id)]
            elif direction == "incoming":
                return [conn for conn in connections if str(conn.get('entity2_id')) == str(entity_id)]
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
                   if str(conn.get('entity2_id')) == str(entity2_id) or 
                      str(conn.get('entity1_id')) == str(entity2_id)]
        except Exception as e:
            print(f"Error searching relationships: {e}")
            return []
    
    def is_api_available(self) -> bool:
        """LittleSis API is always available (public API)"""
        return True
    
    def _normalize_entity_type(self, entity_type: str) -> str:
        """Normalize entity types to our standard categories"""
        type_mapping = {
            'Person': 'person',
            'Org': 'organization',
            'Business': 'corporation',
            'Government': 'government',
            'PoliticalFundraising': 'organization',
            'Public': 'organization'
        }
        return type_mapping.get(entity_type, entity_type.lower())
    
    def _calculate_influence_score(self, entity_data: Dict) -> float:
        """Calculate influence score based on entity data"""
        base_score = 50.0
        
        # Adjust based on entity type
        entity_type = entity_data.get('primary_type', '').lower()
        type_multipliers = {
            'person': 1.2,
            'org': 1.3,
            'business': 1.4,
            'government': 1.5
        }
        
        multiplier = type_multipliers.get(entity_type, 1.0)
        score = base_score * multiplier
        
        # Cap at 100
        return min(score, 100.0)
    
    def _calculate_relationship_strength(self, relationship_data: Dict) -> float:
        """Calculate relationship strength based on relationship data"""
        base_strength = 0.5
        
        # Adjust based on relationship type and details
        rel_description = relationship_data.get('description1', '').lower()
        
        strength_boosters = {
            'board': 0.3,
            'director': 0.3,
            'executive': 0.35,
            'owner': 0.4,
            'founder': 0.4,
            'donor': 0.25,
            'lobby': 0.3,
            'family': 0.4,
            'member': 0.2
        }
        
        # Find matching booster
        boost = 0.1
        for key, value in strength_boosters.items():
            if key in rel_description:
                boost = value
                break
        
        return min(base_strength + boost, 1.0)
    
    def _get_fallback_entities(self, query: str, count: int) -> List[Dict]:
        """Fallback entities when API fails"""
        print("⚠️  Using fallback entity data (API temporarily unavailable)")
        return [
            {
                "id": i + 1,
                "name": f"{query} Entity {i + 1}",
                "type": ["corporation", "organization", "person", "government"][i % 4],
                "description": f"Fallback entity for {query}",
                "influence_score": 60 + (i * 10) % 40,
                "website": f"https://example.com/entity{i + 1}",
                "sector": ["Technology", "Finance", "Energy", "Healthcare"][i % 4],
                "founded_year": 1980 + (i * 5) % 40,
                "metadata": {}
            }
            for i in range(min(count, 5))
        ]
    
    def _get_fallback_connections(self, entity_id: int, max_connections: int) -> List[Dict]:
        """Fallback connections when API fails"""
        print("⚠️  Using fallback connection data (API temporarily unavailable)")
        return [
            {
                "id": entity_id * 100 + i,
                "entity1_id": entity_id,
                "entity2_id": entity_id + i + 100,
                "entity2_name": f"Connected Entity {i + 1}",
                "relationship_type": ["board_member", "executive", "donor", "partner"][i % 4],
                "description": f"Fallback relationship {i + 1}",
                "strength": 0.5 + (i * 0.1),
                "start_date": None,
                "end_date": None,
                "is_current": True,
                "metadata": {}
            }
            for i in range(min(max_connections, 3))
        ]
    
    def _get_fallback_entity_details(self, entity_id: int) -> Dict:
        """Fallback entity details when API fails"""
        return {
            "id": entity_id,
            "name": f"Entity {entity_id}",
            "type": "organization",
            "description": "Fallback entity details (API temporarily unavailable)",
            "website": f"https://example.com/entity{entity_id}",
            "influence_score": 65,
            "sector": "Various",
            "founded_year": 2000,
            "address": "Unknown",
            "phone": "Unknown",
            "email": "Unknown",
            "metadata": {}
        }


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
        'littlesis': LittleSisClient(),  # No API key needed - public API
        'opensecrets': OpenSecretsClient(opensecrets_api_key)
    }