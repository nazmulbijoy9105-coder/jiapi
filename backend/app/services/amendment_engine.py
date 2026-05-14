"""
JIAPI - Amendment Engine Service
Point-in-time computation, diff generation, auto-apply
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update
from datetime import date
from typing import List, Optional
import difflib

from app.models.legislation import ContentBlock, Amendment
from app.core.enums import ChangeType


class AmendmentEngine:
    """Core engine for tracking and applying amendments"""

    @staticmethod
    async def get_text_at_date(
        db: AsyncSession,
        block_id: str,
        as_of: date,
    ) -> Optional[str]:
        """Get the text of a content block as it existed on a specific date"""
        result = await db.execute(
            select(ContentBlock).where(
                and_(
                    ContentBlock.id == block_id,
                    ContentBlock.effective_from <= as_of,
                )
            )
        )
        block = result.scalar_one_or_none()
        if not block:
            return None

        # If block was amended after as_of, reconstruct original text
        amendments = await db.execute(
            select(Amendment).where(
                and_(
                    Amendment.target_block_id == block_id,
                    Amendment.effective_date > as_of,
                )
            ).order_by(Amendment.effective_date.desc())
        )

        text = block.text_current
        for amendment in amendments.scalars().all():
            if amendment.change_type == ChangeType.SUBSTITUTE:
                text = amendment.old_text or text
            elif amendment.change_type == ChangeType.INSERT:
                # Reverse insertion
                if amendment.new_text and amendment.new_text in text:
                    text = text.replace(amendment.new_text, "")
            elif amendment.change_type == ChangeType.DELETE:
                # Reverse deletion
                if amendment.old_text:
                    text = amendment.old_text + text

        return text

    @staticmethod
    def generate_diff(old_text: str, new_text: str) -> List[dict]:
        """Generate unified diff between two texts"""
        old_lines = old_text.splitlines(keepends=True)
        new_lines = new_text.splitlines(keepends=True)

        diff = list(difflib.unified_diff(
            old_lines, new_lines,
            fromfile="before", tofile="after",
            lineterm=""
        ))

        changes = []
        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                changes.append({"type": "added", "text": line[1:]})
            elif line.startswith("-") and not line.startswith("---"):
                changes.append({"type": "removed", "text": line[1:]})
            elif line.startswith("@@"):
                changes.append({"type": "context", "text": line})

        return changes

    @staticmethod
    async def apply_amendment(
        db: AsyncSession,
        amendment: Amendment,
        auto_apply: bool = True,
    ) -> ContentBlock:
        """Apply an amendment to its target block"""
        result = await db.execute(
            select(ContentBlock).where(ContentBlock.id == amendment.target_block_id)
        )
        block = result.scalar_one()

        if amendment.change_type == ChangeType.SUBSTITUTE:
            block.text_current = amendment.new_text or block.text_current
        elif amendment.change_type == ChangeType.INSERT:
            if amendment.new_text:
                block.text_current += "\n" + amendment.new_text
        elif amendment.change_type == ChangeType.DELETE:
            if amendment.old_text and amendment.old_text in block.text_current:
                block.text_current = block.text_current.replace(amendment.old_text, "")
        elif amendment.change_type == ChangeType.RENUMBER:
            if amendment.new_numbering:
                block.numbering = amendment.new_numbering

        block.amendment_count += 1
        amendment.auto_applied = auto_apply

        await db.flush()
        return block

    @staticmethod
    async def get_amendment_history(
        db: AsyncSession,
        block_id: str,
    ) -> List[Amendment]:
        """Get full amendment history for a content block"""
        result = await db.execute(
            select(Amendment).where(
                Amendment.target_block_id == block_id
            ).order_by(Amendment.effective_date)
        )
        return result.scalars().all()
