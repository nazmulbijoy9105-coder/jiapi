"""
JIAPI - Pre-2023 Legislation Router
ITO 1984, Finance Acts 1984-2023, SROs, Circulars
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from datetime import date
from app.schemas import LegislationResponse, ContentBlockResponse
from app.core.security import get_current_user

router = APIRouter()


@router.get("/acts/ito1984", response_model=LegislationResponse)
async def get_ito1984(current_user: dict = Depends(get_current_user)):
    """
    Get Income Tax Ordinance 1984 as last amended (FY 2022-23).

    Entirely superseded by ITA 2023 from July 1, 2023.
    """
    return {
        "id": "ito1984-primary",
        "era": "pre2023",
        "legislation_type": "act",
        "title_en": "Income Tax Ordinance, 1984",
        "title_bn": "আয়কর অধ্যাদেশ, ১৯৮৪",
        "short_title": "ITO 1984",
        "act_number": "Ordinance No. XXXVI of 1984",
        "year": 1984,
        "authority": "Parliament of Bangladesh",
        "effective_date": date(1984, 7, 1),
        "repeal_date": date(2023, 6, 30),
        "status": "repealed",
        "is_repealed": True,
        "preamble": """An Ordinance to consolidate and amend the law relating to income tax""",
        "total_sections": 0,
        "total_schedules": 0,
        "keywords": ["income tax", "ITO 1984", "historical", "repealed"],
        "created_at": "1984-07-01T00:00:00",
        "updated_at": "2023-06-30T00:00:00",
        "document_url": "https://bdlaws.minlaw.gov.bd/act-600.html"
    }


@router.get("/acts/ito1984/sections/{section_number}", response_model=ContentBlockResponse)
async def get_ito1984_section(
    section_number: str = Path(..., description="Section number (e.g., 30, 30(1))"),
    as_of: Optional[date] = Query(None, description="Get text as of specific date"),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific section of ITO 1984 with historical amendments"""
    return {
        "id": f"ito1984-sec-{section_number}",
        "legislation_id": "ito1984-primary",
        "block_type": "section",
        "numbering": section_number,
        "heading_en": f"Section {section_number} of ITO 1984",
        "text_original": f"Original text of Section {section_number} as enacted in 1984",
        "text_current": f"Text as last amended before repeal (June 30, 2023)",
        "effective_from": date(1984, 7, 1),
        "effective_to": date(2023, 6, 30),
        "display_order": int(section_number) if section_number.isdigit() else 0,
        "level": 0,
        "is_active": False,
        "is_repealed": True,
        "keywords": ["ITO 1984", "historical"]
    }


@router.get("/finance-acts", response_model=List[LegislationResponse])
async def list_finance_acts(
    year_from: Optional[int] = Query(None),
    year_to: Optional[int] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """
    List Finance Acts 1984-2023.

    These are the annual amendments to ITO 1984 before ITA 2023.
    """
    acts = []
    for year in range(1984, 2024):
        acts.append({
            "id": f"fa-{year}",
            "era": "pre2023",
            "legislation_type": "finance_act",
            "title_en": f"Finance Act, {year}",
            "short_title": f"FA {year}",
            "year": year,
            "authority": "Parliament of Bangladesh",
            "effective_date": date(year, 7, 1),
            "status": "superseded",
            "keywords": ["budget", "tax rates", "historical"],
            "created_at": f"{year}-06-01T00:00:00",
            "updated_at": f"{year}-06-01T00:00:00"
        })

    if year_from:
        acts = [a for a in acts if a["year"] >= year_from]
    if year_to:
        acts = [a for a in acts if a["year"] <= year_to]

    return acts


@router.get("/sros")
async def list_historical_sros(
    year: Optional[int] = Query(None),
    sector: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """List historical SROs (pre-2023) still relevant for pending assessments"""
    return {"message": "Historical SROs endpoint", "count": 0}


@router.get("/circulars")
async def list_historical_circulars(
    year: Optional[int] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """List historical circulars (pre-2023)"""
    return {"message": "Historical circulars endpoint", "count": 0}


@router.get("/dtaas")
async def list_historical_dtaas(current_user: dict = Depends(get_current_user)):
    """List DTAA versions before 2023 (some treaties updated post-2023)"""
    return {"message": "Historical DTAA versions", "count": 35}
