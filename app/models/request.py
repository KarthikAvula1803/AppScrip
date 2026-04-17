"""
Request Models — Input validation schemas using Pydantic.
"""

from pydantic import BaseModel, Field, field_validator


class SectorRequest(BaseModel):
    """
    Schema representing an incoming sector analysis request.
    Used for documentation and potential future POST endpoints.
    """

    sector: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Name of the market sector (alphabetic only)",
        examples=["pharma", "technology", "energy"],
    )

    @field_validator("sector")
    @classmethod
    def sector_must_be_alpha(cls, value: str) -> str:
        """Ensures the sector contains only alphabetic characters."""
        cleaned = value.strip().lower()
        if not cleaned.isalpha():
            raise ValueError(
                f"Sector '{value}' must contain only alphabetic characters (no spaces, digits, or symbols)."
            )
        return cleaned

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"sector": "pharma"},
                {"sector": "technology"},
                {"sector": "energy"},
            ]
        }
    }
