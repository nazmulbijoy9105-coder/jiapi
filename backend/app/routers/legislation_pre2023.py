"""
JIAPI - Pre-2023 Legislation Router
ITO 1984, historical Finance Acts, SROs, GOs, Circulars, DTAAs
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, List
from datetime import date

from app.core.database import get_db
from app.core.security import get_current_active_user, RoleChecker
from app.models.legislation import Legislation, ContentBlock, Amendment, EraEnum, LegislationType
from app.models.user import User, UserRole
from app.schemas.legislation import (
    LegislationCreate, LegislationUpdate, LegislationResponse, LegislationDetail,
    LegislationBrief, ContentBlockResponse,
    PointInTimeQuery, PointInTimeResponse,
    DiffQuery, DiffResponse, AmendmentResponse
)

router = APIRouter()
editor_checker = RoleChecker([UserRole.ADMIN, UserRole.EDITOR, UserRole.VERIFIER])


# ============== ITO 1984 ==============

@router.get("/acts/ito1984", response_model=LegislationDetail)
async def get_ito1984(
    as_of: Optional[date] = Query(None, description="Get law as it existed on this date"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get Income Tax Ordinance 1984 with all historical amendments (as last amended FY 2022-23)."""
    result = await db.execute(
        select(Legislation).where(
            and_(
                Legislation.legislation_type == LegislationType.INCOME_TAX_ACT,
                Legislation.year == 1984,
                Legislation.era == EraEnum.PRE_2023
            )
        )
    )
    legislation = result.scalar_one_or_none()

    if not legislation:
        raise HTTPException(status_code=404, detail="ITO 1984 not found")

    return legislation


@router.get("/acts/ito1984/sections/{section_number}", response_model=ContentBlockResponse)
async def get_ito1984_section(
    section_number: str,
    as_of: Optional[date] = Query(None, description="Point-in-time query"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific section of ITO 1984."""
    result = await db.execute(
        select(ContentBlock)
        .join(Legislation)
        .where(
            and_(
                Legislation.legislation_type == LegislationType.INCOME_TAX_ACT,
                Legislation.year == 1984,
                ContentBlock.numbering == section_number
            )
        )
    )
    block = result.scalar_one_or_none()

    if not block:
        raise HTTPException(status_code=404, detail=f"Section {section_number} not found")

    return block


# ============== Historical Finance Acts ==============

@router.get("/finance-acts", response_model=List[LegislationBrief])
async def list_historical_finance_acts(
    from_year: Optional[int] = Query(None, description="Start year"),
    to_year: Optional[int] = Query(None, description="End year"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List historical Finance Acts (1984-2023)."""
    query = select(Legislation).where(
        and_(
            Legislation.legislation_type == LegislationType.FINANCE_ACT,
            Legislation.era == EraEnum.PRE_2023
        )
    )
    if from_year:
        query = query.where(Legislation.year >= from_year)
    if to_year:
        query = query.where(Legislation.year <= to_year)

    query = query.order_by(Legislation.year.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/finance-acts/{finance_act_id}", response_model=LegislationDetail)
async def get_historical_finance_act(
    finance_act_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific historical Finance Act."""
    result = await db.execute(
        select(Legislation).where(
            and_(
                Legislation.id == finance_act_id,
                Legislation.legislation_type == LegislationType.FINANCE_ACT,
                Legislation.era == EraEnum.PRE_2023
            )
        )
    )
    legislation = result.scalar_one_or_none()

    if not legislation:
        raise HTTPException(status_code=404, detail="Finance Act not found")

    return legislation


# ============== Historical SROs ==============

@router.get("/sros", response_model=List[LegislationBrief])
async def list_historical_sros(
    year: Optional[int] = Query(None),
    sector: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List historical SROs still relevant for pending assessments."""
    query = select(Legislation).where(
        and_(
            Legislation.legislation_type == LegislationType.SRO,
            Legislation.era == EraEnum.PRE_2023
        )
    )
    if year:
        query = query.where(Legislation.year == year)

    query = query.order_by(Legislation.enactment_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/sros/{sro_id}", response_model=LegislationDetail)
async def get_historical_sro(
    sro_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific historical SRO."""
    result = await db.execute(
        select(Legislation).where(
            and_(
                Legislation.id == sro_id,
                Legislation.legislation_type == LegislationType.SRO,
                Legislation.era == EraEnum.PRE_2023
            )
        )
    )
    legislation = result.scalar_one_or_none()

    if not legislation:
        raise HTTPException(status_code=404, detail="SRO not found")

    return legislation


# ============== Historical GOs & Circulars ==============

@router.get("/general-orders", response_model=List[LegislationBrief])
async def list_historical_gos(
    year: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List historical NBR General Orders."""
    query = select(Legislation).where(
        and_(
            Legislation.legislation_type == LegislationType.GENERAL_ORDER,
            Legislation.era == EraEnum.PRE_2023
        )
    )
    if year:
        query = query.where(Legislation.year == year)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/circulars", response_model=List[LegislationBrief])
async def list_historical_circulars(
    year: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List historical NBR Circular Letters."""
    query = select(Legislation).where(
        and_(
            Legislation.legislation_type == LegislationType.CIRCULAR,
            Legislation.era == EraEnum.PRE_2023
        )
    )
    if year:
        query = query.where(Legislation.year == year)

    result = await db.execute(query)
    return result.scalars().all()


# ============== Historical DTAAs ==============

@router.get("/dtaas", response_model=List[dict])
async def list_historical_dtaas(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List pre-2023 DTAA treaty versions."""
    from app.models.case_law import DTAATreaty

    result = await db.execute(
        select(DTAATreaty).where(DTAATreaty.effective_date < date(2023, 6, 1))
    )
    treaties = result.scalars().all()

    return [
        {
            "id": t.id,
            "country_name": t.country_name,
            "country_code": t.country_code,
            "effective_date": t.effective_date,
        }
        for t in treaties
    ]


# ============== Point-in-Time & Diff ==============

@router.post("/point-in-time", response_model=PointInTimeResponse)
async def get_point_in_time(
    query: PointInTimeQuery,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get pre-2023 legislation as it existed on a specific date."""
    from app.services.amendment_engine import get_legislation_at_date
    return await get_legislation_at_date(db, query.legislation_id, query.as_of_date)


@router.post("/diff", response_model=DiffResponse)
async def get_diff(
    query: DiffQuery,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Compare pre-2023 legislation between two dates."""
    from app.services.amendment_engine import get_legislation_diff
    return await get_legislation_diff(db, query.legislation_id, query.from_date, query.to_date)


# ============== Amendment History ==============

@router.get("/amendments/history", response_model=List[AmendmentResponse])
async def get_amendment_history(
    legislation_id: Optional[str] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get amendment history for pre-2023 legislation."""
    query = select(Amendment).join(Legislation, Amendment.target_legislation_id == Legislation.id).where(
        Legislation.era == EraEnum.PRE_2023
    )
    if legislation_id:
        query = query.where(Amendment.target_legislation_id == legislation_id)
    if from_date:
        query = query.where(Amendment.effective_date >= from_date)
    if to_date:
        query = query.where(Amendment.effective_date <= to_date)

    query = query.order_by(Amendment.effective_date.desc())
    result = await db.execute(query)
    return result.scalars().all()
