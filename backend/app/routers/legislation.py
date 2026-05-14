"""
JIAPI - Legislation Router
Post-2023 and Pre-2023 APIs
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import Optional, List
from datetime import date

from app.core.database import get_db
from app.models.legislation import Legislation, Section, LegislationType, EraEnum
from app.schemas.legislation import (
    LegislationCreate, LegislationUpdate, LegislationResponse, LegislationDetailResponse,
    SectionCreate, SectionUpdate, SectionResponse, SectionDetailResponse,
    SectionPointInTimeRequest, SectionDiffRequest, SectionDiffResponse,
    PaginatedResponse,
)

router = APIRouter()


# ==================== POST-2023 LEGISLATION ====================

@router.get("/post2023/legislations", response_model=PaginatedResponse)
async def list_post2023_legislations(
    legislation_type: Optional[LegislationType] = None,
    year: Optional[int] = None,
    status: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Legislation).where(Legislation.era == EraEnum.POST_2023)

    if legislation_type:
        query = query.where(Legislation.legislation_type == legislation_type)
    if year:
        query = query.where(Legislation.year == year)
    if status:
        query = query.where(Legislation.status == status)
    if tags:
        for tag in tags:
            query = query.where(Legislation.tags.contains([tag]))
    if search:
        query = query.where(
            or_(
                Legislation.title_en.ilike(f"%{search}%"),
                Legislation.title_bn.ilike(f"%{search}%"),
                Legislation.keywords.contains([search]),
            )
        )

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    # Paginate
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(Legislation.effective_date.desc())

    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
        items=[LegislationResponse.model_validate(item) for item in items],
    )


@router.get("/post2023/legislations/{legislation_id}", response_model=LegislationDetailResponse)
async def get_post2023_legislation(
    legislation_id: str,
    db: AsyncSession = Depends(get_db),
):
    query = select(Legislation).where(
        and_(Legislation.id == legislation_id, Legislation.era == EraEnum.POST_2023)
    )
    result = await db.execute(query)
    legislation = result.scalar_one_or_none()

    if not legislation:
        raise HTTPException(status_code=404, detail="Legislation not found")

    return LegislationDetailResponse.model_validate(legislation)


@router.post("/post2023/legislations", response_model=LegislationResponse, status_code=status.HTTP_201_CREATED)
async def create_post2023_legislation(
    data: LegislationCreate,
    db: AsyncSession = Depends(get_db),
):
    legislation = Legislation(**data.model_dump(), era=EraEnum.POST_2023)
    db.add(legislation)
    await db.commit()
    await db.refresh(legislation)
    return LegislationResponse.model_validate(legislation)


# ==================== PRE-2023 LEGISLATION ====================

@router.get("/pre2023/legislations", response_model=PaginatedResponse)
async def list_pre2023_legislations(
    legislation_type: Optional[LegislationType] = None,
    year: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Legislation).where(Legislation.era == EraEnum.PRE_2023)

    if legislation_type:
        query = query.where(Legislation.legislation_type == legislation_type)
    if year:
        query = query.where(Legislation.year == year)
    if status:
        query = query.where(Legislation.status == status)
    if search:
        query = query.where(
            or_(
                Legislation.title_en.ilike(f"%{search}%"),
                Legislation.title_bn.ilike(f"%{search}%"),
            )
        )

    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(Legislation.year.desc())

    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
        items=[LegislationResponse.model_validate(item) for item in items],
    )


@router.get("/pre2023/legislations/{legislation_id}", response_model=LegislationDetailResponse)
async def get_pre2023_legislation(
    legislation_id: str,
    db: AsyncSession = Depends(get_db),
):
    query = select(Legislation).where(
        and_(Legislation.id == legislation_id, Legislation.era == EraEnum.PRE_2023)
    )
    result = await db.execute(query)
    legislation = result.scalar_one_or_none()

    if not legislation:
        raise HTTPException(status_code=404, detail="Legislation not found")

    return LegislationDetailResponse.model_validate(legislation)


# ==================== SECTIONS ====================

@router.get("/legislations/{legislation_id}/sections", response_model=PaginatedResponse)
async def list_sections(
    legislation_id: str,
    level: Optional[int] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Section).where(Section.legislation_id == legislation_id)

    if level is not None:
        query = query.where(Section.level == level)
    if search:
        query = query.where(
            or_(
                Section.section_number.ilike(f"%{search}%"),
                Section.section_title_en.ilike(f"%{search}%"),
                Section.text_current.ilike(f"%{search}%"),
            )
        )

    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(Section.section_number)

    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
        items=[SectionResponse.model_validate(item) for item in items],
    )


@router.get("/sections/{section_id}", response_model=SectionDetailResponse)
async def get_section(
    section_id: str,
    db: AsyncSession = Depends(get_db),
):
    query = select(Section).where(Section.id == section_id)
    result = await db.execute(query)
    section = result.scalar_one_or_none()

    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    return SectionDetailResponse.model_validate(section)


@router.get("/sections/{section_id}/point-in-time")
async def get_section_point_in_time(
    section_id: str,
    as_of: date = Query(..., description="Date to view section as of"),
    db: AsyncSession = Depends(get_db),
):
    from app.services.amendment import AmendmentService

    service = AmendmentService(db)
    result = await service.get_section_at_date(section_id, as_of)

    if not result:
        raise HTTPException(status_code=404, detail="Section not found")

    return result


@router.get("/sections/{section_id}/diff", response_model=SectionDiffResponse)
async def get_section_diff(
    section_id: str,
    from_date: date = Query(..., description="Start date"),
    to_date: date = Query(..., description="End date"),
    db: AsyncSession = Depends(get_db),
):
    from app.services.amendment import AmendmentService

    service = AmendmentService(db)
    result = await service.get_section_diff(section_id, from_date, to_date)

    if not result:
        raise HTTPException(status_code=404, detail="Section not found")

    return result
