from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import search, compare, calculate, fx, admin

app = FastAPI(
    title="LuxCompare AI",
    description="Luxury item price comparison with live FX rates",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(compare.router, prefix="/compare", tags=["Compare"])
app.include_router(calculate.router, prefix="/calculate", tags=["Calculate"])
app.include_router(fx.router, prefix="/fx", tags=["FX Rates"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.on_event("startup")
async def startup():
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("LuxCompare AI starting — warming FX cache...")
    from app.services.fx_service import refresh_rates
    await refresh_rates()
    logger.info("Application startup complete.")

@app.get("/")
def root():
    return {"message": "LuxCompare AI API v3.0", "status": "operational"}

@app.get("/health")
def health():
    return {"status": "ok"}
