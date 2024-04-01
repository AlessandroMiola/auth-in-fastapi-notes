from fastapi import APIRouter

from basic_auth.src.apis.v1 import routes

router = APIRouter(prefix="/basic", tags=["login"])
router.include_router(routes.router)
