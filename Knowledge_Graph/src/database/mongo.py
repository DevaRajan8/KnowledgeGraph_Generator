from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, Any, List
from src.config import MONGO_URI, MONGO_DB, MONGO_COLLECTION
from src.logger import get_logger

logger = get_logger(__name__)

async def get_mongo_client():
    client = AsyncIOMotorClient(MONGO_URI)
    return client[MONGO_DB]

async def store_topics_in_mongo(topics: List[Dict[str, Any]], domain: str) -> bool:
    """Store or upsert topics in MongoDB."""
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]

        if topics:
            for topic in topics:
                await collection.update_one(
                    {"id": topic["id"], "domain": domain},
                    {"$set": topic},
                    upsert=True
                )
            logger.info(f"Stored {len(topics)} topics in MongoDB collection '{MONGO_COLLECTION}'")
            return True
        return False
    except Exception as e:
        logger.error(f"Error storing topics in MongoDB: {str(e)}")
        return False

async def get_topics_from_mongo(
    domain: str, limit: int = 100, filter_criteria: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """Retrieve topics from MongoDB by domain."""
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]

        query = {"domain": domain}
        if filter_criteria:
            query.update(filter_criteria)

        cursor = collection.find(query).limit(limit)
        topics = await cursor.to_list(length=limit)
        logger.info(f"Retrieved {len(topics)} topics from MongoDB for domain '{domain}'")
        return topics
    except Exception as e:
        logger.error(f"Error retrieving topics from MongoDB: {str(e)}")
        return []
