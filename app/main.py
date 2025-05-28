from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.index import router as index_router
from api.stats import router as stats_router
from api.weather import router as weather_router
from core.config import settings
from core.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(debug=settings.app.debug, lifespan=lifespan)

app.include_router(index_router)
app.include_router(weather_router)
app.include_router(stats_router)
