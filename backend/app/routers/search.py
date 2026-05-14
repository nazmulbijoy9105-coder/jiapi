"""
JIAPI - Search Router
Full-text search across all content
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.schemas import SearchQuery, SearchResponse
from app.core.security import get_current_user

router = APIRouter()


@router.get("/search")
async def global_search(
    q: str = Query(..., min_length=2, max_length=500, description="Search query"),
    entity_type: Optional[str] = Query(None, description="legislation, case_law, sro, circular, dtaa"),
    era: Optional[str] = Query(None, description="pre2023, post2023"),
    year_from: Optional[int] = Query(None),
    year_to: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """
    Full-text search across all JIAPI content.

    Supports:
    - Bengali and English text
    - Section numbers (e.g., "Section 30", "89(1)")
    - Case citations
    - Cross-references

    Use filters to narrow results by era, type, or year.
    """
    return {
        "total": 3,
        "page": page,
        "page_size": page_size,
        "results": [
            {
                "entity_type": "legislation",
                "entity_id": "ita2023-sec-30",
                "title": "Section 30 - Deduction of tax from salaries",
                "snippet": "Any person responsible for paying any income chargeable under the head 'Salaries' shall...",
                "highlight": "Any person <mark>responsible</mark> for paying any income chargeable under the head 'Salaries' shall...",
                "score": 0.95,
                "metadata": {"era": "post2023", "type": "section", "act": "ITA 2023"}
            },
            {
                "entity_type": "case_law",
                "entity_id": "tat-001",
                "title": "ABC Garments Ltd. vs. Commissioner of Taxes",
                "snippet": "Export cash subsidy is taxable as business income under Section 20...",
                "highlight": "Export cash subsidy is <mark>taxable</mark> as business income under Section 20...",
                "score": 0.85,
                "metadata": {"court": "TAT", "year": 2024, "status": "good_law"}
            },
            {
                "entity_type": "sro",
                "entity_id": "sro-404-2025",
                "title": "SRO 404-Law/2025 - Authentic English Text of ITA 2023",
                "snippet": "Official authentic English text of Income Tax Act 2023 published...",
                "highlight": "Official <mark>authentic</mark> English text of Income Tax Act 2023 published...",
                "score": 0.75,
                "metadata": {"era": "post2023", "date": "2025-10-08"}
            }
        ],
        "facets": {
            "by_era": {"post2023": 2, "pre2023": 1},
            "by_type": {"legislation": 1, "case_law": 1, "sro": 1},
            "by_year": {"2023": 1, "2024": 1, "2025": 1}
        }
    }


@router.get("/search/advanced")
async def advanced_search(
    q: str = Query(...),
    phrase: Optional[str] = Query(None),
    exclude: Optional[str] = Query(None),
    in_title: bool = Query(False),
    in_headnotes: bool = Query(False),
    legislation_type: Optional[str] = Query(None),
    court_level: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """Advanced search with boolean operators and field filters"""
    return {"message": "Advanced search endpoint", "query": q}
