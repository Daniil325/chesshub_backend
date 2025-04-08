from fastapi import APIRouter

from .tag import router as tag_router

router = APIRouter()

router.include_router(tag_router, tags=["tag"], prefix="/tag")
