from fastapi import APIRouter, Depends, HTTPException
from app.schemas.leaderboard import LeaderboardEntry, ScoreUpdate
from app.services.leaderboard_service import LeaderboardService
from app.core.database import get_database

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/top/{n}", response_model=list[LeaderboardEntry])
async def get_top_n_leaderboard(n: int, db=Depends(get_database)):
    service = LeaderboardService(db)
    entries = await service.get_top_n(n)

    result = []
    for i, entry in enumerate(entries):
        result.append({
            "user_id": entry.get("user_id"),
            "score": entry.get("score"),
            "rank": i + 1,
            "last_updated": entry.get("last_updated"),
        })

    return result


@router.post("/reset")
async def reset_leaderboard(db = Depends(get_database)):
    """Reset the leaderboard by removing all entries. Returns deleted count."""
    service = LeaderboardService(db)
    deleted = await service.reset_leaderboard()
    return {"status": "ok", "deleted": deleted}


@router.get("/reset")
async def reset_leaderboard_get(db = Depends(get_database)):
    """Reset the leaderboard via GET (convenience) — identical to POST /reset."""
    service = LeaderboardService(db)
    deleted = await service.reset_leaderboard()
    return {"status": "ok", "deleted": deleted}


@router.post("/reset-all")
async def reset_leaderboard_alias(db = Depends(get_database)):
    """Alias endpoint for resetting the leaderboard."""
    service = LeaderboardService(db)
    deleted = await service.reset_leaderboard()
    return {"status": "ok", "deleted": deleted}


@router.post("/{user_id}")
async def update_score(
    user_id: str,
    payload: ScoreUpdate,
    db = Depends(get_database)
):
    service = LeaderboardService(db)

    await service.upsert_score(
        user_id=user_id,
        score=payload.score,
    )

    return {"status": "ok"}


@router.get("/{user_id}", response_model=LeaderboardEntry)
async def get_user_entry(user_id: str, db=Depends(get_database)):
    """Get a leaderboard entry by `user_id`. Returns 404 if not found."""
    service = LeaderboardService(db)
    doc = await service.get_entry(user_id)
    if not doc:
        raise HTTPException(status_code=404, detail="user not found")

    rank = await service.get_rank(user_id)

    return {
        "user_id": doc.get("user_id"),
        "score": doc.get("score"),
        "rank": rank or 0,
        "last_updated": doc.get("last_updated"),
    }
