from pydantic import BaseModel
from datetime import datetime

class LeaderboardEntry(BaseModel):
    user_id: str
    score: int
    rank: int
    last_updated: datetime

class ScoreUpdate(BaseModel):
    score: int