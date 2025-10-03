from fastapi import APIRouter

from .category import router as category_router

router = APIRouter()

router.include_router(category_router, tags=["category"], prefix="/category")