from .wikidata.sparql import get_topics_from_wikidata
from .wikipedia_.api import enrich_with_wikipedia
from src.logger import get_logger
import json

logger = get_logger(__name__)

async def get_data_from_wiki(domain: str, limit: int, save_to_mongo=True) -> list:
    """
    Fetch and enrich topics from Wikidata and Wikipedia dynamically.
    """
    # Fetch topics from Wikidata (using SPARQL)
    topics = await get_topics_from_wikidata(domain=domain, limit=limit)
    if not topics:
        logger.error(f"Failed to retrieve {domain} topics from Wikidata")
        return []
    
    logger.info(f"Successfully retrieved {len(topics)} topics from Wikidata")

    # Enrich topics with Wikipedia data
    enriched_topics = await enrich_with_wikipedia(topics, domain=domain, save_to_mongo=save_to_mongo)
    if not enriched_topics:
        logger.error(f"Failed to enrich {domain} topics with Wikipedia data")
        return []
    
    logger.info(f"Successfully enriched {len(enriched_topics)} topics with Wikipedia data")
    return enriched_topics

async def get_and_save_from_wiki(domain: str, limit: int, save_dir: str, save_to_mongo=True) -> list:
    """
    Fetch and enrich topics from Wikidata and Wikipedia.
    File saving is disabled in this version.
    """
    enriched_topics = await get_data_from_wiki(domain=domain, limit=limit, save_to_mongo=save_to_mongo)
    if not enriched_topics:
        logger.error(f"Failed to enrich {domain} topics with Wikipedia data")
        return []
    
    # File saving disabled; simply return the enriched topics.
    logger.info("File saving for enriched topics is disabled. Returning enriched topics directly.")
    return enriched_topics
