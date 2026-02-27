from aiogram import Router
from .start import router as start_router
from .booking import router as booking_router
from .manager import router as manager_router

router = Router()
router.include_router(start_router)
router.include_router(booking_router)
router.include_router(manager_router)

__all__ = ["router"]
