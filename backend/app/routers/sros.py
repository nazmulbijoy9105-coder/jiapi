"""
JIAPI - SROs Router
Statutory Regulatory Orders
"""
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import date
from app.schemas import SROResponse
from app.core.security import get_current_user

router = APIRouter()


@router.get("/sros")
async def list_sros(
    era: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    wing: Optional[str] = Query(None, description="Income Tax, VAT, Customs"),
    sector: Optional[str] = Query(None),
    is_active: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """List SROs with filters"""
    return {
        "total": 2,
        "items": [
            {
                "id": "sro-404-2025",
                "era": "post2023",
                "sro_number": "404-Law/2025",
                "sro_date": date(2025, 10, 8),
                "title_en": "Publication of Authentic English Text of Income Tax Act 2023",
                "title_bn": "আয়কর আইন ২০২৩ এর প্রামাণিক ইংরেজি পাঠ প্রকাশ",
                "issuing_authority": "National Board of Revenue",
                "wing": "Income Tax",
                "description": "Official authentic English text of ITA 2023 published by NBR",
                "effective_date": date(2025, 10, 8),
                "is_active": True,
                "applicable_sections": ["All"],
                "sectors": ["All"],
                "created_at": "2025-10-08T00:00:00",
                "updated_at": "2025-10-08T00:00:00",
                "document_url": "https://nbr.gov.bd/uploads/SRO/404-Law-2025.pdf"
            },
            {
                "id": "sro-123-2024",
                "era": "post2023",
                "sro_number": "123-IT/2024",
                "sro_date": date(2024, 3, 15),
                "title_en": "Exemption of Tax on Interest from Government Securities",
                "title_bn": "সরকারি সিকিউরিটিজের সুদের উপর কর ছাড়",
                "issuing_authority": "National Board of Revenue",
                "wing": "Income Tax",
                "description": "Exemption for individual taxpayers up to Tk. 50,000 interest income",
                "effective_date": date(2024, 4, 1),
                "is_active": True,
                "applicable_sections": ["19", "30"],
                "sectors": ["Individual"],
                "tax_rates": [{"rate": 0, "category": "interest on government securities", "limit": 50000}],
                "created_at": "2024-03-15T00:00:00",
                "updated_at": "2024-03-15T00:00:00"
            }
        ]
    }


@router.get("/sros/{sro_id}", response_model=SROResponse)
async def get_sro(
    sro_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get specific SRO with full text"""
    raise HTTPException(status_code=501, detail="Coming soon")
