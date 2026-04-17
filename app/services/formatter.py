import re
import logging
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

def extract_section(text, keywords):
    for keyword in keywords:
        pattern = rf"{keyword}[:\-\n](.*?)(?=\n\d+\.|\Z|##|#)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
    return "Data not available"

def format_to_markdown(sector, analysis, keywords, sentiment, confidence, sources, timestamp):
    """
    Parses AI analysis results into a professional Markdown report with advanced metrics.
    """
    try:
        logger.info(f"Formatting markdown for sector: {sector}")

        # Clean text before parsing
        analysis = analysis.replace("*", "").strip()

        # Extract sections
        trends = extract_section(analysis, ["Market Trends", "Trends"])
        opportunities = extract_section(analysis, ["Opportunities"])
        risks = extract_section(analysis, ["Risks", "Challenges", "Risk"])

        # Helper to convert text → bullet points
        def to_bullets(text):
            if text == "Data not available":
                return text
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            return "\n".join([f"- {line}" if not line.startswith("-") else line for line in lines])

        markdown = f"""# {sector.capitalize()} Sector - Market Analysis

Generated on: {timestamp}

## 📈 Market Trends
{to_bullets(trends)}

## 💡 Key Opportunities
{to_bullets(opportunities)}

## ⚠️ Risks and Challenges
{to_bullets(risks)}

## 📊 Market Sentiment
{sentiment}

## 🔑 Trending Keywords
{"".join([f"- {k}\n" for k in keywords])}

## 📚 Sources
{"".join([f"- {s}\n" for s in sources])}

## ✅ Confidence Score
{confidence}%
"""
        return markdown.strip()

    except Exception as e:
        logger.error(f"Formatting error: {str(e)}")
        # Fallback
        markdown = f"""# {sector.capitalize()} Sector - Market Analysis

Generated on: {timestamp}

## AI Analysis
{analysis}

## 📊 Market Sentiment
{sentiment}

## ✅ Confidence Score
{confidence}%
"""
        return markdown.strip()
