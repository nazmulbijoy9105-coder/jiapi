"""Circular Letters (প্রজ্ঞাপন) Router"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from typing import Optional
from datetime import datetime
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_api_key, get_optional_api_key
from app.models import Circular
from app.schemas import CircularResponse, PaginatedResponse

router = APIRouter()


@router.get("/circulars", response_model=PaginatedResponse)
async def list_circulars(
    category: Optional[str] = None,
    sub_category: Optional[str] = None,
    status: Optional[str] = "active",
    year: Optional[int] = None,
    search: Optional[str] = None,
    issued_by: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    api_key: dict = Depends(get_optional_api_key),
):
    """List all NBR circular letters"""
    query = select(Circular)

    if category:
        query = query.where(Circular.category == category)
    if sub_category:
        query = query.where(Circular.sub_category == sub_category)
    if status:
        query = query.where(Circular.status == status)
    if year:
        query = query.where(func.extract('year', Circular.circular_date) == year)
    if search:
        query = query.where(
            or_(
                Circular.subject.ilike(f"%{search}%"),
                Circular.content_en.ilike(f"%{search}%"),
                Circular.content_bn.ilike(f"%{search}%"),
            )
        )
    if issued_by:
        query = query.where(Circular.issued_by.ilike(f"%{issued_by}%"))

    query = query.order_by(Circular.circular_date.desc())

    result = await db.execute(query)
    items = result.scalars().all()
    total = len(items)

    start = (page - 1) * page_size
    end = start + page_size

    return {
        "success": True,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "results": [CircularResponse.model_validate(item) for item in items[start:end]],
    }


@router.get("/circulars/{circular_id}", response_model=CircularResponse)
async def get_circular(
    circular_id: UUID,
    db: AsyncSession = Depends(get_db),
    api_key: dict = Depends(get_current_api_key),
):
    """Get specific circular by ID"""
    result = await db.execute(select(Circular).where(Circular.id == circular_id))
    circular = result.scalar_one_or_none()

    if not circular:
        raise HTTPException(status_code=404, detail="Circular not found")

    return CircularResponse.model_validate(circular)
