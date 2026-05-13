import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import search, compare, calculate, fx, admin
from app.services import fx_service

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s  %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Warm up FX cache on startup so first request is never slow."""
    logger.info("LuxCompare AI starting — warming FX cache…")
    await fx_service.refresh_rates()
    logger.info("FX cache ready. Source: %s", fx_service.get_cache_meta()["source"])
    yield
    logger.info("LuxCompare AI shutting down.")


app = FastAPI(
    title="LuxCompare AI",
    description=(
        "Luxury item price comparison across France, Italy, Japan & Singapore. "
        "Live FX rates · VAT refund calculations · Singapore import GST."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router,   prefix="/search",   tags=["Search"])
app.include_router(compare.router,  prefix="/compare",  tags=["Compare"])
app.include_router(calculate.router,prefix="/calculate",tags=["Calculate"])
app.include_router(fx.router,       prefix="/fx",       tags=["FX Rates"])
app.include_router(admin.router,    prefix="/admin",    tags=["Admin"])


@app.get("/")
def root():
    return {"message": "LuxCompare AI API v2.0", "status": "operational"}


@app.get("/health")
async def health():
    fx_meta = fx_service.get_cache_meta()
    return {
        "status":   "ok",
        "fx_source": fx_meta["source"],
        "fx_live":   fx_meta["live_ok"],
        "fx_age_s":  fx_meta["age_seconds"],
    }
