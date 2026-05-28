# app/routes/settings.py

from pathlib import Path

from fastapi import APIRouter
from fastapi import Request
from fastapi import Form

from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from app.config_manager import (
    load_config,
    save_config
)

# =========================================================
# ROUTER
# =========================================================
router = APIRouter()

# =========================================================
# TEMPLATES
# =========================================================
BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

# =========================================================
# SETTINGS PAGE
# =========================================================
@router.get("/settings")
async def settings(request: Request):

    config = load_config()

    return templates.TemplateResponse(
        request=request,
        name="settings.html",
        context={
            "config": config
        }
    )

# =========================================================
# SAVE SETTINGS
# =========================================================
@router.post("/settings")
async def save_settings(

    instagram_user: str = Form(...),
    instagram_user_id: str = Form(...),

    rapidapi_key: str = Form(...),

    smm_api_url: str = Form(...),
    smm_api_key: str = Form(...),

    service_post: str = Form(...),
    quantity_post: str = Form(...),

    service_account: str = Form(...),
    quantity_account: str = Form(...),

    tempo_minutos: int = Form(...)

):

    config = load_config()

    # =====================================================
    # INSTAGRAM
    # =====================================================
    config["instagram_user"] = instagram_user
    config["instagram_user_id"] = instagram_user_id

    # =====================================================
    # RAPIDAPI
    # =====================================================
    config["rapidapi_key"] = rapidapi_key

    # =====================================================
    # SMM
    # =====================================================
    config["smm_api_url"] = smm_api_url
    config["smm_api_key"] = smm_api_key

    # =====================================================
    # POSTS
    # =====================================================
    config["service_post"] = service_post
    config["quantity_post"] = quantity_post

    # =====================================================
    # ACCOUNT
    # =====================================================
    config["service_account"] = service_account
    config["quantity_account"] = quantity_account

    # =====================================================
    # TEMPO
    # =====================================================
    config["tempo_minutos"] = tempo_minutos

    # =====================================================
    # SAVE CONFIG
    # =====================================================
    save_config(config)

    return RedirectResponse(
        url="/settings",
        status_code=303
    )