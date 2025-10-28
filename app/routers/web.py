"""
Web interface routes
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def web_interface(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse("index.html", {"request": request})
