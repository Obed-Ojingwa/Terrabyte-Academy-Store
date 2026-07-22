from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.core.config import settings
from app.db.session import engine

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        openapi_url=f"/api/v1/openapi.json" if settings.DEBUG else None,
        docs_url=f"/api/v1/docs" if settings.DEBUG else None,
        redoc_url=f"/api/v1/redoc" if settings.DEBUG else None,
    )

    # Set up CORS
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include API router
    app.include_router(api_router, prefix="/api/v1")

    # Startup event
    @app.on_event("startup")
    async def startup():
        # Initialize database connection, etc.
        pass

    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown():
        # Close database connections, etc.
        await engine.dispose()

    return app

app = create_app()