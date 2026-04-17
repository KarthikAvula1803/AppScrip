import time
import logging

logger = logging.getLogger(__name__)

# Simple in-memory cache: { key: (data, expiry_timestamp) }
cache_store = {}

# Cache expiry in seconds (5 minutes)
CACHE_EXPIRY = 300

def get_cache(key: str):
    """
    Retrieves data from the cache if it exists and hasn't expired.
    """
    if key in cache_store:
        data, timestamp = cache_store[key]
        if time.time() - timestamp < CACHE_EXPIRY:
            logger.info(f"Cache hit for key: {key}")
            return data
        else:
            logger.info(f"Cache expired for key: {key}")
            del cache_store[key]
    return None

def set_cache(key: str, value: any):
    """
    Stores data in the cache with the current timestamp.
    """
    logger.info(f"Caching data for key: {key}")
    cache_store[key] = (value, time.time())
