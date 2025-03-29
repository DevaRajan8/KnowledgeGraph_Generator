import asyncio
import json
import argparse
from pathlib import Path
from datetime import datetime
from src.logger import get_logger
from src.config import DATA_DIR, DEFAULT_DOMAIN
from src.data_collection import get_and_save_from_wiki
from src.database.mongo import store_topics_in_mongo
from src.knowledge_graph import build_knowledge_graph

logger = get_logger(__name__)

async def main(domain: str, limit: int, save_graph: bool):
    # Create an output folder with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(DATA_DIR) / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Dynamically fetch and save enriched topics
    topics = await get_and_save_from_wiki(domain=domain, limit=limit, save_dir=output_dir, save_to_mongo=False)
    if not topics:
        logger.warning("No topics retrieved; exiting.")
        return

    # Optionally store topics in MongoDB
    stored = await store_topics_in_mongo(topics, domain=domain)
    logger.info(f"Stored in MongoDB: {stored}")

    # Build the knowledge graph
    graph_document = build_knowledge_graph(topics)
    graph_json = json.dumps(graph_document.to_dict(), indent=2)
    
    # Save the graph JSON to a file
    if save_graph:
        out_path = output_dir / f"graph_{domain}_limit{limit}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(graph_json)
        logger.info(f"Saved graph to {out_path}")
    else:
        print(graph_json)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a Knowledge Graph from domain-specific topics dynamically."
    )
    parser.add_argument("--domain", type=str, default=DEFAULT_DOMAIN, help="Domain to fetch topics for")
    parser.add_argument("--limit", type=int, default=10, help="Number of topics to fetch")
    parser.add_argument("--save-graph", action="store_true", help="Save the JSON output to a file instead of printing")
    args = parser.parse_args()

    asyncio.run(main(args.domain, args.limit, args.save_graph))
