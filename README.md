# Knowledge Graph Generator

A tool to create a comprehensive knowledge graph of topics, concepts, and their relationships.

## Overview

This project fetches domain-specific data from multiple sources and combines them into a cohesive knowledge graph that can be used for:

- Learning path (Knowledge Graph) generation
- Visualizing relationships between concepts
- Educational content organization
- Research on evolution and relationships

## Features

- Retrieves domain-specific topics from Wikidata using SPARQL
- Enriches topics with Wikipedia content, summaries and categories
- Handles disambiguation pages and search intelligently
- Creates a preliminary graph structure with topics as nodes and relationships as edges
- Uses async and batching to be efficient
- Comprehensive error handling and logging
- Caches results in redis to avoid redundant API calls
- Stores topics in mongoDB for easy access and manipulation

## Installation

1. Make sure you have Python 3.12+ installed
2. Clone this repository
3. Install dependencies:

```bash
pip install uv
uv venv
source .venv/bin/activate
uv sync --reinstall
```

## Usage

Run the main script to generate the knowledge graph:

```bash
python -m src.main --domain programming --limit 10 --save-graph
```

This will load the local JSON (or fetch from Wikidata if you add that logic), build a graph, and output a file like output/ with a timestamp/graph_programming_limit10.json.

## Data Structure

The generated knowledge graph JSON has the following structure:

```json
{
  "nodes": [
    {
      "id": "assembly language",
      "type": "programming_language",
      "properties": {
        "wikidata_url": "http://www.wikidata.org/entity/Q165436",
        "description": "any low-level programming language ...",
        "url": "https://en.wikipedia.org/wiki/Assembly_language",
        "summary": "In computer programming, assembly language ...",
        "categories": [ ... ],
        "content": "In computer programming, assembly language ...",
        "sections": [],
        "domain": "programming",
        "relationship_properties": {
          "subclass of": [ ... ],
          "inception": [ ... ],
          "instance of": [ ... ]
        }
      }
    },
    {
      "id": "ARexx",
      "type": "programming_language",
      "properties": { ... }
    },
    ...
  ],
  "relationships": [
    {
      "source": "assembly language",
      "target": "low-level programming language",
      "type": "subclass_of",
      "properties": {}
    },
    {
      "source": "assembly language",
      "target": "programming language",
      "type": "instance_of",
      "properties": {}
    },
    ...
  ]
}
```

## Graph Builder

The graph builder (in src/knowledge_graph/graph_builder.py) takes the enriched topics and converts them into nodes and relationships. Each node includes all the topic details (e.g., URL, summary, content) merged into its properties, and relationships are created from selected nested properties (like "instance of", "subclass of", etc.). This module is automatically invoked by the main script.

## Configuration

config.py: Contains the main configuration for the project including database settings, API endpoints, domain configurations, and SPARQL queries.

wikidata/queries.py: Contains SPARQL query templates and domain-specific query configurations
