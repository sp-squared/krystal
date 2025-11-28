#!/usr/bin/env python3
"""
Setup script for Google News API integration
"""

import os
import sys

def setup_news_api():
    """Guide user through News API setup"""
    print("🔧 Google News API Setup")
    print("=" * 50)
    
    # Check if newsapi is available
    try:
        from newsapi import NewsApiClient
        print("✅ newsapi-python library is installed")
    except ImportError:
        print("❌ newsapi-python not found. Install with: pip install newsapi-python")
        return
    
    # Check for existing API key
    api_key = os.getenv('NEWS_API_KEY')
    if api_key:
        print(f"✅ NEWS_API_KEY found: {api_key[:8]}...{api_key[-4:]}")
        
        # Test the API key
        try:
            newsapi = NewsApiClient(api_key=api_key)
            response = newsapi.get_sources()
            if response['status'] == 'ok':
                print("✅ API key is valid and working!")
            else:
                print(f"❌ API key test failed: {response.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"❌ API key test failed: {e}")
    else:
        print("❌ NEWS_API_KEY environment variable not set")
        print("\n📝 To get a News API key:")
        print("1. Go to https://newsapi.org")
        print("2. Register for a free account")
        print("3. Get your API key from the dashboard")
        print("4. Set environment variable:")
        print("   export NEWS_API_KEY='your_api_key_here'")
        print("\n💡 Or add to your .bashrc or .zshrc file")
    
    print("\n🔍 Testing news client...")
    from krystal.data_sources import NewsClient
    
    news_client = NewsClient()
    if news_client.is_api_available():
        print("✅ News client ready for real news data!")
        
        # Test search
        articles = news_client.search_news("technology", max_results=2)
        print(f"✅ Test search found {len(articles)} articles")
        
        for article in articles:
            print(f"   - {article['title'][:50]}...")
    else:
        print("ℹ️  News client using mock data (set NEWS_API_KEY for real data)")

if __name__ == '__main__':
    setup_news_api()