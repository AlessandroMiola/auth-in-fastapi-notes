from fastapi import FastAPI

from basic_auth.src.apis.api import router


def include_router(app) -> None:
    app.include_router(router)


app = FastAPI()
include_router(app)
