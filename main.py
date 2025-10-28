"""
FastAPI Text Analysis Application
Main entry point for the application
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn

from app.routers import api, web
from app.core.config import settings
from app.database.database import engine
from app.database.models import Base
from app.middleware.logging import LoggingMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="Text Analysis API",
    description="Analyze unstructured text to extract summaries, metadata, and sentiment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Add middleware
if settings.DEBUG:
    app.add_middleware(LoggingMiddleware)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(api.router, prefix="/api", tags=["API"])
app.include_router(web.router, tags=["Web"])

# Templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
