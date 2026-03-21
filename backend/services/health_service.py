import httpx
import os
from typing import Dict, Any


class HealthService:
    
    @staticmethod
    async def check_health() -> Dict[str, str]:
        return {"status": "healthy", "message": "API is running"}
    
    @staticmethod
    async def get_hello() -> Dict[str, str]:
        return {"message": "Hello from Jarwo API!"}
