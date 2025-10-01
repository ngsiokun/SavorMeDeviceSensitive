"""
SavorMe Backend - Main FastAPI Application
Mood-Based Recipe Companion Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import router


# Create FastAPI app
app = FastAPI(
    title="SavorMe Backend API",
    description="Mood-based recipe recommendation backend with emotional intelligence",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["SavorMe API"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SavorMe Backend API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

