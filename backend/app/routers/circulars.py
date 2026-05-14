"""
JIAPI - Circulars Router
NBR Circular Letters (প্রজ্ঞাপন)
"""
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import date
from app.schemas import CircularResponse
from app.core.security import get_current_user

router = APIRouter()


@router.get("/circulars")
async def list_circulars(
    era: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    wing: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    is_active: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """List NBR circular letters with filters"""
    return {
        "total": 2,
        "items": [
            {
                "id": "circ-001",
                "era": "post2023",
                "circular_number": "01/IT/2024",
                "circular_date": date(2024, 7, 15),
                "title_en": "Guidelines for Online Return Filing under ITA 2023",
                "title_bn": "আয়কর আইন ২০২৩ এর অধীনে অনলাইন রিটার্ন দাখিলের নির্দেশিকা",
                "issuing_wing": "Income Tax",
                "subject": "Online Return Filing",
                "description": "Step-by-step guidelines for filing returns through the e-TIN portal",
                "effective_date": date(2024, 7, 15),
                "is_active": True,
                "applicable_sections": ["178", "179"],
                "created_at": "2024-07-15T00:00:00",
                "updated_at": "2024-07-15T00:00:00"
            },
            {
                "id": "circ-002",
                "era": "post2023",
                "circular_number": "02/IT/2024",
                "circular_date": date(2024, 8, 20),
                "title_en": "Transfer Pricing Documentation Requirements",
                "title_bn": "ট্রান্সফার প্রাইসিং ডকুমেন্টেশন প্রয়োজনীয়তা",
                "issuing_wing": "Income Tax",
                "subject": "Transfer Pricing",
                "description": "Detailed documentation requirements for international transactions exceeding Tk. 3 crore",
                "effective_date": date(2024, 8, 20),
                "is_active": True,
                "applicable_sections": ["233", "234", "235"],
                "created_at": "2024-08-20T00:00:00",
                "updated_at": "2024-08-20T00:00:00"
            }
        ]
    }
