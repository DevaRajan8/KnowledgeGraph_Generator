from typing import List, Dict, Any

# Define which keys in the nested "properties" should generate relationships.
RELATIONSHIP_PROPERTIES = {
    "instance of": "instance_of",
    "subclass of": "subclass_of",
    "influenced by": "influenced_by",
    "developer": "developer",
    "official website": "official_website",
}

class Node:
    def __init__(self, id: str, type: str, properties: Dict[str, Any] = None):
        self.id = id
        self.type = type
        self.properties = properties if properties else {}

    def to_dict(self):
        return {"id": self.id, "type": self.type, "properties": self.properties}

class Relationship:
    def __init__(self, source: Node, target: Node, type: str, properties: Dict[str, Any] = None):
        self.source = source
        self.target = target
        self.type = type
        self.properties = properties if properties else {}

    def to_dict(self):
        return {
            "source": self.source.id,
            "target": self.target.id,
            "type": self.type,
            "properties": self.properties
        }

class GraphDocument:
    def __init__(self, nodes: List[Node], relationships: List[Relationship]):
        self.nodes = nodes
        self.relationships = relationships

    def to_dict(self):
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "relationships": [r.to_dict() for r in self.relationships]
        }

def build_knowledge_graph(topics: List[Dict[str, Any]]) -> GraphDocument:
    nodes_map = {}  # key: node id, value: Node instance
    relationships = []

    # First, create nodes for each topic.
    for topic in topics:
        # Use topic title as node id (strip extra spaces)
        node_id = topic.get("title", "Unknown").strip()
        node_type = topic.get("topic_type", "entity")
        
        # Copy all keys from the topic except "title", "topic_type", and "properties" (which we handle separately)
        node_details = {k: v for k, v in topic.items() if k not in ["title", "topic_type", "properties", "references"]}
        # Also merge the original nested "properties" (which holds relationship data) into node_details.
        if "properties" in topic:
            # If you want to keep them separate, you might nest them under a key like "relationship_properties".
            node_details["relationship_properties"] = topic["properties"]
        
        node = Node(id=node_id, type=node_type, properties=node_details)
        nodes_map[node_id] = node

    # Now, create relationships from the nested "properties" field.
    for topic in topics:
        source_id = topic.get("title", "Unknown").strip()
        source_node = nodes_map.get(source_id)
        if not source_node:
            continue

        # Use the original "properties" key from the topic (if present) for relationship generation.
        prop_dict = topic.get("properties", {})
        for prop_key, values in prop_dict.items():
            if prop_key not in RELATIONSHIP_PROPERTIES:
                continue

            rel_type = RELATIONSHIP_PROPERTIES[prop_key]
            for val in values:
                target_label = val.get("label", "").strip()
                if not target_label:
                    continue

                # If the target node already exists (from topics), use it; otherwise create an external node.
                if target_label in nodes_map:
                    target_node = nodes_map[target_label]
                else:
                    # Create a new node with type "entity" and with the value object as its property.
                    target_node = Node(id=target_label, type="entity", properties=val)
                    nodes_map[target_label] = target_node

                rel = Relationship(source=source_node, target=target_node, type=rel_type)
                relationships.append(rel)

    all_nodes = list(nodes_map.values())
    return GraphDocument(nodes=all_nodes, relationships=relationships)
