# API routes module - contains all API endpoint definitions
from . import health_routes, ollama_routes, order_routes, item_routes

__all__ = ["health_routes", "ollama_routes", "order_routes", "item_routes"]
