"""
Data Collector Service — Fetches real-time market/news data for a given sector.

Strategy:
  1. Primary  : DuckDuckGo HTML search (no API key required)
  2. Fallback : GNews public RSS feed for broad coverage
  3. Fallback : Static placeholder if both sources fail

All network calls use httpx async client with a strict 5-second timeout.
"""

import logging
import re
from typing import List, Dict, Any

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# ─── Constants ────────────────────────────────────────────────────────────────
DDGO_URL = "https://html.duckduckgo.com/html/"
GNEWS_RSS = "https://gnews.io/api/v4/search"   # used in RSS fallback
TIMEOUT = httpx.Timeout(5.0, connect=3.0)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
}

MAX_RESULTS = 10


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _clean_text(raw: str) -> str:
    """Strip HTML tags, collapse whitespace, drop stray special chars."""
    no_tags = re.sub(r"<[^>]+>", "", raw)
    clean = re.sub(r"\s+", " ", no_tags).strip()
    # Remove ad/tracking noise strings
    clean = re.sub(r"(Ad·|Sponsored|More results)", "", clean)
    return clean


def _deduplicate(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate titles (case-insensitive)."""
    seen: set[str] = set()
    unique = []
    for item in items:
        key = item.get("title", "").lower()
        if key and key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


# ─── Primary Source: DuckDuckGo HTML ──────────────────────────────────────────

async def _fetch_from_duckduckgo(sector: str) -> List[Dict[str, Any]]:
    """
    POST to DuckDuckGo HTML endpoint and scrape result titles + snippets.
    Returns a list of dicts: {"title": str, "snippet": str, "link": str}
    """
    query = f"{sector} sector India market trends news 2026"
    logger.info(f"[DuckDuckGo] Fetching query: '{query}'")

    async with httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS, follow_redirects=True) as client:
        response = await client.post(DDGO_URL, data={"q": query, "kl": "in-en"})

    logger.info(f"[DuckDuckGo] Status: {response.status_code}")
    if response.status_code != 200:
        logger.warning(f"[DuckDuckGo] Unexpected status {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results: List[Dict[str, Any]] = []

    for result in soup.find_all("a", class_="result__a", limit=MAX_RESULTS):
        title = _clean_text(result.get_text())
        link = result.get("href")

        if title and link:
            results.append({
                "title": title,
                "link": link
            })

    logger.info(f"[DuckDuckGo] Scraped {len(results)} raw results")
    return results


# ─── Fallback Source: Google News RSS (no key required) ───────────────────────

async def _fetch_from_google_news_rss(sector: str) -> List[Dict[str, Any]]:
    """
    Fetch Google News RSS feed — completely free, no API key.
    """
    encoded = sector.replace(" ", "+")
    rss_url = (
        f"https://news.google.com/rss/search"
        f"?q={encoded}+india+market+news&hl=en-IN&gl=IN&ceid=IN:en"
    )
    logger.info(f"[GoogleRSS] Fetching: {rss_url}")

    async with httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS, follow_redirects=True) as client:
        response = await client.get(rss_url)

    if response.status_code != 200:
        logger.warning(f"[GoogleRSS] Unexpected status {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "xml")
    items = soup.find_all("item", limit=MAX_RESULTS + 5)
    results: List[Dict[str, Any]] = []

    for item in items:
        title = _clean_text(item.find("title").get_text()) if item.find("title") else ""
        link = item.find("link").get_text(strip=True) if item.find("link") else ""
        
        if title and link:
            results.append({"title": title, "link": link})

    logger.info(f"[GoogleRSS] Fetched {len(results)} items")
    return results


# ─── Public API ───────────────────────────────────────────────────────────────

async def fetch_sector_data(sector: str) -> List[Dict[str, Any]]:
    """
    Public function consumed by the /analyze/{sector} endpoint.
    Combines results from DuckDuckGo and Google News RSS.
    """
    all_results = []

    # --- Attempt 1: DuckDuckGo ---
    try:
        ddg_results = await _fetch_from_duckduckgo(sector)
        if ddg_results:
            all_results.extend(ddg_results)
    except Exception as exc:
        logger.error(f"[DuckDuckGo] Error: {exc}")

    # --- Attempt 2: Google News RSS (Always try for better coverage) ---
    try:
        gn_results = await _fetch_from_google_news_rss(sector)
        if gn_results:
            # Avoid exact duplicates
            existing_links = {item['link'] for item in all_results}
            for item in gn_results:
                if item['link'] not in existing_links:
                    all_results.append(item)
    except Exception as exc:
        logger.error(f"[GoogleRSS] Error: {exc}")

    # --- Fallback if both fail ---
    if not all_results:
        logger.warning(f"All sources failed for sector '{sector}'. Returning placeholder.")
        return [
            {
                "title": f"No recent news found for '{sector}' sector - Analysis based on general market knowledge.",
                "link": "https://news.google.com",
            }
        ]

    # Deduplicate and cap
    final = _deduplicate(all_results)[:MAX_RESULTS]
    logger.info(f"Returning {len(final)} results for sector '{sector}'")
    return final
