"""
JIAPI - Webhooks Router
Real-time notifications on law changes
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.routers.auth import get_current_active_user
from app.models.user import User, Webhook
from app.schemas.user import WebhookCreate, WebhookResponse

router = APIRouter()


@router.get("/", response_model=List[WebhookResponse])
async def list_webhooks(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's webhooks"""
    result = await db.execute(
        select(Webhook).where(Webhook.user_id == current_user.id)
    )
    return result.scalars().all()


@router.post("/", response_model=WebhookResponse)
async def create_webhook(
    webhook_data: WebhookCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new webhook for law change notifications"""
    webhook = Webhook(
        user_id=current_user.id,
        url=webhook_data.url,
        secret=webhook_data.secret,
        events=webhook_data.events,
        filter_era=webhook_data.filter_era,
        filter_legislation_types=webhook_data.filter_legislation_types,
        filter_sections=webhook_data.filter_sections
    )

    db.add(webhook)
    await db.commit()
    await db.refresh(webhook)

    return webhook


@router.get("/{webhook_id}", response_model=WebhookResponse)
async def get_webhook(
    webhook_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific webhook"""
    result = await db.execute(
        select(Webhook).where(
            Webhook.id == webhook_id,
            Webhook.user_id == current_user.id
        )
    )
    webhook = result.scalar_one_or_none()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return webhook


@router.put("/{webhook_id}", response_model=WebhookResponse)
async def update_webhook(
    webhook_id: UUID,
    webhook_data: WebhookCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update webhook configuration"""
    result = await db.execute(
        select(Webhook).where(
            Webhook.id == webhook_id,
            Webhook.user_id == current_user.id
        )
    )
    webhook = result.scalar_one_or_none()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    webhook.url = webhook_data.url
    webhook.secret = webhook_data.secret
    webhook.events = webhook_data.events
    webhook.filter_era = webhook_data.filter_era
    webhook.filter_legislation_types = webhook_data.filter_legislation_types
    webhook.filter_sections = webhook_data.filter_sections

    await db.commit()
    await db.refresh(webhook)

    return webhook


@router.delete("/{webhook_id}")
async def delete_webhook(
    webhook_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete webhook"""
    result = await db.execute(
        select(Webhook).where(
            Webhook.id == webhook_id,
            Webhook.user_id == current_user.id
        )
    )
    webhook = result.scalar_one_or_none()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    await db.delete(webhook)
    await db.commit()

    return {"message": "Webhook deleted"}


@router.post("/{webhook_id}/test")
async def test_webhook(
    webhook_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Send test payload to webhook"""
    result = await db.execute(
        select(Webhook).where(
            Webhook.id == webhook_id,
            Webhook.user_id == current_user.id
        )
    )
    webhook = result.scalar_one_or_none()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    # TODO: Implement actual webhook delivery
    test_payload = {
        "event": "webhook.test",
        "timestamp": "2024-01-01T00:00:00Z",
        "data": {
            "message": "This is a test payload from JIAPI"
        }
    }

    return {
        "message": "Test payload sent",
        "webhook_id": str(webhook_id),
        "payload": test_payload
    }
