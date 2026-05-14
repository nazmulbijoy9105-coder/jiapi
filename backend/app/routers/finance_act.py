"""Finance Act Router"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_api_key, get_optional_api_key
from app.models import FinanceAct
from app.schemas import FinanceActResponse, PaginatedResponse

router = APIRouter()


@router.get("/finance-acts", response_model=PaginatedResponse)
async def list_finance_acts(
    year: Optional[int] = None,
    status: Optional[str] = "active",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    api_key: dict = Depends(get_optional_api_key),
):
    """List all Finance Acts"""
    query = select(FinanceAct)

    if year:
        query = query.where(FinanceAct.act_year == year)
    if status:
        query = query.where(FinanceAct.status == status)

    query = query.order_by(FinanceAct.act_year.desc())

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
        "results": [FinanceActResponse.model_validate(item) for item in items[start:end]],
    }


@router.get("/finance-acts/{finance_act_id}", response_model=FinanceActResponse)
async def get_finance_act(
    finance_act_id: UUID,
    db: AsyncSession = Depends(get_db),
    api_key: dict = Depends(get_current_api_key),
):
    """Get specific Finance Act by ID"""
    result = await db.execute(select(FinanceAct).where(FinanceAct.id == finance_act_id))
    act = result.scalar_one_or_none()

    if not act:
        raise HTTPException(status_code=404, detail="Finance Act not found")

    return FinanceActResponse.model_validate(act)


@router.get("/finance-acts/year/{act_year}", response_model=FinanceActResponse)
async def get_finance_act_by_year(
    act_year: int,
    db: AsyncSession = Depends(get_db),
    api_key: dict = Depends(get_current_api_key),
):
    """Get Finance Act by year (e.g., 2024, 2025)"""
    result = await db.execute(
        select(FinanceAct).where(FinanceAct.act_year == act_year)
    )
    act = result.scalar_one_or_none()

    if not act:
        raise HTTPException(status_code=404, detail=f"Finance Act {act_year} not found")

    return FinanceActResponse.model_validate(act)


@router.get("/finance-acts/{finance_act_id}/tax-rates")
async def get_tax_rates(
    finance_act_id: UUID,
    db: AsyncSession = Depends(get_db),
    api_key: dict = Depends(get_current_api_key),
):
    """Get tax rates from a specific Finance Act"""
    result = await db.execute(
        select(FinanceAct).where(FinanceAct.id == finance_act_id)
    )
    act = result.scalar_one_or_none()

    if not act:
        raise HTTPException(status_code=404, detail="Finance Act not found")

    return {
        "success": True,
        "act_year": act.act_year,
        "tax_rates": {
            "individual": act.tax_rates_individual,
            "corporate": act.tax_rates_corporate,
            "other": act.tax_rates_other,
        },
    }
