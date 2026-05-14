"""
JIAPI - Case Law Service
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.models import CaseLaw, ContentBlock, CourtLevel, CaseStatus
from app.schemas.schemas import (
    CaseLawCreate, CaseLawResponse, CaseLawDetailResponse,
    CaseLawSearchRequest, CitationCheckRequest, CitationCheckResponse,
    PaginatedResponse, PaginationParams
)


class CaseLawService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_case(self, data: CaseLawCreate) -> CaseLaw:
        provision_ids = data.provision_ids
        case_data = data.model_dump(exclude={"provision_ids"})
        case = CaseLaw(**case_data)
        self.db.add(case)
        await self.db.flush()

        # Link provisions
        if provision_ids:
            for provision_id in provision_ids:
                block = await self.db.get(ContentBlock, provision_id)
                if block:
                    case.provisions_referenced.append(block)

        await self.db.flush()
        return case

    async def get_case(self, case_id: UUID) -> Optional[CaseLaw]:
        result = await self.db.execute(
            select(CaseLaw)
            .options(selectinload(CaseLaw.provisions_referenced))
            .options(selectinload(CaseLaw.overruling_case))
            .where(CaseLaw.id == case_id)
        )
        return result.scalar_one_or_none()

    async def get_case_by_citation(self, citation: str) -> Optional[CaseLaw]:
        result = await self.db.execute(
            select(CaseLaw).where(CaseLaw.citation == citation)
        )
        return result.scalar_one_or_none()

    async def list_cases(
        self,
        court_level: Optional[CourtLevel] = None,
        year: Optional[int] = None,
        status: Optional[CaseStatus] = None,
        issue_category: Optional[str] = None,
        era_referenced: Optional[str] = None,
        pagination: PaginationParams = None
    ) -> PaginatedResponse:
        query = select(CaseLaw)
        filters = []

        if court_level:
            filters.append(CaseLaw.court_level == court_level)
        if year:
            filters.append(CaseLaw.year == year)
        if status:
            filters.append(CaseLaw.status == status)
        if issue_category:
            filters.append(CaseLaw.issue_category == issue_category)
        if era_referenced:
            filters.append(CaseLaw.era_referenced == era_referenced)

        if filters:
            query = query.where(and_(*filters))

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        if pagination:
            query = query.offset((pagination.page - 1) * pagination.page_size).limit(pagination.page_size)

        result = await self.db.execute(query)
        items = result.scalars().all()

        page_size = pagination.page_size if pagination else len(items)
        page = pagination.page if pagination else 1
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1

        return PaginatedResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            items=[CaseLawResponse.model_validate(item) for item in items]
        )

    async def search_cases(self, request: CaseLawSearchRequest) -> List[CaseLaw]:
        query = select(CaseLaw).where(
            or_(
                CaseLaw.petitioner.ilike(f"%{request.query}%"),
                CaseLaw.respondent.ilike(f"%{request.query}%"),
                CaseLaw.headnotes_en.ilike(f"%{request.query}%"),
                CaseLaw.headnotes_bn.ilike(f"%{request.query}%"),
                CaseLaw.summary.ilike(f"%{request.query}%"),
                CaseLaw.full_text.ilike(f"%{request.query}%"),
                CaseLaw.citation.ilike(f"%{request.query}%")
            )
        )

        if request.court_level:
            query = query.where(CaseLaw.court_level == request.court_level)
        if request.year_from:
            query = query.where(CaseLaw.year >= request.year_from)
        if request.year_to:
            query = query.where(CaseLaw.year <= request.year_to)
        if request.status:
            query = query.where(CaseLaw.status == request.status)
        if request.issue_category:
            query = query.where(CaseLaw.issue_category == request.issue_category)
        if request.era_referenced:
            query = query.where(CaseLaw.era_referenced == request.era_referenced)

        result = await self.db.execute(query.limit(100))
        return result.scalars().all()

    async def check_citation(self, request: CitationCheckRequest) -> CitationCheckResponse:
        case = await self.get_case_by_citation(request.citation)

        if not case:
            return CitationCheckResponse(
                citation=request.citation,
                found=False,
                is_good_law=False
            )

        is_good = case.status == CaseStatus.GOOD_LAW
        overruling = None
        if case.overruling_case:
            overruling = case.overruling_case.citation

        return CitationCheckResponse(
            citation=request.citation,
            found=True,
            case=CaseLawResponse.model_validate(case),
            status=case.status.value,
            overruling_case=overruling,
            is_good_law=is_good
        )

    async def get_cases_by_provision(self, block_id: UUID) -> List[CaseLaw]:
        block = await self.db.get(ContentBlock, block_id)
        if not block:
            return []
        return block.case_laws
