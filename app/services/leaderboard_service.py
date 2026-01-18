from datetime import datetime

class LeaderboardService:
    def __init__(self, db):
        self.collection = db.leaderboard

    async def upsert_score(self, user_id: str, score: int):
        """Upsert a user's score in the leaderboard (no username stored)."""
        await self.collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "user_id": user_id,
                    "score": score,
                    "last_updated": datetime.utcnow(),
                }
            },
            upsert=True,
        )

    async def get_top_n(self, n: int):
        return await self.collection.find() \
            .sort("score", -1) \
            .limit(n) \
            .to_list(length=n)

    async def get_rank(self, user_id: str):
        user = await self.collection.find_one({"user_id": user_id})
        if not user:
            return None

        rank = await self.collection.count_documents({
            "score": {"$gt": user["score"]}
        }) + 1

        return rank

    # `get_entry` removed — user retrieval is handled elsewhere previously

    async def reset_leaderboard(self) -> int:
        """Delete all entries from the leaderboard collection.

        Returns:
            int: number of deleted documents
        """
        result = await self.collection.delete_many({})
        # Motor's DeleteResult exposes `deleted_count`
        return int(getattr(result, "deleted_count", 0))
