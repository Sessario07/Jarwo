import asyncpg
import os
from typing import Optional


_db_pool: Optional[asyncpg.Pool] = None

async def init_db_pool() -> asyncpg.Pool:
    global _db_pool
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/jarwo")
    _db_pool = await asyncpg.create_pool(database_url, min_size=5, max_size=20)
    return _db_pool

async def close_db_pool():
    global _db_pool
    if _db_pool:
        await _db_pool.close()
        _db_pool = None

def get_db_pool() -> asyncpg.Pool:
    if _db_pool is None:
        raise RuntimeError("Database pool not initialized")
    return _db_pool

def set_db_pool(pool: asyncpg.Pool):
    global _db_pool
    _db_pool = pool
