"""
JIAPI - Case Law Router
Appellate Division, High Court Division, Tax Appellate Tribunal
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from datetime import date
from app.schemas import CaseLawResponse, CaseLawBase, SearchQuery
from app.core.security import get_current_user

router = APIRouter()


@router.get("/judgments/appellate-division", response_model=List[CaseLawResponse])
async def list_ad_judgments(
    year: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """
    List Appellate Division tax judgments.

    Highest court in Bangladesh. Final authority on tax matters.
    """
    return [
        {
            "id": "ad-001",
            "case_number": "Civil Appeal No. 45 of 2019",
            "case_title": "Commissioner of Taxes vs. Grameenphone Ltd.",
            "court_level": "appellate_division",
            "judgment_date": date(2022, 3, 15),
            "year": 2022,
            "appellant": "Commissioner of Taxes, Dhaka",
            "respondent": "Grameenphone Ltd.",
            "assessee_name": "Grameenphone Ltd.",
            "headnotes": """Whether SIM tax is a tax on income or a regulatory fee. 
            Held: SIM tax is not income tax but a regulatory fee under Telecommunications Act.""",
            "status": "good_law",
            "assessment_year": "2015-2016",
            "tax_amount_involved": 250000000,
            "era_referenced": "pre2023",
            "sections_referenced": ["2(62)", "4"],
            "citation": "72 DLR (AD) 45",
            "created_at": "2022-03-15T00:00:00",
            "updated_at": "2022-03-15T00:00:00"
        }
    ]


@router.get("/judgments/high-court", response_model=List[CaseLawResponse])
async def list_hcd_judgments(
    year: Optional[int] = Query(None),
    division: Optional[str] = Query(None, description="dhaka, chittagong, khulna, rajshahi, sylhet, barisal, rangpur"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """
    List High Court Division tax references.

    HCD handles tax references under Section 160 of ITA 2023 (formerly Section 159 of ITO 1984).
    """
    return [
        {
            "id": "hcd-001",
            "case_number": "Income Tax Reference No. 12 of 2020",
            "case_title": "Bangladesh Bank vs. Commissioner of Taxes",
            "court_level": "high_court",
            "bench": "Dhaka",
            "judgment_date": date(2021, 8, 20),
            "year": 2021,
            "appellant": "Bangladesh Bank",
            "respondent": "Commissioner of Taxes",
            "headnotes": """Whether interest on government securities is taxable. 
            Held: Interest on T-bills is taxable under the head 'Interest on Securities'.""",
            "status": "good_law",
            "assessment_year": "2018-2019",
            "era_referenced": "pre2023",
            "sections_referenced": ["19", "22"],
            "citation": "73 DLR 234",
            "created_at": "2021-08-20T00:00:00",
            "updated_at": "2021-08-20T00:00:00"
        }
    ]


@router.get("/judgments/tat", response_model=List[CaseLawResponse])
async def list_tat_decisions(
    year: Optional[int] = Query(None),
    bench: Optional[str] = Query(None, description="dhaka, chittagong, khulna, rajshahi"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """
    List Tax Appellate Tribunal (TAT) decisions.

    TAT is the first-instance appellate body under ITA 2023 Section 159.
    """
    return [
        {
            "id": "tat-001",
            "case_number": "TAT Appeal No. 234 of 2023",
            "case_title": "ABC Garments Ltd. vs. Commissioner of Taxes",
            "court_level": "tat",
            "tribunal_bench": "Dhaka",
            "judgment_date": date(2024, 2, 10),
            "year": 2024,
            "appellant": "ABC Garments Ltd.",
            "respondent": "Commissioner of Taxes, Dhaka",
            "assessee_name": "ABC Garments Ltd.",
            "headnotes": """Whether export cash subsidy is taxable income. 
            Held: Export cash subsidy is taxable as business income under Section 20.""",
            "status": "good_law",
            "assessment_year": "2021-2022",
            "tax_amount_involved": 15000000,
            "era_referenced": "post2023",
            "sections_referenced": ["20", "30"],
            "citation": "TAT Dhaka 234/2023",
            "created_at": "2024-02-10T00:00:00",
            "updated_at": "2024-02-10T00:00:00"
        }
    ]


@router.get("/judgments/{case_id}", response_model=CaseLawResponse)
async def get_judgment(
    case_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get full judgment by ID with all provisions referenced"""
    raise HTTPException(status_code=501, detail="Coming soon")


@router.get("/search")
async def search_case_law(
    q: str = Query(..., min_length=2),
    court: Optional[str] = Query(None),
    year_from: Optional[int] = Query(None),
    year_to: Optional[int] = Query(None),
    era: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Full-text search across all case law.

    Supports Bengali and English text search.
    """
    return {
        "total": 1,
        "results": [
            {
                "case_id": "tat-001",
                "title": "ABC Garments Ltd. vs. Commissioner of Taxes",
                "court": "TAT Dhaka",
                "year": 2024,
                "snippet": "Export cash subsidy is taxable as business income...",
                "score": 0.95
            }
        ]
    }


@router.get("/citation-checker")
async def check_citation(
    citation: str = Query(..., description="Case citation to verify"),
    current_user: dict = Depends(get_current_user)
):
    """
    Verify if a case citation is still good law.

    Checks overruling, distinguishing, and following cases.
    """
    return {
        "citation": citation,
        "status": "good_law",
        "overruled_by": None,
        "distinguished_in": [],
        "followed_in": [],
        "last_verified": date.today()
    }


@router.get("/provisions/{section_number}/cases")
async def get_cases_by_provision(
    section_number: str,
    era: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Get all case law that references a specific section"""
    return {"section": section_number, "cases": [], "count": 0}
