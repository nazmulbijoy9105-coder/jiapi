"""
JIAPI - Post-2023 Legislation Router
ITA 2023, ITR 2024, Finance Acts, SROs, GOs, Circulars, DTAAs, TP Regs, BEPS
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from typing import Optional, List
from datetime import date

from app.core.database import get_db
from app.core.security import get_current_active_user, RoleChecker
from app.models.legislation import Legislation, ContentBlock, Amendment, EraEnum, LegislationType, LegislationStatus
from app.models.user import User, UserRole
from app.schemas.legislation import (
    LegislationCreate, LegislationUpdate, LegislationResponse, LegislationDetail,
    LegislationBrief, LegislationSearchQuery, LegislationSearchResult,
    ContentBlockResponse, PointInTimeQuery, PointInTimeResponse,
    DiffQuery, DiffResponse, AmendmentCreate, AmendmentResponse
)

router = APIRouter()
editor_checker = RoleChecker([UserRole.ADMIN, UserRole.EDITOR, UserRole.VERIFIER])


# ============== ITA 2023 ==============

@router.get("/acts/ita2023", response_model=LegislationDetail)
async def get_ita2023(
    as_of: Optional[date] = Query(None, description="Get law as it existed on this date"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get Income Tax Act 2023 with all current amendments applied."""
    result = await db.execute(
        select(Legislation).where(
            and_(
                Legislation.legislation_type == LegislationType.INCOME_TAX_ACT,
                Legislation.year == 2023,
                Legislation.era == EraEnum.POST_2023
            )
        )
    )
    legislation = result.scalar_one_or_none()

    if not legislation:
        raise HTTPException(status_code=404, detail="ITA 2023 not found")

    return legislation


@router.get("/acts/ita2023/sections/{section_number}", response_model=ContentBlockResponse)
async def get_ita2023_section(
    section_number: str,
    as_of: Optional[date] = Query(None, description="Point-in-time query"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific section of ITA 2023."""
    result = await db.execute(
        select(ContentBlock)
        .join(Legislation)
        .where(
            and_(
                Legislation.legislation_type == LegislationType.INCOME_TAX_ACT,
                Legislation.year == 2023,
                ContentBlock.numbering == section_number
            )
        )
    )
    block = result.scalar_one_or_none()

    if not block:
        raise HTTPException(status_code=404, detail=f"Section {section_number} not found")

    return block


# ============== ITR 2024 ==============

@router.get("/rules/itr2024", response_model=LegislationDetail)
async def get_itr2024(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get Income Tax Rules 2024."""
    result = await db.execute(
        select(Legislation).where(
            and_(
                Legislation.legislation_type == LegislationType.INCOME_TAX_RULES,
                Legislation.year == 2024,
                Legislation.era == EraEnum.POST_2023
            )
        )
    )
    legislation = result.scalar_one_or_none()

    if not legislation:
        raise HTTPException(status_code=404, detail="ITR 2024 not found")

    return legislation


# ============== Finance Acts ==============

@router.get("/finance-acts", response_model=List[LegislationBrief])
async def list_finance_acts(
    year: Optional[int] = Query(None, description="Filter by year"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all Finance Acts (annual budget laws)."""
    query = select(Legislation).where(
        and_(
            Legislation.legislation_type == LegislationType.FINANCE_ACT,
            Legislation.era == EraEnum.POST_2023
        )
    )
    if year:
        query = query.where(Legislation.year == year)

    query = query.order_by(Legislation.year.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/finance-acts/{finance_act_id}", response_model=LegislationDetail)
async def get_finance_act(
    finance_act_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific Finance Act with all amendments."""
    result = await db.execute(
        select(Legislation).where(
            and_(
                Legislation.id == finance_act_id,
                Legislation.legislation_type == LegislationType.FINANCE_ACT
            )
        )
    )
    legislation = result.scalar_one_or_none()

    if not legislation:
        raise HTTPException(status_code=404, detail="Finance Act not found")

    return legislation


# ============== SROs ==============

@router.get("/sros", response_model=List[LegislationBrief])
async def list_sros(
    sector: Optional[str] = Query(None, description="Filter by sector"),
    year: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all Statutory Regulatory Orders (SROs)."""
    query = select(Legislation).where(
        and_(
            Legislation.legislation_type == LegislationType.SRO,
            Legislation.era == EraEnum.POST_2023
        )
    )
    if year:
        query = query.where(Legislation.year == year)
    if status:
        query = query.where(Legislation.status == status)

    query = query.order_by(Legislation.enactment_date.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/sros/{sro_id}", response_model=LegislationDetail)
async def get_sro(
    sro_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific SRO."""
    result = await db.execute(
        select(Legislation).where(
            and_(Legislation.id == sro_id, Legislation.legislation_type == LegislationType.SRO)
        )
    )
    legislation = result.scalar_one_or_none()

    if not legislation:
        raise HTTPException(status_code=404, detail="SRO not found")

    return legislation


# ============== General Orders ==============

@router.get("/general-orders", response_model=List[LegislationBrief])
async def list_general_orders(
    year: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List NBR General Orders (GOs)."""
    query = select(Legislation).where(
        and_(
            Legislation.legislation_type == LegislationType.GENERAL_ORDER,
            Legislation.era == EraEnum.POST_2023
        )
    )
    if year:
        query = query.where(Legislation.year == year)

    result = await db.execute(query)
    return result.scalars().all()


# ============== Circulars ==============

@router.get("/circulars", response_model=List[LegislationBrief])
async def list_circulars(
    year: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List NBR Circular Letters (প্রজ্ঞাপন)."""
    query = select(Legislation).where(
        and_(
            Legislation.legislation_type == LegislationType.CIRCULAR,
            Legislation.era == EraEnum.POST_2023
        )
    )
    if year:
        query = query.where(Legislation.year == year)

    result = await db.execute(query)
    return result.scalars().all()


# ============== Cross-Reference: VAT Act 2012 ==============

@router.get("/cross-reference/vat2012", response_model=List[LegislationBrief])
async def get_vat2012_references(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get relevant VAT Act 2012 sections for business income cross-reference."""
    result = await db.execute(
        select(Legislation).where(
            and_(
                Legislation.legislation_type == LegislationType.VAT_ACT,
                Legislation.era == EraEnum.POST_2023
            )
        )
    )
    return result.scalars().all()


# ============== Cross-Reference: Customs Act 1969 ==============

@router.get("/cross-reference/customs1969", response_model=List[LegislationBrief])
async def get_customs1969_references(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get Customs Act 1969 provisions for import income adjustments."""
    result = await db.execute(
        select(Legislation).where(
            and_(
                Legislation.legislation_type == LegislationType.CUSTOMS_ACT,
                Legislation.era == EraEnum.POST_2023
            )
        )
    )
    return result.scalars().all()


# ============== DTAAs ==============

@router.get("/dtaas", response_model=List[dict])
async def list_dtaas(
    active_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all Double Taxation Avoidance Agreements (~35 treaties)."""
    from app.models.case_law import DTAATreaty

    query = select(DTAATreaty)
    if active_only:
        query = query.where(DTAATreaty.is_active == True)

    query = query.order_by(DTAATreaty.country_name)
    result = await db.execute(query)
    treaties = result.scalars().all()

    return [
        {
            "id": t.id,
            "country_name": t.country_name,
            "country_code": t.country_code,
            "signed_date": t.signed_date,
            "effective_date": t.effective_date,
            "is_active": t.is_active,
            "is_limited": t.is_limited,
        }
        for t in treaties
    ]


@router.get("/dtaas/{country_code}", response_model=dict)
async def get_dtaa(
    country_code: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get specific DTAA by country code."""
    from app.models.case_law import DTAATreaty

    result = await db.execute(
        select(DTAATreaty).where(DTAATreaty.country_code == country_code.upper())
    )
    treaty = result.scalar_one_or_none()

    if not treaty:
        raise HTTPException(status_code=404, detail=f"DTAA for {country_code} not found")

    return treaty


# ============== BEPS ==============

@router.get("/beps", response_model=List[dict])
async def list_beps(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List OECD BEPS framework references."""
    from app.models.case_law import BEPSReference

    result = await db.execute(select(BEPSReference).order_by(BEPSReference.action_number))
    references = result.scalars().all()

    return [
        {
            "id": r.id,
            "action_number": r.action_number,
            "action_title": r.action_title,
            "bangladesh_adoption_status": r.bangladesh_adoption_status,
        }
        for r in references
    ]


# ============== TP Regulations ==============

@router.get("/tp-regulations", response_model=LegislationDetail)
async def get_tp_regulations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get Transfer Pricing Regulations under ITA 2023 (international transactions chapter)."""
    result = await db.execute(
        select(Legislation).where(
            and_(
                Legislation.legislation_type == LegislationType.TP_REGULATION,
                Legislation.era == EraEnum.POST_2023
            )
        )
    )
    legislation = result.scalar_one_or_none()

    if not legislation:
        raise HTTPException(status_code=404, detail="TP Regulations not found")

    return legislation


# ============== Compliance Manual ==============

@router.get("/compliance-manual", response_model=LegislationDetail)
async def get_compliance_manual(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get NBR Tax Compliance Manual."""
    result = await db.execute(
        select(Legislation).where(
            and_(
                Legislation.legislation_type == LegislationType.COMPLIANCE_MANUAL,
                Legislation.era == EraEnum.POST_2023
            )
        )
    )
    legislation = result.scalar_one_or_none()

    if not legislation:
        raise HTTPException(status_code=404, detail="Compliance Manual not found")

    return legislation


# ============== Amendment Feed ==============

@router.get("/amendments/feed", response_model=List[AmendmentResponse])
async def get_amendment_feed(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get latest amendments feed (RSS/JSON)."""
    result = await db.execute(
        select(Amendment)
        .join(Legislation, Amendment.target_legislation_id == Legislation.id)
        .where(Legislation.era == EraEnum.POST_2023)
        .order_by(Amendment.effective_date.desc())
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()


# ============== Point-in-Time & Diff ==============

@router.post("/point-in-time", response_model=PointInTimeResponse)
async def get_point_in_time(
    query: PointInTimeQuery,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get legislation as it existed on a specific date."""
    from app.services.amendment_engine import get_legislation_at_date
    return await get_legislation_at_date(db, query.legislation_id, query.as_of_date)


@router.post("/diff", response_model=DiffResponse)
async def get_diff(
    query: DiffQuery,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Compare legislation between two dates."""
    from app.services.amendment_engine import get_legislation_diff
    return await get_legislation_diff(db, query.legislation_id, query.from_date, query.to_date)


# ============== Admin: Create/Update Legislation ==============

@router.post("/legislation", response_model=LegislationResponse, status_code=status.HTTP_201_CREATED)
async def create_legislation(
    data: LegislationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(editor_checker)
):
    """Create new legislation (Admin/Editor only)."""
    legislation = Legislation(**data.model_dump(exclude={"content_blocks"}))
    db.add(legislation)
    await db.commit()
    await db.refresh(legislation)
    return legislation


@router.put("/legislation/{legislation_id}", response_model=LegislationResponse)
async def update_legislation(
    legislation_id: str,
    data: LegislationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(editor_checker)
):
    """Update legislation (Admin/Editor only)."""
    result = await db.execute(select(Legislation).where(Legislation.id == legislation_id))
    legislation = result.scalar_one_or_none()

    if not legislation:
        raise HTTPException(status_code=404, detail="Legislation not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(legislation, field, value)

    await db.commit()
    await db.refresh(legislation)
    return legislation
