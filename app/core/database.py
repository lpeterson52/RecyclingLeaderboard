from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


def connect():
	"""Initialize the Motor client and database reference."""
	global _client, _db
	if _client is None:
		_client = AsyncIOMotorClient(settings.MONGO_URI)
		# AsyncIOMotorClient.__getitem__ returns an AsyncIOMotorDatabase
		_db = _client[settings.MONGO_DB]
	return _client


def close():
	"""Close the Motor client."""
	global _client
	if _client is not None:
		_client.close()


async def get_database() -> AsyncIOMotorDatabase:
	"""FastAPI dependency returning the Motor database instance.

	Returns an `AsyncIOMotorDatabase`. As a runtime safeguard we assert
	the DB is initialized so static type checkers don't treat it as None.
	"""
	global _db
	if _db is None:
		connect()
	assert _db is not None
	return _db


async def ensure_indexes():
	"""Create useful indexes (call at startup)."""
	db = await get_database()
	# index on score descending for fast top-N queries
	await db.leaderboard.create_index([("score", -1)])

