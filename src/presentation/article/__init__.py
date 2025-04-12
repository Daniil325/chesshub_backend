from fastapi import APIRouter

from .tag import router as tag_router
from .category import router as category_router
from .article_tag import router as article_tag_router

router = APIRouter()

router.include_router(tag_router, tags=["tag"], prefix="/tag")
router.include_router(category_router, tags=["category"], prefix="/category")
router.include_router(article_tag_router, tags=["article_tag"], prefix="/article_tag")