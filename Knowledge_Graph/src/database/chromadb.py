import chromadb
import logging
from typing import Dict, List, Optional, Any
from chromadb.api import client as ChromaClient
from chromadb.config import Settings
from chromadb.errors import InvalidCollectionException
from src.logger import get_logger
from src.config import CHROMA_PERSIST_DIR

logger = get_logger(__name__)

chromadb_logger = logging.getLogger("chromadb")
chromadb_logger.setLevel(logging.WARNING)

class ChromaDBClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ChromaDBClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, persist_directory: str = CHROMA_PERSIST_DIR):
        if self._initialized:
            return
        try:
            self._client = ChromaClient(
                Settings(
                    persist_directory=persist_directory,
                    is_persistent=True,
                    anonymized_telemetry=False,
                )
            )
            logger.info(f"ChromaDB client initialized with dir: {persist_directory}")
            self._initialized = True
        except Exception as e:
            logger.error(f"Error initializing ChromaDB client: {str(e)}")
            raise

    @property
    def client(self):
        if not hasattr(self, "_client"):
            raise RuntimeError("ChromaDB client not initialized.")
        return self._client

    def list_collections(self) -> List[str]:
        return [c.name for c in self.client.list_collections()]

    def collection_exists(self, name: str) -> bool:
        try:
            self.client.get_collection(name=name)
            return True
        except (ValueError, InvalidCollectionException):
            return False

    def get_or_create_collection(self, name: str, metadata: Optional[Dict[str, Any]] = None):
        try:
            return self.client.get_collection(name=name)
        except (ValueError, InvalidCollectionException):
            logger.info(f"Creating new ChromaDB collection: {name}")
            return self.client.create_collection(name=name, metadata=metadata)

    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        embeddings: List[List[float]],
        ids: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ):
        coll = self.get_or_create_collection(collection_name)
        coll.add(documents=documents, embeddings=embeddings, ids=ids, metadatas=metadatas)
        logger.info(f"Added {len(documents)} documents to '{collection_name}'")

    def query_collection(
        self,
        collection_name: str,
        query_embeddings: List[List[float]],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ):
        if not self.collection_exists(collection_name):
            raise ValueError(f"Collection '{collection_name}' does not exist.")
        coll = self.client.get_collection(name=collection_name)
        return coll.query(query_embeddings=query_embeddings, n_results=n_results, where=where)
