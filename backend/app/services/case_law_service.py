"""
JIAPI - Case Law Service
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.orm import selectinload
from typing import List, Optional

from ..models.case_law import CaseLaw, CaseLawProvision
from ..schemas.case_law import CaseLawCreate, CaseLawUpdate, CaseLawSearchRequest, CitationCheckResponse


class CaseLawService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_case(self, data: CaseLawCreate) -> CaseLaw:
        provisions_data = data.provisions_referenced or []
        case_data = data.model_dump(exclude={"provisions_referenced"})
        case = CaseLaw(**case_data)
        self.db.add(case)
        await self.db.flush()

        # Add provisions
        for prov in provisions_data:
            cp = CaseLawProvision(
                case_law_id=case.id,
                section_id=prov.get("section_id"),
                interpretation_type=prov.get("interpretation_type"),
                context_quote=prov.get("context_quote")
            )
            self.db.add(cp)

        await self.db.commit()
        await self.db.refresh(case)
        return case

    async def get_case(self, case_id: str) -> Optional[CaseLaw]:
        result = await self.db.execute(
            select(CaseLaw)
            .options(selectinload(CaseLaw.provisions_referenced))
            .where(CaseLaw.id == case_id)
        )
        return result.scalar_one_or_none()

    async def get_case_by_number(self, case_number: str) -> Optional[CaseLaw]:
        result = await self.db.execute(
            select(CaseLaw).where(CaseLaw.case_number == case_number)
        )
        return result.scalar_one_or_none()

    async def list_cases(self, court_level: Optional[str] = None, year: Optional[int] = None, 
                        skip: int = 0, limit: int = 20):
        query = select(CaseLaw)
        if court_level:
            query = query.where(CaseLaw.court_level == court_level)
        if year:
            query = query.where(CaseLaw.year == year)
        query = query.order_by(desc(CaseLaw.judgment_date)).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_case(self, case_id: str, data: CaseLawUpdate) -> Optional[CaseLaw]:
        case = await self.get_case(case_id)
        if not case:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(case, field, value)

        await self.db.commit()
        await self.db.refresh(case)
        return case

    async def delete_case(self, case_id: str) -> bool:
        case = await self.get_case(case_id)
        if not case:
            return False
        await self.db.delete(case)
        await self.db.commit()
        return True

    async def search_cases(self, request: CaseLawSearchRequest):
        query = select(CaseLaw)

        if request.query:
            search_filter = or_(
                CaseLaw.case_title.ilike(f"%{request.query}%"),
                CaseLaw.case_title_bn.ilike(f"%{request.query}%"),
                CaseLaw.headnotes.ilike(f"%{request.query}%"),
                CaseLaw.summary.ilike(f"%{request.query}%"),
                CaseLaw.full_text.ilike(f"%{request.query}%")
            )
            query = query.where(search_filter)

        if request.court_level:
            query = query.where(CaseLaw.court_level == request.court_level)
        if request.year:
            query = query.where(CaseLaw.year == request.year)
        if request.status:
            query = query.where(CaseLaw.status == request.status)
        if request.keywords:
            query = query.where(CaseLaw.keywords.overlap(request.keywords))
        if request.judgment_date_from:
            query = query.where(CaseLaw.judgment_date >= request.judgment_date_from)
        if request.judgment_date_to:
            query = query.where(CaseLaw.judgment_date <= request.judgment_date_to)

        count_result = await self.db.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar()

        query = query.order_by(desc(CaseLaw.judgment_date))
        query = query.offset((request.page - 1) * request.page_size).limit(request.page_size)

        result = await self.db.execute(query)
        items = result.scalars().all()

        return {
            "total": total,
            "page": request.page,
            "page_size": request.page_size,
            "results": items
        }

    async def check_citation(self, citation: str) -> CitationCheckResponse:
        # Try to find by case number or reporter citation
        result = await self.db.execute(
            select(CaseLaw).where(
                or_(
                    CaseLaw.case_number.ilike(f"%{citation}%"),
                    CaseLaw.reporter_citation.ilike(f"%{citation}%")
                )
            )
        )
        case = result.scalar_one_or_none()

        if not case:
            return CitationCheckResponse(
                citation=citation,
                found=False,
                is_good_law=False,
                message="Citation not found in database"
            )

        is_good = case.status.value == "good_law"
        message = f"Case found. Status: {case.status.value}"
        if case.status.value == "overruled":
            message += f". Overruled by: {case.overruling_case_id}"

        return CitationCheckResponse(
            citation=citation,
            found=True,
            case_id=case.id,
            case_title=case.case_title,
            status=case.status.value,
            is_good_law=is_good,
            overruling_case=case.overruling_case_id,
            message=message
        )

    async def get_cases_by_section(self, section_id: str):
        result = await self.db.execute(
            select(CaseLaw)
            .join(CaseLawProvision)
            .where(CaseLawProvision.section_id == section_id)
            .order_by(desc(CaseLaw.judgment_date))
        )
        return result.scalars().all()
