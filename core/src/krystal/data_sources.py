"""
Data source clients for LittleSis and Google News APIs
LGPL v3
"""

import requests
import os
import time
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import json

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
        
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def search_entities(self, query: str, page: int = 1, per_page: int = 20) -> List[Dict]:
        """Search for entities by name in LittleSis"""
        try:
            params = {
                'q': query,
                'page': page,
                'per_page': per_page
            }
            
            # TODO: Implement actual API call when we have API access
            # response = self.session.get(f"{self.base_url}/entities", params=params)
            # return response.json().get('data', [])
            
            # Mock data for development
            return [
                {
                    "id": 1,
                    "name": f"{query} Corporation",
                    "type": "Corporation",
                    "description": f"Major corporation related to {query}",
                    "influence_score": 85
                },
                {
                    "id": 2, 
                    "name": f"{query} Foundation",
                    "type": "Organization",
                    "description": f"Non-profit organization related to {query}",
                    "influence_score": 60
                },
                {
                    "id": 3,
                    "name": f"{query} Government Official",
                    "type": "Person",
                    "description": f"Government official involved with {query}",
                    "influence_score": 75
                }
            ]
            
        except Exception as e:
            print(f"Error searching LittleSis: {e}")
            return []
    
    def get_entity_connections(self, entity_id: int, relationship_types: List[str] = None) -> List[Dict]:
        """Fetch connections for a given entity from LittleSis"""
        try:
            # TODO: Implement actual API call
            # response = self.session.get(f"{self.base_url}/entity/{entity_id}/relationships")
            # return response.json().get('data', [])
            
            # Mock connections for development
            mock_connections = [
                {
                    "id": 101,
                    "entity1_id": entity_id,
                    "entity2_id": entity_id + 100,
                    "entity2_name": "Connected Corporation",
                    "relationship_type": "board_member",
                    "description": "Serves on board of directors",
                    "strength": 0.8
                },
                {
                    "id": 102,
                    "entity1_id": entity_id, 
                    "entity2_id": entity_id + 200,
                    "entity2_name": "Political Committee",
                    "relationship_type": "political_donations",
                    "description": "Major political donor",
                    "strength": 0.6
                }
            ]
            
            if relationship_types:
                return [conn for conn in mock_connections if conn['relationship_type'] in relationship_types]
            return mock_connections
            
        except Exception as e:
            print(f"Error fetching entity connections: {e}")
            return []
    
    def get_entity_details(self, entity_id: int) -> Optional[Dict]:
        """Get detailed information about a specific entity"""
        try:
            # TODO: Implement actual API call
            # response = self.session.get(f"{self.base_url}/entity/{entity_id}")
            # return response.json().get('data')
            
            # Mock entity details
            return {
                "id": entity_id,
                "name": f"Entity {entity_id}",
                "type": "Corporation",
                "description": "A major corporate entity with significant influence",
                "website": "https://example.com",
                "influence_score": 78,
                "sector": "Technology",
                "founded_year": 1990
            }
            
        except Exception as e:
            print(f"Error fetching entity details: {e}")
            return None


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
def create_data_sources(news_api_key: str = None, littlesis_api_key: str = None, 
                       opensecrets_api_key: str = None) -> Dict:
    """Convenience function to create all data source clients"""
    return {
        'news': NewsClient(news_api_key),
        'littlesis': LittleSisClient(littlesis_api_key),
        'opensecrets': OpenSecretsClient(opensecrets_api_key)
    }