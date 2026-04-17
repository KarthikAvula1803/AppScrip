"""
Response Models — Output schemas using Pydantic.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class DataItem(BaseModel):
    """
    Represents a single news/market data entry fetched from external sources.
    """

    title: str = Field(..., description="Headline or result title", examples=["India tech sector sees rapid AI growth"])
    snippet: str = Field("", description="Short description or summary snippet")
    link: str = Field("", description="Source URL or domain reference")


class AnalyzeResponse(BaseModel):
    """
    Standard response schema for the /analyze/{sector} endpoint.
    """

    sector: str = Field(
        ...,
        description="The sanitized name of the analyzed sector",
        examples=["pharma"],
    )
    message: str = Field(
        ...,
        description="Status message from the analysis service",
        examples=["Market analysis service is active"],
    )
    status: str = Field(
        ...,
        description="Request outcome: 'success' or 'error'",
        examples=["success"],
    )
    data: Optional[List[DataItem]] = Field(
        default=None,
        description="Real-time news/market data fetched for the sector (max 10 entries)",
    )
    data_count: Optional[int] = Field(
        default=None,
        description="Number of data entries returned",
    )
    report: Optional[str] = Field(
        default=None,
        description="Markdown formatted AI analysis report",
    )
    cached: bool = Field(
        default=False,
        description="Whether the response was served from cache",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sector": "pharma",
                    "message": "Market analysis service is active",
                    "status": "success",
                    "report": "# Pharma Sector - Market Analysis\n\n## 📈 Market Trends...",
                    "data": [
                        {
                            "title": "Pharma sector India sees record exports in 2026",
                            "snippet": "Indian pharmaceutical industry hits $28bn in exports driven by generics.",
                            "link": "economictimes.indiatimes.com",
                        }
                    ],
                    "data_count": 1,
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """
    Standard error response schema.
    """

    detail: str = Field(
        ...,
        description="Human-readable error message",
        examples=["Invalid sector name"],
    )
