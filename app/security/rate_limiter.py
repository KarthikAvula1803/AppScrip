import time
import logging
from collections import deque
from fastapi import HTTPException

logger = logging.getLogger(__name__)

# Store user request data: { api_key: deque([timestamps]) }
user_requests = {}

RATE_LIMIT = 5  # requests per window
TIME_WINDOW = 60  # seconds

def check_rate_limit(api_key: str):
    """
    Enforces a rate limit of RATE_LIMIT requests per TIME_WINDOW seconds per API key.
    Uses an in-memory sliding window.
    """
    current_time = time.time()

    if api_key not in user_requests:
        user_requests[api_key] = deque()

    # sliding window: remove timestamps older than TIME_WINDOW
    while user_requests[api_key] and current_time - user_requests[api_key][0] > TIME_WINDOW:
        user_requests[api_key].popleft()

    if len(user_requests[api_key]) >= RATE_LIMIT:
        logger.warning(f"Rate limit exceeded for API key: {api_key}")
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again in a minute."
        )

    user_requests[api_key].append(current_time)
    logger.debug(f"Request allowed for {api_key}. Current window count: {len(user_requests[api_key])}")
