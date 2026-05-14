from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

@router.get("/")
async def health_check_slash():
    return {"status": "ok", "version": "1.0.0"}
