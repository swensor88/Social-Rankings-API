from app.routes.accounts import router as accounts_router
from app.routes.health import router as health_router
from app.routes.political_bodies import router as political_bodies_router
from app.routes.politicians import router as politicians_router
from app.routes.social_channels import router as social_channels_router

__all__ = [
    "health_router",
    "political_bodies_router",
    "politicians_router",
    "social_channels_router",
    "accounts_router",
]
