from fastapi import FastAPI
from app.core.config import get_settings
from app.core.middleware import setup_cors_middleware
from app.api.endpoints import audio

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Setup middleware
setup_cors_middleware(app)

# Include routers
app.include_router(audio.router, prefix=f"{settings.API_V1_STR}/audio", tags=["audio"])