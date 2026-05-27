from fastapi import FastAPI

from app.config import settings
from app.migrations import run_startup_migrations
from app.routes import (
    accounts_router,
    health_router,
    political_bodies_router,
    politicians_router,
    social_channels_router,
)

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def startup() -> None:
    if settings.run_migrations_on_startup:
        run_startup_migrations()

app.include_router(health_router)
app.include_router(political_bodies_router)
app.include_router(politicians_router)
app.include_router(social_channels_router)
app.include_router(accounts_router)
