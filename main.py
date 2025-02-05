from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError
from test_notice.middlewares.logging import ActionLoggingMiddleware
from test_notice.models import init_mongo
from test_notice.routes.auth import router as auth
from test_notice.routes.notice import router as notice
from test_notice.routes.admin import router as admin


def include_middlewares(app: FastAPI) -> FastAPI:
    app.add_middleware(ActionLoggingMiddleware)
    return app


def include_routes(app: FastAPI) -> FastAPI:
    app.include_router(auth)
    app.include_router(notice)
    app.include_router(admin)
    return app


async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content=[error for error in exc.errors()],
    )


def incldue_exception_handlers(app: FastAPI) -> FastAPI:
    # app.add_exception_handler(500, validation_exception_handler)
    return app


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # pylint: disable=unused-argument
    await init_mongo()
    yield


def build_app_main() -> FastAPI:
    app = FastAPI(
        root_path="/api/v1",
        lifespan=lifespan
    )
    app = include_routes(app)
    app = include_middlewares(app)
    app = incldue_exception_handlers(app)
    return app


app = build_app_main()
