import os
import logging
from fastapi import Header, HTTPException

logger = logging.getLogger(__name__)

# Load API Key from environment
API_KEY = os.getenv("API_KEY")

def verify_api_key(x_api_key: str = Header(None)):
    """
    Validates the x-api-key header against the configured environment variable.
    """
    if not API_KEY:
        logger.error("API_KEY environment variable is not set. Security is compromised.")
        # In production, you might want to fail closed. 
        # For this setup, we will raise an error to alert the developer.
        raise HTTPException(status_code=500, detail="Security configuration error")

    if x_api_key != API_KEY:
        logger.warning(f"Unauthorized access attempt with key: {x_api_key}")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return x_api_key
