from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.dashboard import router as dashboard_router
from app.routes.settings import router as settings_router
from app.routes.api import router as api_router

from app.monitor import start_monitor

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    start_monitor()

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

app.include_router(dashboard_router)
app.include_router(settings_router)
app.include_router(api_router)