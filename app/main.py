"""
Market Analysis API - Entry Point
Author: Senior Backend Engineer
"""

import logging
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes import analyze
from app.security.auth import verify_api_key
from app.security.rate_limiter import check_rate_limit

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# --- App Initialization ---
app = FastAPI(
    title="Market Analysis API",
    description=(
        "A production-ready RESTful API for market sector analysis. "
        "Provides sector-level insights, validation, and structured responses."
    ),
    version="1.0.0",
    contact={
        "name": "Market Analysis Team",
        "email": "support@marketanalysis.io",
    },
    license_info={
        "name": "MIT",
    },
)

# --- Include Routers ---
app.include_router(analyze.router, prefix="/api/v1", tags=["Sector Analysis"])


# --- Security Middleware ---
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """
    Global middleware to handle API Key Authentication and Rate Limiting.
    Excludes base, documentation, and health check endpoints.
    """
    path = request.url.path
    # Exclude public endpoints
    if path in ["/", "/health", "/docs", "/openapi.json", "/api/v1/", "/api/v1/health"]:
        return await call_next(request)

    try:
        api_key = request.headers.get("x-api-key")

        # Auth check
        verify_api_key(api_key)

        # Rate limiting
        check_rate_limit(api_key)

        response = await call_next(request)
        return response

    except Exception as e:
        status_code = getattr(e, "status_code", 500)
        detail = getattr(e, "detail", "Internal Server Error")
        
        # Log unauthorized access or rate limit violations
        if status_code in [401, 429]:
            logger.warning(f"Security event on {path}: {detail} (Status: {status_code})")
        else:
            logger.error(f"Middleware error on {path}: {str(e)}")

        return JSONResponse(
            status_code=status_code,
            content={"status": "error", "message": detail}
        )


# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error. Please try again later."},
    )


# --- Health Check ---
@app.get("/health", tags=["Health"])
async def health_check():
    """Returns API health status."""
    logger.info("Health check endpoint accessed.")
    return {"status": "ok", "message": "Market Analysis API is running."}


# --- Root ---
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API info."""
    return {
        "api": "Market Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
