from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncpg
import os

from api import health_routes, ollama_routes, order_routes, item_routes
from core.database import init_db_pool, close_db_pool, set_db_pool, get_db_pool

# Database initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db_pool = await init_db_pool()
    set_db_pool(db_pool)
    yield
    # Shutdown
    await close_db_pool()

app = FastAPI(
    title="Jarwo API",
    description="AI-powered assistant API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_routes.router)
app.include_router(ollama_routes.router)
app.include_router(order_routes.router)
app.include_router(item_routes.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Jarwo API is running"}

