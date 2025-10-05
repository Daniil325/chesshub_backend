from fastapi import APIRouter

from .test import router as test_router
from .course import router as courses_router
from .lesson import router as lesson_router

router = APIRouter()

router.include_router(test_router, tags=["test"], prefix="/test")
router.include_router(courses_router, tags=["course"], prefix="/course")
router.include_router(lesson_router, tags=["lesson"], prefix="/lesson")