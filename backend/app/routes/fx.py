from fastapi import APIRouter, HTTPException
from app.services import fx_service

router = APIRouter()


@router.get("")
async def get_fx_rates():
    """Return current exchange rates and cache metadata."""
    rates = await fx_service.get_rates()
    meta  = fx_service.get_cache_meta()
    return {
        "rates": rates,
        "meta":  meta,
    }


@router.post("/refresh")
async def force_refresh():
    """Force-refresh FX rates from the live API (ignores cache TTL)."""
    await fx_service.refresh_rates()
    meta = fx_service.get_cache_meta()
    return {
        "refreshed": True,
        "source":    meta["source"],
        "fetched_at": meta["fetched_at_iso"],
    }
