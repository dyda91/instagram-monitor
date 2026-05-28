# app/routes/dashboard.py

from fastapi import APIRouter
from fastapi import Request

from fastapi.templating import Jinja2Templates

from app.monitor import get_monitor_data

# =========================================================
# ROUTER
# =========================================================
router = APIRouter()

# =========================================================
# TEMPLATES
# =========================================================
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

# =========================================================
# DASHBOARD
# =========================================================
@router.get("/")
async def dashboard(request: Request):

    data = get_monitor_data()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "data": data
        }
    )