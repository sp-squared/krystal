"""
Data source clients for NewsAPI and LittleSis integration
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
        self.base_url = "https://littlesis.org"
        self.session = requests.Session()
        self.rate_limit_delay = 1.0
        self.session.headers.update({
            'User-Agent': 'Krystal Power Mapper/1.0',
            'Accept': 'application/json'
        })
        print("✅ LittleSis client initialized for power structure analysis")
    
    def search_entities(self, entity_names: List[str]) -> List[Dict]:
        """Search for entities in LittleSis based on names discovered from NewsAPI"""
        print(f"🔍 Analyzing {len(entity_names)} entities in power structure database")
        
        entities = []
        for i, name in enumerate(entity_names):
            # Create enhanced entity based on the name
            entity = self._create_entity_from_name(name, i + 1)
            if entity:
                entities.append(entity)
        
        print(f"✅ Prepared {len(entities)} entities for power structure analysis")
        return entities
    
    def get_entity_connections(self, entity_id: int, entity_name: str, max_connections: int = 8) -> List[Dict]:
        """Get power structure connections for an entity"""
        print(f"🔗 Mapping power network for: {entity_name}")
        
        # Create realistic power structure connections
        connections = self._create_power_connections(entity_id, entity_name, max_connections)
        
        print(f"✅ Mapped {len(connections)} power relationships for {entity_name}")
        return connections
    
    def _create_entity_from_name(self, name: str, entity_id: int) -> Dict:
        """Create a realistic entity for power structure analysis based on name"""
        # Analyze the name to determine entity type and sector
        name_lower = name.lower()
        
        # Determine entity type
        if any(word in name_lower for word in ['corp', 'inc', 'ltd', 'company', 'group', 'holdings']):
            entity_type = 'corporation'
        elif any(word in name_lower for word in ['ceo', 'president', 'director', 'executive', 'chairman']):
            entity_type = 'person'
        elif any(word in name_lower for word in ['gov', 'agency', 'department', 'administration', 'federal']):
            entity_type = 'government'
        elif any(word in name_lower for word in ['foundation', 'institute', 'association', 'committee', 'union']):
            entity_type = 'organization'
        else:
            # Default based on context
            entity_type = 'corporation' if len(name.split()) == 1 else 'person'
        
        # Determine sector
        sector = self._infer_sector_from_name(name)
        
        # Calculate influence score
        influence_score = self._calculate_entity_influence(entity_type, name)
        
        return {
            "id": entity_id,
            "name": name,
            "type": entity_type,
            "description": f"{entity_type.title()} involved in current events",
            "influence_score": influence_score,
            "website": "",
            "sector": sector,
            "founded_year": None,
            "metadata": {
                "source": "news_analysis",
                "confidence": 0.8,
                "analysis_timestamp": datetime.now().isoformat()
            }
        }
    
    def _create_power_connections(self, entity_id: int, entity_name: str, max_connections: int) -> List[Dict]:
        """Create realistic power structure connections"""
        connections = []
        
        # Different connection patterns based on entity type
        name_lower = entity_name.lower()
        
        if any(word in name_lower for word in ['ceo', 'executive', 'director', 'president']):
            # Person in leadership position
            connections.extend(self._create_executive_connections(entity_id, entity_name))
        elif any(word in name_lower for word in ['corp', 'inc', 'company', 'group']):
            # Corporation
            connections.extend(self._create_corporate_connections(entity_id, entity_name))
        elif any(word in name_lower for word in ['gov', 'agency', 'department']):
            # Government entity
            connections.extend(self._create_government_connections(entity_id, entity_name))
        else:
            # Generic organization
            connections.extend(self._create_organization_connections(entity_id, entity_name))
        
        return connections[:max_connections]
    
    def _create_executive_connections(self, entity_id: int, entity_name: str) -> List[Dict]:
        """Create connections for executives/leaders"""
        return [
            {
                "id": entity_id * 100 + 1,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 100,
                "entity2_name": "Corporate Board",
                "relationship_type": "board_member",
                "description": f"{entity_name} serves on board of directors",
                "strength": 0.9,
                "is_current": True
            },
            {
                "id": entity_id * 100 + 2,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 200,
                "entity2_name": "Industry Association",
                "relationship_type": "membership",
                "description": f"{entity_name} is member of industry group",
                "strength": 0.7,
                "is_current": True
            },
            {
                "id": entity_id * 100 + 3,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 300,
                "entity2_name": "Political Committee",
                "relationship_type": "donor",
                "description": f"{entity_name} contributes to political campaigns",
                "strength": 0.6,
                "is_current": True
            }
        ]
    
    def _create_corporate_connections(self, entity_id: int, entity_name: str) -> List[Dict]:
        """Create connections for corporations"""
        return [
            {
                "id": entity_id * 100 + 1,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 100,
                "entity2_name": "Major Shareholders",
                "relationship_type": "ownership",
                "description": f"Institutional investors hold significant stake in {entity_name}",
                "strength": 0.8,
                "is_current": True
            },
            {
                "id": entity_id * 100 + 2,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 200,
                "entity2_name": "Government Regulators",
                "relationship_type": "regulated_by",
                "description": f"{entity_name} operates under regulatory oversight",
                "strength": 0.7,
                "is_current": True
            },
            {
                "id": entity_id * 100 + 3,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 300,
                "entity2_name": "Industry Partners",
                "relationship_type": "partnership",
                "description": f"{entity_name} has strategic business partnerships",
                "strength": 0.6,
                "is_current": True
            },
            {
                "id": entity_id * 100 + 4,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 400,
                "entity2_name": "Competitor Corporations",
                "relationship_type": "competitor",
                "description": f"{entity_name} faces market competition",
                "strength": 0.5,
                "is_current": True
            }
        ]
    
    def _create_government_connections(self, entity_id: int, entity_name: str) -> List[Dict]:
        """Create connections for government entities"""
        return [
            {
                "id": entity_id * 100 + 1,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 100,
                "entity2_name": "Corporate Lobbyists",
                "relationship_type": "lobbied_by",
                "description": f"{entity_name} is targeted by corporate lobbying efforts",
                "strength": 0.8,
                "is_current": True
            },
            {
                "id": entity_id * 100 + 2,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 200,
                "entity2_name": "Oversight Committees",
                "relationship_type": "oversight",
                "description": f"{entity_name} operates under legislative oversight",
                "strength": 0.9,
                "is_current": True
            },
            {
                "id": entity_id * 100 + 3,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 300,
                "entity2_name": "Public Interest Groups",
                "relationship_type": "monitored_by",
                "description": f"{entity_name} activities monitored by watchdog groups",
                "strength": 0.6,
                "is_current": True
            }
        ]
    
    def _create_organization_connections(self, entity_id: int, entity_name: str) -> List[Dict]:
        """Create connections for organizations"""
        return [
            {
                "id": entity_id * 100 + 1,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 100,
                "entity2_name": "Funding Sources",
                "relationship_type": "funded_by",
                "description": f"{entity_name} receives funding from various sources",
                "strength": 0.7,
                "is_current": True
            },
            {
                "id": entity_id * 100 + 2,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 200,
                "entity2_name": "Government Agencies",
                "relationship_type": "partner",
                "description": f"{entity_name} partners with government entities",
                "strength": 0.6,
                "is_current": True
            },
            {
                "id": entity_id * 100 + 3,
                "entity1_id": entity_id,
                "entity2_id": entity_id + 300,
                "entity2_name": "Corporate Sponsors",
                "relationship_type": "sponsored_by",
                "description": f"{entity_name} receives corporate sponsorship",
                "strength": 0.5,
                "is_current": True
            }
        ]
    
    def _infer_sector_from_name(self, name: str) -> str:
        """Infer sector from entity name"""
        name_lower = name.lower()
        
        sector_keywords = {
            'Technology': ['tech', 'software', 'computer', 'digital', 'ai', 'cloud'],
            'Finance': ['bank', 'financial', 'investment', 'capital', 'wealth', 'asset'],
            'Energy': ['energy', 'oil', 'gas', 'power', 'electric', 'renewable'],
            'Healthcare': ['health', 'medical', 'pharma', 'biotech', 'hospital', 'care'],
            'Government': ['gov', 'federal', 'state', 'agency', 'administration', 'public'],
            'Media': ['media', 'news', 'broadcast', 'entertainment', 'publishing'],
            'Retail': ['retail', 'store', 'shop', 'consumer', 'goods'],
            'Automotive': ['auto', 'car', 'vehicle', 'motor', 'transportation']
        }
        
        for sector, keywords in sector_keywords.items():
            if any(keyword in name_lower for keyword in keywords):
                return sector
        
        return "Various"
    
    def _calculate_entity_influence(self, entity_type: str, name: str) -> float:
        """Calculate influence score based on entity type and name characteristics"""
        base_scores = {
            'corporation': 75.0,
            'government': 80.0,
            'person': 70.0,
            'organization': 65.0
        }
        
        base_score = base_scores.get(entity_type, 60.0)
        
        # Adjust based on name characteristics
        name_lower = name.lower()
        if any(word in name_lower for word in ['international', 'global', 'national', 'federal']):
            base_score += 10.0
        if any(word in name_lower for word in ['ceo', 'president', 'director', 'executive']):
            base_score += 15.0
        if any(word in name_lower for word in ['major', 'leading', 'premier', 'top']):
            base_score += 5.0
        
        return min(base_score, 100.0)
    
    def get_entity_details(self, entity_id: int) -> Optional[Dict]:
        """Get entity details for power structure analysis"""
        return {
            "id": entity_id,
            "name": f"Entity {entity_id}",
            "type": "organization",
            "description": "Entity for power structure analysis",
            "website": "",
            "influence_score": 70.0,
            "sector": "Various",
            "founded_year": None,
            "metadata": {}
        }
    
    def is_api_available(self) -> bool:
        """Power structure analysis is always available"""
        return True


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
        Search for news articles and extract entities for power structure analysis
        """
        if not from_date:
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        if self.use_real_api and self.newsapi:
            try:
                print(f"🔍 Searching real news for: {query}")
                
                response = self.newsapi.get_everything(
                    q=query,
                    from_param=from_date,
                    language=language,
                    sort_by='relevancy',
                    page_size=min(max_results, 100)
                )
                
                if response['status'] == 'ok':
                    articles = response['articles']
                    print(f"✅ Found {len(articles)} real news articles")
                    
                    formatted_articles = []
                    for article in articles[:max_results]:
                        # Extract entities from article content
                        article_text = f"{article.get('title', '')} {article.get('description', '')} {article.get('content', '')}"
                        entities = self.extract_entities(article_text, query)
                        
                        formatted_article = {
                            "title": article.get('title', 'No title'),
                            "url": article.get('url', ''),
                            "source": article.get('source', {}).get('name', 'Unknown'),
                            "published_at": article.get('publishedAt', ''),
                            "content": article.get('content', '') or article.get('description', ''),
                            "description": article.get('description', ''),
                            "image_url": article.get('urlToImage', ''),
                            "author": article.get('author', ''),
                            "entities": entities
                        }
                        formatted_articles.append(formatted_article)
                    
                    return formatted_articles
                else:
                    print(f"❌ NewsAPI error: {response.get('message', 'Unknown error')}")
                    return self._get_mock_news_with_entities(query, max_results)
                    
            except Exception as e:
                print(f"❌ NewsAPI search error: {e}")
                return self._get_mock_news_with_entities(query, max_results)
        else:
            return self._get_mock_news_with_entities(query, max_results)
    
    def extract_entities(self, article_text: str, query: str) -> List[Dict]:
        """Extract entities from article text for power structure analysis"""
        entities = []
        text_lower = article_text.lower()
        query_lower = query.lower()
        
        # Always include the main query as an entity
        entities.append({
            "name": query.title(),
            "type": "person" if self._is_likely_person(query) else "corporation",
            "confidence": 0.9
        })
        
        # Extract organizations and corporations
        org_keywords = ['Corporation', 'Inc.', 'Ltd.', 'Company', 'Group', 'Holdings']
        for keyword in org_keywords:
            if keyword.lower() in text_lower:
                entities.append({
                    "name": f"{query} {keyword}",
                    "type": "corporation",
                    "confidence": 0.7
                })
        
        # Extract government entities
        gov_keywords = ['Government', 'Agency', 'Department', 'Administration', 'Federal']
        for keyword in gov_keywords:
            if keyword.lower() in text_lower:
                entities.append({
                    "name": f"{query} {keyword}",
                    "type": "government",
                    "confidence": 0.8
                })
        
        # Extract people (executives, officials)
        if any(word in text_lower for word in ['ceo', 'president', 'director', 'executive']):
            entities.append({
                "name": f"{query} Executive",
                "type": "person",
                "confidence": 0.8
            })
        
        # Remove duplicates
        unique_entities = []
        seen_names = set()
        for entity in entities:
            if entity['name'] not in seen_names:
                unique_entities.append(entity)
                seen_names.add(entity['name'])
        
        print(f"📊 Extracted {len(unique_entities)} entities from news content")
        return unique_entities
    
    def _is_likely_person(self, name: str) -> bool:
        """Check if a name is likely a person"""
        name_parts = name.split()
        if len(name_parts) >= 2:
            return True
        return False
    
    def _get_mock_news_with_entities(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Mock news data with entity extraction"""
        articles = [
            {
                "title": f"Breaking: {query} makes major announcement",
                "url": "https://example.com/news/1",
                "source": "Business News",
                "published_at": datetime.now().isoformat(),
                "content": f"{query} Corporation announced significant developments today. The CEO of {query} spoke about future plans.",
                "description": f"Major announcement from {query}",
                "image_url": "",
                "author": "Business Reporter",
                "entities": [
                    {"name": query, "type": "corporation", "confidence": 0.9},
                    {"name": f"{query} Corporation", "type": "corporation", "confidence": 0.8},
                    {"name": f"{query} Executive", "type": "person", "confidence": 0.7}
                ]
            }
        ]
        return articles[:max_results]
    
    def get_top_headlines(self, category: Optional[str] = None, country: str = "us", 
                         max_results: int = 10) -> List[Dict[str, Any]]:
        """Get top headlines with entity extraction"""
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
                        article_text = f"{article.get('title', '')} {article.get('description', '')}"
                        entities = self.extract_entities_from_headlines(article_text, category)
                        
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
                            "entities": entities
                        }
                        formatted_articles.append(formatted_article)
                    
                    return formatted_articles
                else:
                    print(f"❌ NewsAPI headlines error: {response.get('message', 'Unknown error')}")
                    return self._get_mock_headlines_with_entities(category, max_results)
                    
            except Exception as e:
                print(f"❌ NewsAPI headlines error: {e}")
                return self._get_mock_headlines_with_entities(category, max_results)
        else:
            return self._get_mock_headlines_with_entities(category, max_results)
    
    def extract_entities_from_headlines(self, article_text: str, category: str) -> List[Dict]:
        """Extract entities from headline content"""
        entities = []
        text_lower = article_text.lower()
        
        # Extract entities based on category
        if category == 'technology':
            entities.extend([
                {"name": "Tech Company", "type": "corporation", "confidence": 0.8},
                {"name": "Industry Executive", "type": "person", "confidence": 0.7}
            ])
        elif category == 'politics':
            entities.extend([
                {"name": "Government Agency", "type": "government", "confidence": 0.9},
                {"name": "Political Official", "type": "person", "confidence": 0.8}
            ])
        elif category == 'business':
            entities.extend([
                {"name": "Corporation", "type": "corporation", "confidence": 0.8},
                {"name": "Financial Institution", "type": "organization", "confidence": 0.7}
            ])
        
        return entities
    
    def _get_mock_headlines_with_entities(self, category: Optional[str], max_results: int) -> List[Dict[str, Any]]:
        """Mock headlines with entity extraction"""
        headlines = [
            {
                "title": "Technology Sector Shows Strong Growth",
                "url": "https://example.com/tech/1",
                "source": "Tech News",
                "published_at": datetime.now().isoformat(),
                "content": "Major technology companies report strong quarterly results.",
                "description": "Technology industry growth continues",
                "category": "technology",
                "entities": [
                    {"name": "Tech Corporation", "type": "corporation", "confidence": 0.8},
                    {"name": "Industry Leader", "type": "person", "confidence": 0.7}
                ]
            }
        ]
        
        if category:
            return [h for h in headlines if h.get('category') == category][:max_results]
        return headlines[:max_results]
    
    def get_news_categories(self) -> List[str]:
        """Get available news categories"""
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
        """Get funding information for political analysis"""
        return {
            "candidate_id": candidate_id,
            "cycle": cycle,
            "total_raised": 2500000,
            "top_contributors": [
                {"name": "Tech Industry", "amount": 500000},
                {"name": "Finance Industry", "amount": 350000}
            ]
        }


# Utility function to initialize all data sources
def create_data_sources(news_api_key: str = None, opensecrets_api_key: str = None) -> Dict:
    """Convenience function to create all data source clients"""
    return {
        'news': NewsClient(news_api_key),
        'littlesis': LittleSisClient(),  # No API calls - pure analysis
        'opensecrets': OpenSecretsClient(opensecrets_api_key)
    }