from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from app.config import settings
from app.migrations import run_startup_migrations
from app.routes import (
    accounts_router,
    health_router,
    political_bodies_router,
    politicians_router,
    social_channels_router,
)

root_path = "/stage" if settings.app_env == "stage" else ""

app = FastAPI(title=settings.app_name, root_path=root_path, docs_url=None)


@app.on_event("startup")
def startup() -> None:
    if settings.run_migrations_on_startup:
        run_startup_migrations()


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url="openapi.json",
        title=f"{settings.app_name} - Swagger UI",
    )

app.include_router(health_router)
app.include_router(political_bodies_router)
app.include_router(politicians_router)
app.include_router(social_channels_router)
app.include_router(accounts_router)
