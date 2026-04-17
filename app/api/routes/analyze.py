"""
Analyze Router — /api/v1/analyze/{sector}
"""

import logging
from fastapi import APIRouter, HTTPException, Path
from app.models.response import AnalyzeResponse
from app.utils.helpers import sanitize_sector, validate_sector
from app.services.ai_service import analyze_with_ai
from app.services.formatter import format_to_markdown
from app.utils.cache import get_cache, set_cache
from app.services.data_collector import fetch_sector_data
from app.utils.advanced_features import (
    extract_keywords,
    calculate_confidence,
    analyze_sentiment,
    get_timestamp
)

logger = logging.getLogger(__name__)

router = APIRouter()
@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}



@router.get(
    "/analyze/{sector}",
    response_model=AnalyzeResponse,
    summary="Analyze a Market Sector",
    description=(
        "Accepts a sector name as a path parameter, validates it, "
        "and returns a structured market analysis response."
    ),
    responses={
        200: {"description": "Successful analysis response"},
        400: {"description": "Invalid sector name provided"},
        500: {"description": "Internal server error"},
    },
)
async def analyze_sector(
    sector: str = Path(
        ...,
        min_length=3,
        max_length=30,
        description="Name of the market sector to analyze (alphabetic characters only)",
        examples=["pharma"],
    ),
) -> AnalyzeResponse:
    """
    Analyze a given market sector.

    - **sector**: Must be alphabetic, minimum 3 characters, maximum 50 characters.
    """
    try:
        logger.info(f"Received analysis request for sector: '{sector}'")

        # Sanitize input
        clean_sector = sanitize_sector(sector)

        # Validate business rules
        is_valid, error_msg = validate_sector(clean_sector)
        if not is_valid:
            logger.warning(f"Validation failed for sector '{sector}': {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)

        logger.info(f"Successfully processed sector: '{clean_sector}'")

        # Phase 5: Cache Check
        cached_result = get_cache(clean_sector)
        if cached_result:
            logger.info(f"Serving cached data for {clean_sector}")
            return AnalyzeResponse(
                sector=clean_sector,
                message="Market analysis retrieved from cache",
                status="success",
                report=cached_result,
                cached=True
            )

        # Fetch real-time market data
        fetched_data = await fetch_sector_data(clean_sector)

        # Phase 6: Advanced Features
        keywords = extract_keywords(fetched_data)
        confidence = calculate_confidence(fetched_data)
        sentiment = analyze_sentiment(fetched_data)
        timestamp = get_timestamp()
        
        # Fallback values for safety (Phase 6 Failure-proofing)
        if not keywords:
            keywords = ["market", "data"]
        sentiment = sentiment or "Neutral"
        sources = [item.get("link") for item in fetched_data]
        if not sources:
            sources = ["No sources available"]

        # Phase 3: AI Analysis
        context_data = [
            f"Title: {item.get('title')} | Link: {item.get('link')}"
            for item in fetched_data
        ]
        analysis_text = await analyze_with_ai(clean_sector, context_data)

        # Phase 4 & 6: Markdown Report Generation
        markdown_report = format_to_markdown(
            clean_sector,
            analysis_text,
            keywords,
            sentiment,
            confidence,
            sources,
            timestamp
        )

        # Phase 5: Save to Cache
        set_cache(clean_sector, markdown_report)

        return AnalyzeResponse(
            sector=clean_sector,
            message="Market analysis service is active",
            status="success",
            report=markdown_report,
            data=fetched_data,
            data_count=len(fetched_data) if fetched_data else 0,
            cached=False
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error while processing sector '{sector}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
