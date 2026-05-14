"""
JIAPI - Legislation Service
Core business logic for tax law database
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc, asc
from sqlalchemy.orm import selectinload
from datetime import date, datetime
from typing import List, Optional, Dict, Any
import difflib

from app.models.legislation import Legislation, ContentBlock, Amendment, EraEnum, LegislationType, StatusEnum
from app.schemas.legislation import (
    LegislationCreate, LegislationUpdate, LegislationResponse,
    ContentBlockResponse, AmendmentResponse,
    SectionPointInTimeResponse, DiffResponse,
    SearchRequest, SearchResponse, SearchResultItem,
    AmendmentFeedResponse, AmendmentFeedItem
)
from app.core.config import settings


class LegislationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ==================== CRUD OPERATIONS ====================

    async def create_legislation(self, data: LegislationCreate) -> LegislationResponse:
        """Create new legislation with content blocks"""
        legislation = Legislation(
            era=data.era,
            legislation_type=data.legislation_type,
            title_en=data.title_en,
            title_bn=data.title_bn,
            short_title=data.short_title,
            act_number=data.act_number,
            year=data.year,
            authority=data.authority,
            gazette_reference=data.gazette_reference,
            sro_number=data.sro_number,
            enactment_date=data.enactment_date,
            effective_date=data.effective_date,
            repeal_date=data.repeal_date,
            status=data.status,
            preamble=data.preamble,
            tags=data.tags,
            keywords=data.keywords,
            sector=data.sector,
            full_text=data.full_text,
        )

        self.db.add(legislation)
        await self.db.flush()

        # Create content blocks
        for idx, block_data in enumerate(data.content_blocks):
            block = ContentBlock(
                legislation_id=legislation.id,
                block_type=block_data.block_type,
                numbering=block_data.numbering,
                heading=block_data.heading,
                text_original=block_data.text_current,
                text_current=block_data.text_current,
                order_index=idx,
                effective_from=block_data.effective_from,
                effective_to=block_data.effective_to,
            )
            self.db.add(block)

        await self.db.commit()
        await self.db.refresh(legislation)

        return await self.get_legislation_by_id(legislation.id)

    async def get_legislation_by_id(self, legislation_id: str) -> Optional[LegislationResponse]:
        """Get legislation by ID with all content blocks"""
        result = await self.db.execute(
            select(Legislation)
            .where(Legislation.id == legislation_id)
            .options(selectinload(Legislation.content_blocks))
        )
        legislation = result.scalar_one_or_none()
        if not legislation:
            return None
        return self._to_response(legislation)

    async def list_legislations(
        self,
        era: Optional[EraEnum] = None,
        legislation_type: Optional[LegislationType] = None,
        year: Optional[int] = None,
        status: Optional[StatusEnum] = None,
        sector: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """List legislations with filtering"""
        query = select(Legislation)

        if era:
            query = query.where(Legislation.era == era)
        if legislation_type:
            query = query.where(Legislation.legislation_type == legislation_type)
        if year:
            query = query.where(Legislation.year == year)
        if status:
            query = query.where(Legislation.status == status)
        if sector:
            query = query.where(Legislation.sector == sector)
        if search:
            search_filter = or_(
                Legislation.title_en.ilike(f"%{search}%"),
                Legislation.title_bn.ilike(f"%{search}%"),
                Legislation.short_title.ilike(f"%{search}%"),
                Legislation.keywords.contains([search]),
            )
            query = query.where(search_filter)

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # Pagination
        query = query.order_by(desc(Legislation.effective_date))
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(query)
        legislations = result.scalars().all()

        return {
            "items": [self._to_response_simple(l) for l in legislations],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": (total + page_size - 1) // page_size,
        }

    async def update_legislation(self, legislation_id: str, data: LegislationUpdate) -> Optional[LegislationResponse]:
        """Update legislation metadata"""
        result = await self.db.execute(
            select(Legislation).where(Legislation.id == legislation_id)
        )
        legislation = result.scalar_one_or_none()
        if not legislation:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(legislation, field, value)

        await self.db.commit()
        await self.db.refresh(legislation)
        return await self.get_legislation_by_id(legislation_id)

    # ==================== SECTION OPERATIONS ====================

    async def get_section_by_number(
        self,
        legislation_id: str,
        section_number: str,
        as_of_date: Optional[date] = None,
    ) -> Optional[ContentBlockResponse]:
        """Get a specific section, optionally as of a specific date"""
        query = select(ContentBlock).where(
            and_(
                ContentBlock.legislation_id == legislation_id,
                ContentBlock.numbering == section_number,
                ContentBlock.block_type == "section",
            )
        )

        if as_of_date:
            query = query.where(
                and_(
                    ContentBlock.effective_from <= as_of_date,
                    or_(
                        ContentBlock.effective_to.is_(None),
                        ContentBlock.effective_to >= as_of_date,
                    ),
                )
            )

        result = await self.db.execute(query)
        block = result.scalar_one_or_none()
        if not block:
            return None

        return ContentBlockResponse(
            id=block.id,
            legislation_id=block.legislation_id,
            block_type=block.block_type,
            numbering=block.numbering,
            heading=block.heading,
            text_current=block.text_current,
            text_original=block.text_original,
            order_index=block.order_index,
            effective_from=block.effective_from,
            effective_to=block.effective_to,
            amendment_count=len(block.amendment_history) if block.amendment_history else 0,
        )

    async def get_point_in_time(
        self,
        legislation_id: str,
        section_number: str,
        as_of_date: date,
    ) -> Optional[SectionPointInTimeResponse]:
        """Get section text as it existed on a specific date with amendment history"""
        # Get the section as of the date
        section = await self.get_section_by_number(legislation_id, section_number, as_of_date)
        if not section:
            return None

        # Get amendments applied up to that date
        amendments_result = await self.db.execute(
            select(Amendment)
            .where(
                and_(
                    Amendment.target_block_id == section.id,
                    Amendment.effective_date <= as_of_date,
                    Amendment.is_applied == True,
                )
            )
            .order_by(Amendment.effective_date)
        )
        amendments = amendments_result.scalars().all()

        # Check if this is the current version
        current_section = await self.get_section_by_number(legislation_id, section_number)
        is_current = current_section and current_section.text_current == section.text_current

        return SectionPointInTimeResponse(
            legislation_id=legislation_id,
            section_number=section_number,
            as_of_date=as_of_date,
            text=section.text_current,
            amendments_applied=[
                AmendmentResponse(
                    id=a.id,
                    change_type=a.change_type,
                    old_text=a.old_text,
                    new_text=a.new_text,
                    effective_date=a.effective_date,
                    notification_date=a.notification_date,
                    description=a.description,
                    source_legislation_id=a.source_legislation_id,
                    source_section_ref=a.source_section_ref,
                    target_legislation_id=a.target_legislation_id,
                    target_block_id=a.target_block_id,
                    is_applied=a.is_applied,
                    applied_at=a.applied_at,
                )
                for a in amendments
            ],
            is_current=is_current,
        )

    async def get_diff(
        self,
        legislation_id: str,
        section_number: str,
        from_date: date,
        to_date: date,
    ) -> Optional[DiffResponse]:
        """Get diff between two dates for a section"""
        old_section = await self.get_section_by_number(legislation_id, section_number, from_date)
        new_section = await self.get_section_by_number(legislation_id, section_number, to_date)

        if not old_section or not new_section:
            return None

        # Compute diff
        old_lines = old_section.text_current.splitlines()
        new_lines = new_section.text_current.splitlines()
        diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=""))

        # Get amendments in the date range
        amendments_result = await self.db.execute(
            select(Amendment)
            .where(
                and_(
                    Amendment.target_block_id == new_section.id,
                    Amendment.effective_date >= from_date,
                    Amendment.effective_date <= to_date,
                    Amendment.is_applied == True,
                )
            )
            .order_by(Amendment.effective_date)
        )
        amendments = amendments_result.scalars().all()

        # Parse changes
        changes = []
        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                changes.append({"type": "added", "text": line[1:]})
            elif line.startswith("-") and not line.startswith("---"):
                changes.append({"type": "removed", "text": line[1:]})

        return DiffResponse(
            legislation_id=legislation_id,
            section_number=section_number,
            from_date=from_date,
            to_date=to_date,
            old_text=old_section.text_current,
            new_text=new_section.text_current,
            changes=changes,
            amendments=[
                AmendmentResponse(
                    id=a.id,
                    change_type=a.change_type,
                    old_text=a.old_text,
                    new_text=a.new_text,
                    effective_date=a.effective_date,
                    notification_date=a.notification_date,
                    description=a.description,
                    source_legislation_id=a.source_legislation_id,
                    source_section_ref=a.source_section_ref,
                    target_legislation_id=a.target_legislation_id,
                    target_block_id=a.target_block_id,
                    is_applied=a.is_applied,
                    applied_at=a.applied_at,
                )
                for a in amendments
            ],
        )

    # ==================== AMENDMENT OPERATIONS ====================

    async def create_amendment(self, amendment_data: Dict[str, Any]) -> AmendmentResponse:
        """Create and optionally apply an amendment"""
        amendment = Amendment(**amendment_data)
        self.db.add(amendment)

        if settings.AMENDMENT_AUTO_APPLY and amendment.target_block_id:
            await self._apply_amendment(amendment)

        await self.db.commit()
        await self.db.refresh(amendment)

        return AmendmentResponse(
            id=amendment.id,
            change_type=amendment.change_type,
            old_text=amendment.old_text,
            new_text=amendment.new_text,
            effective_date=amendment.effective_date,
            notification_date=amendment.notification_date,
            description=amendment.description,
            source_legislation_id=amendment.source_legislation_id,
            source_section_ref=amendment.source_section_ref,
            target_legislation_id=amendment.target_legislation_id,
            target_block_id=amendment.target_block_id,
            is_applied=amendment.is_applied,
            applied_at=amendment.applied_at,
        )

    async def _apply_amendment(self, amendment: Amendment):
        """Apply amendment to target content block"""
        if not amendment.target_block_id:
            return

        result = await self.db.execute(
            select(ContentBlock).where(ContentBlock.id == amendment.target_block_id)
        )
        block = result.scalar_one_or_none()
        if not block:
            return

        if amendment.change_type == "substitute":
            block.text_current = amendment.new_text or block.text_current
        elif amendment.change_type == "insert":
            block.text_current = (block.text_current or "") + "\n" + (amendment.new_text or "")
        elif amendment.change_type == "delete":
            if amendment.old_text and amendment.old_text in block.text_current:
                block.text_current = block.text_current.replace(amendment.old_text, "")

        amendment.is_applied = True
        amendment.applied_at = datetime.utcnow()

    async def get_amendment_feed(
        self,
        era: Optional[EraEnum] = None,
        days: int = 30,
        page: int = 1,
        page_size: int = 20,
    ) -> AmendmentFeedResponse:
        """Get recent amendments feed"""
        from_date = datetime.utcnow() - __import__("datetime").timedelta(days=days)

        query = select(Amendment).where(Amendment.created_at >= from_date)

        if era:
            query = query.join(Legislation, Amendment.target_legislation_id == Legislation.id)
            query = query.where(Legislation.era == era)

        query = query.order_by(desc(Amendment.created_at))
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(query)
        amendments = result.scalars().all()

        items = []
        for a in amendments:
            source = await self.db.execute(
                select(Legislation).where(Legislation.id == a.source_legislation_id)
            )
            target = await self.db.execute(
                select(Legislation).where(Legislation.id == a.target_legislation_id)
            )
            source_leg = source.scalar_one_or_none()
            target_leg = target.scalar_one_or_none()

            items.append(AmendmentFeedItem(
                id=a.id,
                source_title=source_leg.title_en if source_leg else "Unknown",
                target_title=target_leg.title_en if target_leg else "Unknown",
                change_type=a.change_type,
                effective_date=a.effective_date,
                description=a.description,
                created_at=a.created_at,
            ))

        return AmendmentFeedResponse(
            items=items,
            total=len(items),
            last_updated=datetime.utcnow(),
        )

    # ==================== SEARCH ====================

    async def search(self, request: SearchRequest) -> SearchResponse:
        """Full-text search across legislation and content blocks"""
        # This is a simplified version - in production, use Elasticsearch
        results = []

        # Search legislations
        leg_query = select(Legislation).where(
            or_(
                Legislation.title_en.ilike(f"%{request.query}%"),
                Legislation.title_bn.ilike(f"%{request.query}%"),
                Legislation.preamble.ilike(f"%{request.query}%"),
                Legislation.keywords.contains([request.query]),
            )
        )

        if request.era:
            leg_query = leg_query.where(Legislation.era == request.era)
        if request.legislation_type:
            leg_query = leg_query.where(Legislation.legislation_type == request.legislation_type)
        if request.year:
            leg_query = leg_query.where(Legislation.year == request.year)

        leg_result = await self.db.execute(leg_query.limit(50))
        legislations = leg_result.scalars().all()

        for leg in legislations:
            results.append(SearchResultItem(
                id=leg.id,
                type="legislation",
                title=leg.title_en,
                snippet=leg.preamble[:200] if leg.preamble else leg.title_en,
                highlights=[request.query],
                score=1.0,
                url=f"/api/v1/legislations/{leg.id}",
            ))

        # Search content blocks
        block_query = select(ContentBlock).where(
            ContentBlock.text_current.ilike(f"%{request.query}%")
        )

        if request.section_number:
            block_query = block_query.where(ContentBlock.numbering == request.section_number)

        block_result = await self.db.execute(block_query.limit(50))
        blocks = block_result.scalars().all()

        for block in blocks:
            leg_result = await self.db.execute(
                select(Legislation).where(Legislation.id == block.legislation_id)
            )
            leg = leg_result.scalar_one_or_none()

            # Find snippet around query
            text = block.text_current
            idx = text.lower().find(request.query.lower())
            start = max(0, idx - 75)
            end = min(len(text), idx + len(request.query) + 75)
            snippet = text[start:end]

            results.append(SearchResultItem(
                id=block.id,
                type="content_block",
                title=f"{leg.title_en if leg else 'Unknown'} - Section {block.numbering}" if leg else f"Section {block.numbering}",
                snippet=snippet,
                highlights=[request.query],
                score=0.9,
                url=f"/api/v1/legislations/{block.legislation_id}/sections/{block.numbering}",
            ))

        # Sort by relevance and paginate
        results.sort(key=lambda x: x.score, reverse=True)
        total = len(results)
        start_idx = (request.page - 1) * request.page_size
        end_idx = start_idx + request.page_size
        paginated = results[start_idx:end_idx]

        return SearchResponse(
            query=request.query,
            results=paginated,
            total=total,
            page=request.page,
            page_size=request.page_size,
            took_ms=0,
        )

    # ==================== HELPERS ====================

    def _to_response(self, legislation: Legislation) -> LegislationResponse:
        """Convert model to response with content blocks"""
        return LegislationResponse(
            id=legislation.id,
            era=legislation.era,
            legislation_type=legislation.legislation_type,
            title_en=legislation.title_en,
            title_bn=legislation.title_bn,
            short_title=legislation.short_title,
            act_number=legislation.act_number,
            year=legislation.year,
            authority=legislation.authority,
            gazette_reference=legislation.gazette_reference,
            sro_number=legislation.sro_number,
            enactment_date=legislation.enactment_date,
            effective_date=legislation.effective_date,
            repeal_date=legislation.repeal_date,
            status=legislation.status,
            version_number=legislation.version_number,
            parent_id=legislation.parent_id,
            document_url=legislation.document_url,
            preamble=legislation.preamble,
            tags=legislation.tags or [],
            keywords=legislation.keywords or [],
            sector=legislation.sector,
            created_at=legislation.created_at,
            updated_at=legislation.updated_at,
            content_blocks=[
                ContentBlockResponse(
                    id=b.id,
                    legislation_id=b.legislation_id,
                    block_type=b.block_type,
                    numbering=b.numbering,
                    heading=b.heading,
                    text_current=b.text_current,
                    text_original=b.text_original,
                    order_index=b.order_index,
                    effective_from=b.effective_from,
                    effective_to=b.effective_to,
                    amendment_count=len(b.amendment_history) if b.amendment_history else 0,
                )
                for b in (legislation.content_blocks or [])
            ],
            amendment_count=len(legislation.amendments) if legislation.amendments else 0,
        )

    def _to_response_simple(self, legislation: Legislation) -> LegislationResponse:
        """Simplified response without content blocks"""
        return LegislationResponse(
            id=legislation.id,
            era=legislation.era,
            legislation_type=legislation.legislation_type,
            title_en=legislation.title_en,
            title_bn=legislation.title_bn,
            short_title=legislation.short_title,
            act_number=legislation.act_number,
            year=legislation.year,
            authority=legislation.authority,
            gazette_reference=legislation.gazette_reference,
            sro_number=legislation.sro_number,
            enactment_date=legislation.enactment_date,
            effective_date=legislation.effective_date,
            repeal_date=legislation.repeal_date,
            status=legislation.status,
            version_number=legislation.version_number,
            parent_id=legislation.parent_id,
            document_url=legislation.document_url,
            preamble=legislation.preamble,
            tags=legislation.tags or [],
            keywords=legislation.keywords or [],
            sector=legislation.sector,
            created_at=legislation.created_at,
            updated_at=legislation.updated_at,
            content_blocks=[],
            amendment_count=0,
        )
