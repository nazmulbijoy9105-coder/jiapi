"""
JIAPI - Case Law API Router
Appellate Division, High Court, Tax Appellate Tribunal
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from ..core.database import get_db
from ..services.case_law_service import CaseLawService
from ..schemas.case_law import (
    CaseLawCreate, CaseLawUpdate, CaseLawResponse, CaseLawDetailResponse,
    CaseLawSearchRequest, CaseLawSearchResponse,
    CitationCheckRequest, CitationCheckResponse
)

router = APIRouter(prefix="/caselaw", tags=["Case Law"])


# ============== Appellate Division ==============

@router.get("/appellate-division", response_model=List[CaseLawResponse])
async def list_ad_judgments(
    year: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List Appellate Division tax judgments"""
    service = CaseLawService(db)
    return await service.list_cases("appellate_division", year, skip, limit)


@router.get("/appellate-division/{case_id}", response_model=CaseLawDetailResponse)
async def get_ad_judgment(case_id: str, db: AsyncSession = Depends(get_db)):
    """Get specific Appellate Division judgment"""
    service = CaseLawService(db)
    case = await service.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


# ============== High Court Division ==============

@router.get("/high-court", response_model=List[CaseLawResponse])
async def list_hcd_references(
    year: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List High Court Division tax references"""
    service = CaseLawService(db)
    return await service.list_cases("high_court", year, skip, limit)


@router.get("/high-court/{case_id}", response_model=CaseLawDetailResponse)
async def get_hcd_reference(case_id: str, db: AsyncSession = Depends(get_db)):
    """Get specific High Court reference"""
    service = CaseLawService(db)
    case = await service.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


# ============== Tax Appellate Tribunal ==============

@router.get("/tat", response_model=List[CaseLawResponse])
async def list_tat_decisions(
    year: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List Tax Appellate Tribunal decisions"""
    service = CaseLawService(db)
    return await service.list_cases("tat", year, skip, limit)


@router.get("/tat/{case_id}", response_model=CaseLawDetailResponse)
async def get_tat_decision(case_id: str, db: AsyncSession = Depends(get_db)):
    """Get specific TAT decision"""
    service = CaseLawService(db)
    case = await service.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


# ============== All Case Law ==============

@router.get("/judgments", response_model=List[CaseLawResponse])
async def list_all_judgments(
    court: Optional[str] = Query(None, description="Filter by court level"),
    year: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List all tax judgments across all courts"""
    service = CaseLawService(db)
    return await service.list_cases(court, year, skip, limit)


@router.get("/judgments/{case_id}", response_model=CaseLawDetailResponse)
async def get_judgment(case_id: str, db: AsyncSession = Depends(get_db)):
    """Get any judgment by ID"""
    service = CaseLawService(db)
    case = await service.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


# ============== Citation Checker ==============

@router.post("/citation-checker", response_model=CitationCheckResponse)
async def check_citation(request: CitationCheckRequest, db: AsyncSession = Depends(get_db)):
    """Check if a case citation is still good law"""
    service = CaseLawService(db)
    return await service.check_citation(request.citation)


# ============== Search ==============

@router.post("/search", response_model=CaseLawSearchResponse)
async def search_case_law(request: CaseLawSearchRequest, db: AsyncSession = Depends(get_db)):
    """Full-text search across all case law"""
    service = CaseLawService(db)
    return await service.search_cases(request)


# ============== Cases by Section ==============

@router.get("/by-section/{section_id}", response_model=List[CaseLawResponse])
async def get_cases_by_section(
    section_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get all case law referencing a specific legislation section"""
    service = CaseLawService(db)
    return await service.get_cases_by_section(section_id)


# ============== Admin Endpoints ==============

@router.post("/judgments", response_model=CaseLawResponse, status_code=201)
async def create_case(data: CaseLawCreate, db: AsyncSession = Depends(get_db)):
    service = CaseLawService(db)
    return await service.create_case(data)


@router.put("/judgments/{case_id}", response_model=CaseLawResponse)
async def update_case(case_id: str, data: CaseLawUpdate, db: AsyncSession = Depends(get_db)):
    service = CaseLawService(db)
    case = await service.update_case(case_id, data)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.delete("/judgments/{case_id}")
async def delete_case(case_id: str, db: AsyncSession = Depends(get_db)):
    service = CaseLawService(db)
    success = await service.delete_case(case_id)
    if not success:
        raise HTTPException(status_code=404, detail="Case not found")
    return {"message": "Case deleted successfully"}
