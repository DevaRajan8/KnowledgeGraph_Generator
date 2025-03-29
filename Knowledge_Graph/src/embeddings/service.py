import asyncio
import uuid
import time
from typing import List, Dict, Any
import ollama

from src.logger import get_logger
from src.config import OLLAMA_BASE_URL, OLLAMA_EMBEDDING_MODEL
from src.database.chromadb import ChromaDBClient

logger = get_logger(__name__)

async def generate_embedding_async(text: str) -> List[float]:
    try:
        client = ollama.AsyncClient(host=OLLAMA_BASE_URL)
        response = await client.embed(model=OLLAMA_EMBEDDING_MODEL, input=text)
        return response.embeddings
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        return []

async def generate_embeddings_batch_async(texts: List[str]) -> List[List[float]]:
    tasks = [generate_embedding_async(t) for t in texts]
    all_embeddings = await asyncio.gather(*tasks)
    return all_embeddings

async def process_topics_batch_async(
    topics: List[Dict[str, Any]],
    collection_name: str = "programming_embeddings"
) -> List[Dict[str, Any]]:
    if not topics:
        return []
    texts = [t.get("content_for_embedding", "") or t.get("summary", "") for t in topics]
    embeddings = await generate_embeddings_batch_async(texts)

    # Store embeddings in Chroma
    chroma_client = ChromaDBClient()
    ids = []
    for topic in topics:
        # Make an ID that is unique
        topic_id = f"{topic.get('id','unknown')}_{uuid.uuid4()}"
        ids.append(topic_id)

    # For metadata, you can store anything relevant
    metadatas = [{"topic_id": t.get("id")} for t in topics]

    chroma_client.add_documents(
        collection_name=collection_name,
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    # Attach an embedding reference back to each topic if needed
    for i, topic in enumerate(topics):
        topic["embedding_id"] = ids[i]

    return topics
