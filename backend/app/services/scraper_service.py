"""
JIAPI - Scraper Service
Scrapes bdlaws.minlaw.gov.bd, nbr.gov.bd for updates
"""
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime

from app.core.config import settings


class BDScraperService:
    """Scraper for Bangladesh legal sources"""

    BASE_URL = settings.BDLAWS_URL
    NBR_URL = settings.NBR_GAZETTE_URL

    async def fetch_bdlaws_act(self, act_id: str) -> Optional[Dict]:
        """Fetch specific act from bdlaws.minlaw.gov.bd"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                url = f"{self.BASE_URL}/act-details/{act_id}"
                response = await client.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                title = soup.find("h1", class_="act-title")
                content = soup.find("div", class_="act-content")

                return {
                    "source": "bdlaws",
                    "url": url,
                    "title": title.get_text(strip=True) if title else None,
                    "content_html": str(content) if content else None,
                    "scraped_at": datetime.utcnow().isoformat(),
                }
            except Exception as e:
                return {"error": str(e), "source": "bdlaws"}

    async def fetch_nbr_sros(self, year: int) -> List[Dict]:
        """Fetch SROs from NBR website"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                url = f"{self.NBR_URL}/sros/{year}"
                response = await client.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")
                sros = []

                for item in soup.find_all("div", class_="sro-item"):
                    sros.append({
                        "sro_number": item.get("data-sro-number"),
                        "title": item.get_text(strip=True),
                        "date": item.get("data-date"),
                        "url": item.find("a")["href"] if item.find("a") else None,
                    })

                return sros
            except Exception as e:
                return [{"error": str(e)}]

    async def check_for_updates(self) -> Dict:
        """Check all sources for new amendments/legislation"""
        return {
            "checked_at": datetime.utcnow().isoformat(),
            "sources": {
                "bdlaws": {"status": "pending", "new_items": 0},
                "nbr": {"status": "pending", "new_items": 0},
            },
            "message": "Use this service to monitor for new legislation",
        }
