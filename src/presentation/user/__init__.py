from fastapi import APIRouter

from .routes import router as user_router

router = APIRouter()

router.include_router(user_router, tags=["user"], prefix="/user")