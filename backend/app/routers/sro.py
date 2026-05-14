"""SRO (Statutory Regulatory Orders) Router"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_api_key, get_optional_api_key
from app.models import SRO
from app.schemas import SROResponse, PaginatedResponse

router = APIRouter()


@router.get("/sros", response_model=PaginatedResponse)
async def list_sros(
    sro_type: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = "active",
    year: Optional[int] = None,
    search: Optional[str] = None,
    effective_from: Optional[datetime] = None,
    effective_to: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    api_key: dict = Depends(get_optional_api_key),
):
    """List all SROs with filters"""
    query = select(SRO)

    if sro_type:
        query = query.where(SRO.sro_type == sro_type)
    if category:
        query = query.where(SRO.category == category)
    if status:
        query = query.where(SRO.status == status)
    if year:
        query = query.where(func.extract('year', SRO.sro_date) == year)
    if search:
        query = query.where(
            or_(
                SRO.subject.ilike(f"%{search}%"),
                SRO.description.ilike(f"%{search}%"),
            )
        )
    if effective_from:
        query = query.where(SRO.effective_from >= effective_from)
    if effective_to:
        query = query.where(SRO.effective_from <= effective_to)

    query = query.order_by(SRO.sro_date.desc())

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
        "results": [SROResponse.model_validate(item) for item in items[start:end]],
    }


@router.get("/sros/{sro_id}", response_model=SROResponse)
async def get_sro(
    sro_id: UUID,
    db: AsyncSession = Depends(get_db),
    api_key: dict = Depends(get_current_api_key),
):
    """Get specific SRO by ID"""
    result = await db.execute(select(SRO).where(SRO.id == sro_id))
    sro = result.scalar_one_or_none()

    if not sro:
        raise HTTPException(status_code=404, detail="SRO not found")

    return SROResponse.model_validate(sro)


@router.get("/sros/categories")
async def get_sro_categories(
    db: AsyncSession = Depends(get_db),
    api_key: dict = Depends(get_optional_api_key),
):
    """Get all SRO categories and types for filtering"""
    cat_result = await db.execute(
        select(SRO.category, func.count(SRO.id)).group_by(SRO.category)
    )

    type_result = await db.execute(
        select(SRO.sro_type, func.count(SRO.id)).group_by(SRO.sro_type)
    )

    return {
        "success": True,
        "categories": {cat: count for cat, count in cat_result.all()},
        "types": {t: count for t, count in type_result.all()},
    }
