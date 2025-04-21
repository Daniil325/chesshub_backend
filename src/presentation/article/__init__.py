from fastapi import APIRouter

from .tag import router as tag_router
from .category import router as category_router
from .article_tag import router as article_tag_router
from .article_reaction import router as article_reaction_router
from .article import router as article_router
from .image import router as image_router

router = APIRouter()

router.include_router(tag_router, tags=["tag"], prefix="/tag")
router.include_router(category_router, tags=["category"], prefix="/category")
router.include_router(article_tag_router, tags=["article_tag"], prefix="/article_tag")
router.include_router(
    article_reaction_router, tags=["article_reaction"], prefix="/article_reaction"
)
router.include_router(article_router, tags=["article"], prefix="/article")
router.include_router(image_router, tags=["image"], prefix="/image")
