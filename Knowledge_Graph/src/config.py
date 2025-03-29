import os

# Existing config values...
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "my_kg_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "my_kg_collection")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma")

DEFAULT_DOMAIN = "programming"
DATA_DIR = os.getenv("DATA_DIR", "./output")
REDIS_CACHE_EXPIRATION = 86400

WIKIDATA_ENDPOINT = os.getenv("WIKIDATA_ENDPOINT", "https://query.wikidata.org/sparql")
WIKIDATA_USER_AGENT = os.getenv("WIKIDATA_USER_AGENT", "KnowledgeGraphBot/1.0 (your-email@example.com)")
WIKIPEDIA_USER_AGENT = os.getenv("WIKIPEDIA_USER_AGENT", "KnowledgeGraphWikipediaBot/1.0 (your-email@example.com)")
DOMAIN = os.getenv("DOMAIN", "programming")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 5))

# In src/config.py
DOMAIN = "programming"

# Define default colors for each domain (customize as needed)
DOMAIN_COLORS = {
    "programming": {
        "programming_language": "#FF5733",
        "framework": "#33FF57",
        "unknown": "#CCCCCC"
    }
}

# Define colors for each topic type
TOPIC_TYPE_COLORS = {
    "programming_language": "#FF5733",
    "framework": "#33FF57",
    "library": "#3357FF",
    "unknown": "#CCCCCC"
}

# If you have DOMAIN_CONFIGS already, keep it as is.


# Domain-specific configuration for SPARQL queries
DOMAIN_CONFIGS = {
    "programming": {
        "name": "Programming",
        "topics": [
            {
                "type": "object_oriented_programming",
                "entity_id": "Q79872",
                "description": "programming paradigm based on the concept of objects",
            },
            {
                "type": "programming_language",
                "entity_id": "Q9143",
                "description": "Programming languages",
            },
            {
                "type": "programming_paradigm",
                "entity_id": "Q188267",
                "description": "Programming paradigms",
            },
            {
                "type": "software_framework",
                "entity_id": "Q271680",
                "description": "Software frameworks",
            },
            {
                "type": "software_development",
                "entity_id": "Q638608",
                "description": "Software development",
            },
            {
                "type": "computer_programming",
                "entity_id": "Q80006",
                "description": "the process of designing and building an executable computer program to accomplish a specific computing result or to perform a specific task",
            },
        ],
    },
    "mathematics": {
        "name": "Mathematics",
        "topics": [
            {
                "type": "mathematical_concept",
                "entity_id": "Q2754677",
                "description": "Mathematical concepts",
            },
            {
                "type": "mathematical_theorem",
                "entity_id": "Q47317",
                "description": "Mathematical theorems",
            },
            {
                "type": "mathematical_field",
                "entity_id": "Q12482",
                "description": "Fields of mathematics",
            },
            {
                "type": "mathematician",
                "entity_id": "Q170790",
                "description": "Mathematicians",
            },
            {
                "type": "mathematical_object",
                "entity_id": "Q246672",
                "description": "Mathematical objects",
            },
        ],
    },
}

