from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncpg
import os

from api import health_routes, ollama_routes, order_routes, item_routes
from core.database import init_db_pool, close_db_pool, set_db_pool, get_db_pool
from api import health_routes, ollama_routes, order_routes, item_routes, twilio_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_pool = await init_db_pool()
    set_db_pool(db_pool)
    yield
    await close_db_pool()

app = FastAPI(
    title="Jarwo API",
    description="AI-powered assistant API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_routes.router)
app.include_router(ollama_routes.router)
app.include_router(order_routes.router)
app.include_router(item_routes.router)
app.include_router(twilio_routes.router)

@app.get("/")
async def root():
    return {"message": "Jarwo API is running"}

