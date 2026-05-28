# app/routes/dashboard.py

from pathlib import Path

from fastapi import APIRouter
from fastapi import Request

from fastapi.templating import Jinja2Templates

from app.monitor import get_monitor_data
from app.config_manager import load_config

# =========================================================
# ROUTER
# =========================================================
router = APIRouter()

# =========================================================
# TEMPLATE
# =========================================================
BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

# =========================================================
# DASHBOARD
# =========================================================
@router.get("/")
async def dashboard(request: Request):

    monitor_data = get_monitor_data()

    config = load_config()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "posts": monitor_data["posts"],
            "logs": monitor_data["logs"],
            "config": config
        }
    )