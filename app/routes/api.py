# app/routes/api.py

from fastapi import APIRouter

from app.monitor import get_monitor_data

# =========================================================
# ROUTER
# =========================================================
router = APIRouter(
    prefix="/api"
)

# =========================================================
# STATUS API
# =========================================================
@router.get("/status")
async def status():

    data = get_monitor_data()

    return {
        "status": "online",
        "posts": data["posts"],
        "last_check": data["last_check"],
        "instagram_user":
            data["config"]["instagram_user"]
    }