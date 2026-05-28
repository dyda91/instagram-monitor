from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.dashboard import router as dashboard_router
from app.routes.settings import router as settings_router
from app.routes.api import router as api_router

from app.monitor import start_monitor

# =========================================================
# APP
# =========================================================
app = FastAPI()

# =========================================================
# STATIC
# =========================================================
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# =========================================================
# ROUTES
# =========================================================
app.include_router(dashboard_router)

app.include_router(settings_router)

app.include_router(api_router)

# =========================================================
# START MONITOR
# =========================================================
start_monitor()