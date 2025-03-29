import redis
from redis import Redis, ConnectionPool
from src.logger import get_logger
from src.config import REDIS_HOST, REDIS_PORT, REDIS_DB

logger = get_logger(__name__)
_redis_pool = None

def get_redis_pool() -> ConnectionPool:
    global _redis_pool
    if _redis_pool is None:
        try:
            _redis_pool = redis.ConnectionPool(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                decode_responses=False,
                socket_timeout=5.0,
                socket_connect_timeout=5.0,
            )
            logger.debug("Redis connection pool created")
        except Exception as e:
            logger.error(f"Failed to create Redis connection pool: {str(e)}")
            raise
    return _redis_pool

def get_redis_client() -> Redis:
    try:
        return Redis(connection_pool=get_redis_pool())
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        # Return a fallback if needed
        return None
