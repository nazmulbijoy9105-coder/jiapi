"""
JIAPI - Amendment Router
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional, List
from datetime import date, datetime

from app.core.database import get_db
from app.models.amendment import Amendment, ChangeType
from app.schemas.amendment import (
    AmendmentCreate, AmendmentUpdate, AmendmentResponse, AmendmentFeedResponse, AmendmentFeedItem,
)

router = APIRouter()


@router.get("/amendments", response_model=list)
async def list_amendments(
    change_type: Optional[ChangeType] = None,
    target_legislation_id: Optional[str] = None,
    target_section_id: Optional[str] = None,
    is_applied: Optional[str] = None,
    effective_from: Optional[date] = None,
    effective_to: Optional[date] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Amendment)

    if change_type:
        query = query.where(Amendment.change_type == change_type)
    if target_legislation_id:
        query = query.where(Amendment.target_legislation_id == target_legislation_id)
    if target_section_id:
        query = query.where(Amendment.target_section_id == target_section_id)
    if is_applied:
        query = query.where(Amendment.is_applied == is_applied)
    if effective_from:
        query = query.where(Amendment.effective_date >= effective_from)
    if effective_to:
        query = query.where(Amendment.effective_date <= effective_to)

    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(desc(Amendment.effective_date))

    result = await db.execute(query)
    items = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "items": [AmendmentResponse.model_validate(item) for item in items],
    }


@router.get("/amendments/feed", response_model=AmendmentFeedResponse)
async def get_amendment_feed(
    limit: int = Query(20, ge=1, le=100),
    since: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Amendment).where(Amendment.is_applied == "applied")

    if since:
        query = query.where(Amendment.created_at >= since)

    query = query.order_by(desc(Amendment.created_at)).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()

    feed_items = []
    for item in items:
        feed_items.append(AmendmentFeedItem(
            id=item.id,
            change_type=item.change_type,
            target_legislation_title=item.target_legislation.title_en if item.target_legislation else "",
            target_section_number=item.section.section_number if item.section else None,
            effective_date=item.effective_date,
            amendment_summary=item.amendment_summary,
            created_at=str(item.created_at),
        ))

    return AmendmentFeedResponse(
        total=len(feed_items),
        items=feed_items,
        last_updated=datetime.utcnow().isoformat(),
    )


@router.post("/amendments", response_model=AmendmentResponse, status_code=status.HTTP_201_CREATED)
async def create_amendment(
    data: AmendmentCreate,
    db: AsyncSession = Depends(get_db),
):
    amendment = Amendment(**data.model_dump())
    db.add(amendment)
    await db.commit()
    await db.refresh(amendment)
    return AmendmentResponse.model_validate(amendment)


@router.get("/amendments/{amendment_id}", response_model=AmendmentResponse)
async def get_amendment(
    amendment_id: str,
    db: AsyncSession = Depends(get_db),
):
    query = select(Amendment).where(Amendment.id == amendment_id)
    result = await db.execute(query)
    amendment = result.scalar_one_or_none()

    if not amendment:
        raise HTTPException(status_code=404, detail="Amendment not found")

    return AmendmentResponse.model_validate(amendment)


@router.patch("/amendments/{amendment_id}/apply")
async def apply_amendment(
    amendment_id: str,
    db: AsyncSession = Depends(get_db),
):
    from app.services.amendment import AmendmentService

    service = AmendmentService(db)
    result = await service.apply_amendment(amendment_id)

    if not result:
        raise HTTPException(status_code=404, detail="Amendment not found")

    return {"status": "success", "message": "Amendment applied", "amendment_id": amendment_id}
