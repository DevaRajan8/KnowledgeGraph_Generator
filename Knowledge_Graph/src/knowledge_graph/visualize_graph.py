import networkx as nx
from pyvis.network import Network
import random
import json
from pathlib import Path
import os
from src.config import DOMAIN_COLORS, DOMAIN, TOPIC_TYPE_COLORS
from src.logger import get_logger

logger = get_logger(__name__)

def _escape_xml(text):
    """Escape special characters for XML."""
    if not isinstance(text, str):
        text = str(text)
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
    )

def _get_color_for_topic_type(topic_type, color_scheme=None):
    """Return a color hex code based on topic type for consistent coloring."""
    if color_scheme is None:
        color_scheme = TOPIC_TYPE_COLORS

    if isinstance(topic_type, str):
        topic_type = topic_type.lower().strip()
    return color_scheme.get(topic_type, color_scheme.get("unknown", "#cccccc"))

def _save_graphml(graphml, filename):
    """Save GraphML data to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(graphml)
    logger.info(f"GraphML data saved to {filename}")

def _convert_to_graphml(knowledge_graph_data):
    """Convert knowledge graph data to GraphML format."""
    logger.info("Converting knowledge graph data to GraphML format.")

    # Use "topics" if available; fallback to "nodes"
    nodes = knowledge_graph_data.get("topics", knowledge_graph_data.get("nodes", []))
    # Use edges if available; otherwise empty list
    edges = knowledge_graph_data.get("edges", [])

    # Get domain from metadata if available, otherwise use default
    domain = knowledge_graph_data.get("metadata", {}).get("domain", DOMAIN)
    color_scheme = DOMAIN_COLORS.get(domain, DOMAIN_COLORS[DOMAIN])

    graphml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    graphml += '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">\n'
    graphml += '  <key id="label" for="node" attr.name="label" attr.type="string"/>\n'
    graphml += '  <key id="description" for="node" attr.name="description" attr.type="string"/>\n'
    graphml += '  <key id="topic_type" for="node" attr.name="topic_type" attr.type="string"/>\n'
    graphml += '  <key id="color" for="node" attr.name="color" attr.type="string"/>\n'
    graphml += '  <key id="edge_type" for="edge" attr.name="type" attr.type="string"/>\n'
    graphml += '  <key id="weight" for="edge" attr.name="weight" attr.type="double"/>\n'
    graphml += '  <graph id="G" edgedefault="undirected">\n'

    for node in nodes:
        # Use node's "id" as label
        label = node.get("id", "unknown")
        description = ""
        if "properties" in node:
            description = node["properties"].get("description", "")
        topic_type = node.get("type", "unknown").lower()
        color = _get_color_for_topic_type(topic_type, color_scheme)

        graphml += f'    <node id="{label}">\n'
        graphml += f'      <data key="label">{_escape_xml(label)}</data>\n'
        if description:
            graphml += f'      <data key="description">{_escape_xml(description)}</data>\n'
        graphml += f'      <data key="topic_type">{_escape_xml(topic_type)}</data>\n'
        graphml += f'      <data key="color">{color}</data>\n'
        graphml += "    </node>\n"

    for edge in edges:
        edge_type = edge.get("type", "unknown")
        weight = edge.get("weight", 1)
        source = edge.get("source")
        target = edge.get("target")
        graphml += f'    <edge source="{source}" target="{target}">\n'
        graphml += f'      <data key="edge_type">{edge_type}</data>\n'
        graphml += f'      <data key="weight">{weight}</data>\n'
        graphml += "    </edge>\n"

    graphml += "  </graph>\n"
    graphml += "</graphml>"
    return graphml

def _create_networkx_graph(knowledge_graph_data):
    """Create a NetworkX graph from knowledge graph data."""
    G = nx.Graph()
    nodes = knowledge_graph_data.get("topics", knowledge_graph_data.get("nodes", []))
    domain = knowledge_graph_data.get("metadata", {}).get("domain", DOMAIN)
    color_scheme = DOMAIN_COLORS.get(domain, DOMAIN_COLORS[DOMAIN])

    for node in nodes:
        label = node.get("id", "unknown")
        description = ""
        if "properties" in node:
            description = node["properties"].get("description", "")
        topic_type = node.get("type", "unknown").lower()
        node_attrs = {
            "label": label,
            "description": description,
            "topic_type": topic_type,
            "color": _get_color_for_topic_type(topic_type, color_scheme),
            "title": f"{label}<br>{description}",
        }
        G.add_node(label, **node_attrs)

    for edge in knowledge_graph_data.get("edges", []):
        edge_type = edge.get("type", "unknown")
        weight = edge.get("weight", 1)
        source = edge.get("source")
        target = edge.get("target")
        G.add_edge(source, target, type=edge_type, weight=weight, title=f"Type: {edge_type}")

    return G

def _save_as_html(G, output_path):
    """Visualize the knowledge graph using Pyvis."""
    random.seed(42)

    net = Network(height="800px", width="100%", notebook=False, directed=False)
    net.barnes_hut(gravity=-80000, central_gravity=0.3, spring_length=250)
    net.from_nx(G)
    net.set_options("""
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "solver": "forceAtlas2Based",
        "stabilization": {
          "iterations": 150
        }
      },
      "nodes": {
        "font": {
          "size": 14,
          "face": "Tahoma",
          "color": "#333333"
        },
        "borderWidth": 2,
        "borderWidthSelected": 4,
        "scaling": {
          "min": 20,
          "max": 30
        },
        "shadow": true
      },
      "edges": {
        "color": {
          "inherit": false,
          "opacity": 0.7
        },
        "smooth": {
          "enabled": true,
          "type": "continuous"
        },
        "arrows": {
          "to": {
            "enabled": true,
            "scaleFactor": 0.5
          }
        },
        "shadow": true
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 200,
        "hideEdgesOnDrag": true
      }
    }
    """)
    net.write_html(output_path, notebook=False)
    logger.info(f"Interactive visualization saved to {output_path}")

def generate_graphml_and_save_as_html(knowledge_graph_data, save_dir="output"):
    """Generate and save the knowledge graph as GraphML and HTML files."""
    logger.info("Generating and saving knowledge graph visualizations.")
    save_dir = Path(save_dir)
    save_dir.mkdir(exist_ok=True, parents=True)

    base_name = "knowledge_graph"
    graphml_file = save_dir / f"{base_name}.graphml"
    html_file = save_dir / f"{base_name}.html"

    graphml = _convert_to_graphml(knowledge_graph_data)
    _save_graphml(graphml, graphml_file)

    G = _create_networkx_graph(knowledge_graph_data)
    _save_as_html(G, str(html_file))

    return str(html_file)

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate visualizations for a knowledge graph"
    )
    parser.add_argument("--file", type=str, help="Path to the knowledge graph JSON file")
    parser.add_argument(
        "--domain",
        type=str,
        default=DOMAIN,
        choices=list(DOMAIN_COLORS.keys()),
        help=f"Domain to use for visualization colors (default: {DOMAIN})",
    )

    args = parser.parse_args()

    if args.file:
        input_file = args.file
    else:
        output_dir = Path("output")
        json_files = list(output_dir.glob("*_knowledge_graph_*.json"))
        if not json_files:
            print("No knowledge graph files found. Please run main.py first.")
            sys.exit(1)
        input_file = str(max(json_files, key=os.path.getctime))
        print(f"Using the most recent file: {input_file}")

    with open(input_file, encoding="utf-8") as f:
        data = json.load(f)
        if args.domain:
            if "metadata" not in data:
                data["metadata"] = {"domain": args.domain}
            elif "domain" not in data["metadata"]:
                data["metadata"]["domain"] = args.domain

    html_path = generate_graphml_and_save_as_html(data)
    print(f"Knowledge graph visualization created at {html_path}")
