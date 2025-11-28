"""
Krystal Core - Power Mapping Engine
LGPL v3 - See LICENSE file for complete terms

A comprehensive power structure analysis engine that maps relationships
between corporations, government officials, and influential entities
across news media and public data sources.
"""

__version__ = "0.1.0"
__author__ = "Krystal Team"
__license__ = "LGPL v3"
__description__ = "Power mapping algorithms for transparency and accountability"

# Core algorithm imports
from .power_mapper import PowerMapper
from .data_sources import LittleSisClient, NewsClient, OpenSecretsClient, create_data_sources

# Future module imports (commented out until implemented)
# from .network_analyzer import NetworkAnalyzer
# from .influence_scorer import InfluenceScorer  
# from .entity_resolver import EntityResolver
# from .visualization import PowerGraph

# Define public API
__all__ = [
    # Core analysis
    "PowerMapper",
    
    # Data sources
    "LittleSisClient", 
    "NewsClient",
    "OpenSecretsClient",
    "create_data_sources",
    
    # Future components
    # "NetworkAnalyzer",
    # "InfluenceScorer",
    # "EntityResolver", 
    # "PowerGraph",
]

# Package metadata for easy access
package_info = {
    "name": "krystal-core",
    "version": __version__,
    "author": __author__,
    "license": __license__,
    "description": __description__
}

def get_info():
    """Return package information"""
    return package_info.copy()

def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import requests
        import networkx
        import pandas
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False

# Optional: Add package-level configuration
class Config:
    """Package configuration settings"""
    DEFAULT_CACHE_TIMEOUT = 3600  # 1 hour
    MAX_ENTITIES_PER_QUERY = 1000
    LOG_LEVEL = "INFO"
    
    @classmethod
    def display(cls):
        """Display current configuration"""
        return {k: v for k, v in cls.__dict__.items() if not k.startswith('_')}

# Initialize package state
_initialized = False

def initialize_package():
    """Initialize package components"""
    global _initialized
    if not _initialized:
        # Future: Add any package initialization logic here
        # e.g., setup logging, load configuration, etc.
        _initialized = True
    return _initialized

# Auto-initialize when package is imported
initialize_package()