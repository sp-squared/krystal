"""
Power mapping algorithms and network analysis
LGPL v3

Core engine for analyzing power structures, influence networks,
and relationship patterns across corporations, government, and media.
"""

import networkx as nx
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
import json


class PowerMapper:
    """
    Main power mapping engine that analyzes relationships and influence networks
    between entities across different sectors.
    """
    
    def __init__(self):
        self.graph = nx.Graph()
        self.entities = {}
        self.relationships = []
        self.analysis_cache = {}
        
        # Configuration
        self.min_relationship_strength = 0.1
        self.max_network_depth = 3
        
    def analyze_network(self, entities: List[Dict], relationships: List[Dict]) -> Dict[str, Any]:
        """
        Analyze power structures from entities and relationships
        
        Args:
            entities: List of entity dictionaries with id, name, type, etc.
            relationships: List of relationship dictionaries with source, target, type, etc.
            
        Returns:
            Dictionary containing comprehensive network analysis
        """
        # Build the network graph
        self._build_network(entities, relationships)
        
        # Perform various analyses
        centrality_measures = self._calculate_centrality()
        community_structure = self._detect_communities()
        influence_scores = self._calculate_influence_scores()
        structural_analysis = self._analyze_structure()
        
        return {
            "summary": {
                "entity_count": len(entities),
                "relationship_count": len(relationships),
                "network_density": nx.density(self.graph),
                "connected_components": nx.number_connected_components(self.graph)
            },
            "centrality": centrality_measures,
            "communities": community_structure,
            "influence_rankings": influence_scores,
            "structural_analysis": structural_analysis,
            "key_findings": self._generate_key_findings(centrality_measures, community_structure)
        }
    


    def _build_network(self, entities: List[Dict], relationships: List[Dict]) -> None:
        """Build network graph from entities and relationships - FIXED VERSION"""
        self.graph.clear()
        
        # Generate IDs for entities that don't have them
        processed_entities = []
        for i, entity in enumerate(entities):
            if 'id' not in entity:
                # Create a unique ID based on name or index
                entity_id = entity.get('name', f"entity_{i}")
                # Clean the ID to be alphanumeric
                entity_id = ''.join(c for c in str(entity_id) if c.isalnum() or c in ('_', '-')).lower()
                entity['id'] = entity_id
            processed_entities.append(entity)
        
        self.entities = {entity['id']: entity for entity in processed_entities}
        self.relationships = relationships
        
        # Add entities as nodes
        for entity_id, entity_data in self.entities.items():
            self.graph.add_node(entity_id, **entity_data)
        
        # Add relationships as edges with weights
        for rel in relationships:
            source = rel.get('source')
            target = rel.get('target')
            
            # Ensure both source and target exist in our entities
            if source in self.entities and target in self.entities:
                weight = rel.get('strength', 0.5)  # Default strength if not provided
                if weight >= self.min_relationship_strength:
                    self.graph.add_edge(source, target, **rel)

    def _calculate_centrality(self) -> Dict[str, Dict]:
        """Calculate various centrality measures for the network - FIXED VERSION"""
        if len(self.graph) == 0 or self.graph.number_of_edges() == 0:
            return {}
            
        try:
            centrality_results = {}
            
            # Degree centrality (always works)
            centrality_results["degree_centrality"] = nx.degree_centrality(self.graph)
            
            # Betweenness centrality (requires connected graph)
            try:
                if nx.is_connected(self.graph) and len(self.graph) > 2:
                    centrality_results["betweenness_centrality"] = nx.betweenness_centrality(self.graph)
                else:
                    # For disconnected graphs, calculate per component
                    betweenness = {}
                    for component in nx.connected_components(self.graph):
                        if len(component) > 1:
                            subgraph = self.graph.subgraph(component)
                            sub_betweenness = nx.betweenness_centrality(subgraph)
                            betweenness.update(sub_betweenness)
                        else:
                            # Single node component has betweenness 0
                            node = list(component)[0]
                            betweenness[node] = 0.0
                    centrality_results["betweenness_centrality"] = betweenness
            except Exception as e:
                print(f"Betweenness centrality calculation warning: {e}")
                centrality_results["betweenness_centrality"] = centrality_results["degree_centrality"]
            
            # Eigenvector centrality (requires connected graph)
            try:
                if nx.is_connected(self.graph) and len(self.graph) > 1:
                    centrality_results["eigenvector_centrality"] = nx.eigenvector_centrality(self.graph, max_iter=1000, tol=1e-3)
                else:
                    # Use degree centrality as fallback
                    centrality_results["eigenvector_centrality"] = centrality_results["degree_centrality"]
            except:
                centrality_results["eigenvector_centrality"] = centrality_results["degree_centrality"]
            
            # Closeness centrality
            try:
                centrality_results["closeness_centrality"] = nx.closeness_centrality(self.graph)
            except:
                centrality_results["closeness_centrality"] = centrality_results["degree_centrality"]
            
            return centrality_results
        except Exception as e:
            print(f"Error calculating centrality: {e}")
            return {}
        
    def _detect_communities(self) -> Dict[str, Any]:
        """Detect community structure in the network - FIXED VERSION"""
        if len(self.graph) == 0 or self.graph.number_of_edges() == 0:
            return {"communities": [], "modularity": 0.0, "community_count": 0}
            
        try:
            # Check if graph has enough connections for community detection
            if self.graph.number_of_edges() < 2:
                # Create trivial communities - each node in its own community
                communities = [[node] for node in self.graph.nodes()]
                modularity = 0.0
            else:
                try:
                    # Use Louvain method for community detection
                    communities = nx.community.louvain_communities(self.graph, seed=42, resolution=1.0)
                    modularity = nx.community.modularity(self.graph, communities)
                except Exception as e:
                    print(f"Louvain community detection failed: {e}")
                    # Fallback to connected components as communities
                    communities = [list(component) for component in nx.connected_components(self.graph)]
                    modularity = 0.0
            
            # Format communities with entity details
            detailed_communities = []
            for i, community in enumerate(communities):
                community_entities = []
                community_influence = 0.0
                entity_count = 0
                
                for node_id in community:
                    if node_id in self.entities:
                        entity_data = self.entities[node_id].copy()
                        community_entities.append(entity_data)
                        influence = self._calculate_entity_influence(node_id)
                        community_influence += influence
                        entity_count += 1
                
                if community_entities:  # Only add non-empty communities
                    avg_influence = community_influence / entity_count if entity_count > 0 else 0
                    
                    detailed_communities.append({
                        "id": i + 1,
                        "size": len(community_entities),
                        "entities": community_entities,
                        "influence_score": avg_influence
                    })
            
            return {
                "communities": detailed_communities,
                "modularity": modularity,
                "community_count": len(detailed_communities)
            }
        except Exception as e:
            print(f"Error detecting communities: {e}")
            # Fallback: each node as its own community
            communities = [[node] for node in self.graph.nodes() if node in self.entities]
            detailed_communities = []
            for i, community in enumerate(communities):
                community_entities = [self.entities[node_id] for node_id in community if node_id in self.entities]
                if community_entities:
                    detailed_communities.append({
                        "id": i + 1,
                        "size": len(community_entities),
                        "entities": community_entities,
                        "influence_score": 0.0
                    })
            
            return {
                "communities": detailed_communities,
                "modularity": 0.0,
                "community_count": len(detailed_communities)
            }  
        except Exception as e:
            print(f"Error detecting communities: {e}")
            # Fallback: each node as its own community
            communities = [[node] for node in self.graph.nodes()]
            detailed_communities = []
            for i, community in enumerate(communities):
                community_entities = [self.entities[node_id] for node_id in community if node_id in self.entities]
                if community_entities:
                    detailed_communities.append({
                        "id": i + 1,
                        "size": len(community_entities),
                        "entities": community_entities,
                        "influence_score": 0.0
                    })
            
            return {
                "communities": detailed_communities,
                "modularity": 0.0,
                "community_count": len(detailed_communities)
            }
        
    def _calculate_influence_scores(self) -> List[Dict]:
        """Calculate influence scores for all entities"""
        influence_scores = []
        
        for entity_id in self.graph.nodes():
            score = self._calculate_entity_influence(entity_id)
            entity_data = self.entities[entity_id].copy()
            entity_data['influence_score'] = score
            influence_scores.append(entity_data)
        
        # Sort by influence score (descending)
        return sorted(influence_scores, key=lambda x: x.get('influence_score', 0), reverse=True)
    
    def _calculate_entity_influence(self, entity_id: int) -> float:
        """Calculate influence score for a single entity"""
        if entity_id not in self.graph:
            return 0.0
            
        try:
            # Multi-factor influence calculation
            centrality = nx.degree_centrality(self.graph).get(entity_id, 0)
            betweenness = nx.betweenness_centrality(self.graph).get(entity_id, 0)
            
            # Entity type multiplier
            entity_type = self.entities[entity_id].get('type', '').lower()
            type_multiplier = {
                'corporation': 1.2,
                'government': 1.3,
                'person': 1.1,
                'organization': 1.0
            }.get(entity_type, 1.0)
            
            # Calculate base influence
            base_influence = (centrality * 0.4 + betweenness * 0.6) * 100
            
            return min(base_influence * type_multiplier, 100.0)
            
        except Exception as e:
            print(f"Error calculating influence for entity {entity_id}: {e}")
            return 0.0
    
    def _analyze_structure(self) -> Dict[str, Any]:
        """Analyze structural properties of the network"""
        if len(self.graph) == 0:
            return {}
            
        try:
            # Calculate various network metrics
            degree_sequence = [d for n, d in self.graph.degree()]
            avg_degree = sum(degree_sequence) / len(degree_sequence) if degree_sequence else 0
            
            return {
                "average_degree": avg_degree,
                "diameter": nx.diameter(self.graph) if nx.is_connected(self.graph) else "Disconnected",
                "average_clustering": nx.average_clustering(self.graph),
                "assortativity": nx.degree_assortativity_coefficient(self.graph),
                "degree_distribution": {
                    "min": min(degree_sequence) if degree_sequence else 0,
                    "max": max(degree_sequence) if degree_sequence else 0,
                    "median": sorted(degree_sequence)[len(degree_sequence)//2] if degree_sequence else 0
                }
            }
        except Exception as e:
            print(f"Error analyzing network structure: {e}")
            return {}
    
    def _generate_key_findings(self, centrality: Dict, communities: Dict) -> List[str]:
        """Generate human-readable key findings from analysis"""
        findings = []
        
        if not centrality or not communities:
            return ["Insufficient data for detailed analysis"]
        
        # Most influential entities
        if centrality.get('degree_centrality'):
            most_central = max(centrality['degree_centrality'].items(), key=lambda x: x[1])
            entity_name = self.entities[most_central[0]].get('name', f"Entity {most_central[0]}")
            findings.append(f"Most central entity: {entity_name} (centrality: {most_central[1]:.3f})")
        
        # Community insights
        if communities.get('communities'):
            largest_community = max(communities['communities'], key=lambda x: x['size'])
            findings.append(f"Network divided into {communities['community_count']} communities")
            findings.append(f"Largest community has {largest_community['size']} entities")
        
        # Network health
        if len(self.graph) > 0:
            density = nx.density(self.graph)
            if density > 0.5:
                findings.append("Highly interconnected network (dense structure)")
            elif density < 0.1:
                findings.append("Sparse network with limited connections")
            else:
                findings.append("Moderately connected network")
        
        return findings
    
    def find_connection_paths(self, entity1_id: int, entity2_id: int, max_paths: int = 5) -> List[List[Dict]]:
        """Find all connection paths between two entities"""
        if entity1_id not in self.graph or entity2_id not in self.graph:
            return []
            
        try:
            paths = list(nx.all_simple_paths(self.graph, entity1_id, entity2_id, cutoff=self.max_network_depth))
            paths = paths[:max_paths]  # Limit number of paths
            
            # Convert node IDs to entity details
            detailed_paths = []
            for path in paths:
                detailed_path = [self.entities[node_id] for node_id in path]
                detailed_paths.append(detailed_path)
            
            return detailed_paths
        except Exception as e:
            print(f"Error finding connection paths: {e}")
            return []
    
    def calculate_influence(self, entity_id: int) -> float:
        """Public method to calculate influence for a specific entity"""
        return self._calculate_entity_influence(entity_id)
    
    def get_entity_neighbors(self, entity_id: int, relationship_type: str = None) -> List[Dict]:
        """Get all neighbors of an entity, optionally filtered by relationship type"""
        if entity_id not in self.graph:
            return []
            
        neighbors = []
        for neighbor_id in self.graph.neighbors(entity_id):
            edge_data = self.graph.get_edge_data(entity_id, neighbor_id)
            
            if relationship_type is None or edge_data.get('type') == relationship_type:
                neighbor_data = self.entities[neighbor_id].copy()
                neighbor_data['relationship'] = edge_data
                neighbors.append(neighbor_data)
        
        return neighbors
    
    def export_network_data(self, format: str = "json") -> str:
        """Export network data in various formats"""
        data = {
            "entities": list(self.entities.values()),
            "relationships": self.relationships,
            "metadata": {
                "total_entities": len(self.entities),
                "total_relationships": len(self.relationships),
                "analysis_timestamp": pd.Timestamp.now().isoformat()
            }
        }
        
        if format.lower() == "json":
            return json.dumps(data, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def clear_network(self) -> None:
        """Clear the current network data"""
        self.graph.clear()
        self.entities.clear()
        self.relationships.clear()
        self.analysis_cache.clear()


# Utility functions
def create_sample_network() -> PowerMapper:
    """Create a sample power network for testing"""
    mapper = PowerMapper()
    
    # Sample entities
    entities = [
        {"id": 1, "name": "Tech Giant Inc", "type": "corporation", "sector": "technology"},
        {"id": 2, "name": "Government Agency", "type": "government", "sector": "government"},
        {"id": 3, "name": "Industry Association", "type": "organization", "sector": "advocacy"},
        {"id": 4, "name": "Media Conglomerate", "type": "corporation", "sector": "media"},
        {"id": 5, "name": "Political Figure", "type": "person", "sector": "government"}
    ]
    
    # Sample relationships
    relationships = [
        {"source": 1, "target": 2, "type": "lobbying", "strength": 0.8},
        {"source": 1, "target": 3, "type": "membership", "strength": 0.9},
        {"source": 2, "target": 5, "type": "employment", "strength": 0.7},
        {"source": 3, "target": 4, "type": "partnership", "strength": 0.6},
        {"source": 4, "target": 5, "type": "endorsement", "strength": 0.5}
    ]
    
    mapper.analyze_network(entities, relationships)
    return mapper