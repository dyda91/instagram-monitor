from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.dashboard import router as dashboard_router
from app.routes.settings import router as settings_router
from app.routes.api import router as api_router

from app.monitor import start_monitor


# =========================================================
# LIFESPAN (STARTUP SEGURO)
# =========================================================
@asynccontextmanager
async def lifespan(app: FastAPI):

    # inicia o monitor junto com o servidor
    start_monitor()

    yield

    # aqui você poderia parar threads se necessário no futuro


# =========================================================
# APP
# =========================================================
app = FastAPI(lifespan=lifespan)


# =========================================================
# STATIC FILES
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