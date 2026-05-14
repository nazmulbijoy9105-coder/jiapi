"""
JIAPI - Amendment Service
Point-in-time and diff engine
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, asc
from typing import Optional
from datetime import date

from app.models.amendment import Amendment, ChangeType
from app.models.legislation import Section


class AmendmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_section_at_date(self, section_id: str, as_of: date) -> Optional[dict]:
        """Get section text as it existed on a specific date"""
        query = select(Section).where(Section.id == section_id)
        result = await self.db.execute(query)
        section = result.scalar_one_or_none()

        if not section:
            return None

        # Start with original text
        current_text = section.text_original or ""

        # Get all amendments applied before the target date
        amend_query = select(Amendment).where(
            and_(
                Amendment.target_section_id == section_id,
                Amendment.is_applied == "applied",
                Amendment.effective_date <= as_of,
            )
        ).order_by(asc(Amendment.effective_date))

        amend_result = await self.db.execute(amend_query)
        amendments = amend_result.scalars().all()

        # Apply amendments sequentially
        applied_amendments = []
        for amendment in amendments:
            if amendment.change_type == ChangeType.SUBSTITUTE:
                current_text = amendment.new_text or current_text
            elif amendment.change_type == ChangeType.INSERT:
                current_text = (current_text or "") + "\n" + (amendment.new_text or "")
            elif amendment.change_type == ChangeType.DELETE:
                if amendment.old_text and current_text:
                    current_text = current_text.replace(amendment.old_text, "")
            elif amendment.change_type == ChangeType.REPEAL:
                current_text = "[REPEALED]"

            applied_amendments.append({
                "id": amendment.id,
                "change_type": amendment.change_type.value,
                "effective_date": str(amendment.effective_date),
                "source": amendment.source_legislation.title_en if amendment.source_legislation else None,
            })

        return {
            "section_id": section.id,
            "section_number": section.section_number,
            "section_title": section.section_title_en,
            "as_of_date": str(as_of),
            "text": current_text,
            "original_text": section.text_original,
            "amendments_applied": len(applied_amendments),
            "amendment_history": applied_amendments,
        }

    async def get_section_diff(self, section_id: str, from_date: date, to_date: date) -> Optional[dict]:
        """Get diff between two dates"""
        from_text_data = await self.get_section_at_date(section_id, from_date)
        to_text_data = await self.get_section_at_date(section_id, to_date)

        if not from_text_data or not to_text_data:
            return None

        # Get amendments between the two dates
        amend_query = select(Amendment).where(
            and_(
                Amendment.target_section_id == section_id,
                Amendment.is_applied == "applied",
                Amendment.effective_date > from_date,
                Amendment.effective_date <= to_date,
            )
        ).order_by(asc(Amendment.effective_date))

        amend_result = await self.db.execute(amend_query)
        amendments = amend_result.scalars().all()

        # Simple diff highlighting
        changes = []
        for amendment in amendments:
            changes.append({
                "amendment_id": amendment.id,
                "change_type": amendment.change_type.value,
                "effective_date": str(amendment.effective_date),
                "old_text": amendment.old_text,
                "new_text": amendment.new_text,
                "summary": amendment.amendment_summary,
            })

        return {
            "section_id": section_id,
            "section_number": from_text_data["section_number"],
            "from_date": str(from_date),
            "to_date": str(to_date),
            "old_text": from_text_data["text"],
            "new_text": to_text_data["text"],
            "changes": changes,
            "amendments_applied": [{
                "id": a.id,
                "change_type": a.change_type.value,
                "effective_date": str(a.effective_date),
                "source": a.source_legislation.title_en if a.source_legislation else None,
            } for a in amendments],
        }

    async def apply_amendment(self, amendment_id: str) -> bool:
        """Apply an amendment to update section text"""
        query = select(Amendment).where(Amendment.id == amendment_id)
        result = await self.db.execute(query)
        amendment = result.scalar_one_or_none()

        if not amendment:
            return False

        if not amendment.target_section_id:
            return False

        # Get target section
        sec_query = select(Section).where(Section.id == amendment.target_section_id)
        sec_result = await self.db.execute(sec_query)
        section = sec_result.scalar_one_or_none()

        if not section:
            return False

        # Apply the change
        current = section.text_current or section.text_original or ""

        if amendment.change_type == ChangeType.SUBSTITUTE:
            section.text_current = amendment.new_text or current
        elif amendment.change_type == ChangeType.INSERT:
            section.text_current = current + "\n" + (amendment.new_text or "")
        elif amendment.change_type == ChangeType.DELETE:
            if amendment.old_text and current:
                section.text_current = current.replace(amendment.old_text, "")
        elif amendment.change_type == ChangeType.REPEAL:
            section.text_current = "[REPEALED]"
            section.is_repealed = True
        elif amendment.change_type == ChangeType.RENUMBER:
            if amendment.new_number:
                section.section_number = amendment.new_number

        section.is_amended = True
        amendment.is_applied = "applied"
        amendment.applied_at = date.today()

        await self.db.commit()
        return True
