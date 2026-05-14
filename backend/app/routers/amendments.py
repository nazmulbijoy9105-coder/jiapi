"""
JIAPI - Amendments Router
Amendment tracking and diff engine
"""
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import date
from app.schemas import AmendmentResponse, AmendmentFeedItem
from app.core.security import get_current_user

router = APIRouter()


@router.get("/amendments")
async def list_amendments(
    legislation_id: Optional[str] = Query(None),
    section_number: Optional[str] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    is_applied: Optional[bool] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """
    List all amendments with filters.

    Track every change to legislation with source attribution.
    """
    return {
        "total": 2,
        "items": [
            {
                "id": "amd-001",
                "change_type": "substitute",
                "old_text": "General corporate tax rate: 30%",
                "new_text": "General corporate tax rate: 27.5%",
                "effective_date": date(2025, 7, 1),
                "description": "Finance Act 2025 reduced corporate tax rate",
                "change_summary": "Corporate tax rate reduced from 30% to 27.5%",
                "is_applied": True,
                "applied_at": "2025-07-01T00:00:00",
                "created_at": "2025-06-01T00:00:00"
            },
            {
                "id": "amd-002",
                "change_type": "insert",
                "new_text": "Minimum tax can be carried forward for 3 years",
                "effective_date": date(2025, 7, 1),
                "description": "Finance Act 2025 introduced minimum tax carry forward",
                "change_summary": "New provision: Minimum tax carry forward for 3 years",
                "is_applied": True,
                "applied_at": "2025-07-01T00:00:00",
                "created_at": "2025-06-01T00:00:00"
            }
        ]
    }


@router.get("/amendments/feed")
async def get_amendment_feed(
    limit: int = Query(20, ge=1, le=100),
    priority: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Get latest amendment feed for notifications"""
    return {
        "total": 3,
        "items": [
            {
                "id": "feed-001",
                "title": "Finance Act 2025 - Corporate Tax Rate Changes",
                "description": "General corporate tax rate reduced to 27.5% for non-listed entities",
                "affected_sections": ["Rate Schedule"],
                "priority": "high",
                "effective_date": date(2025, 7, 1),
                "created_at": "2025-06-01T00:00:00"
            },
            {
                "id": "feed-002",
                "title": "Finance Act 2025 - Minimum Tax Carry Forward",
                "description": "Minimum tax can now be carried forward for 3 years",
                "affected_sections": ["163", "70"],
                "priority": "high",
                "effective_date": date(2025, 7, 1),
                "created_at": "2025-06-01T00:00:00"
            },
            {
                "id": "feed-003",
                "title": "SRO 404-Law/2025 - Authentic English Text Published",
                "description": "Official authentic English text of ITA 2023 published by NBR",
                "affected_sections": ["All"],
                "priority": "normal",
                "effective_date": date(2025, 10, 8),
                "created_at": "2025-10-08T00:00:00"
            }
        ]
    }
