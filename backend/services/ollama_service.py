import httpx
import os
from typing import Dict, Any


class OllamaService:
    
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        self.model = "qwen2.5:3b-instruct"
    
    async def generate_inference(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> Dict[str, Any]:
        if not prompt:
            return {"error": "Prompt is required"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "system": system_prompt,
                        "stream": False
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                return {
                    "success": True,
                    "model": self.model,
                    "prompt": prompt,
                    "response": result.get("response", ""),
                    "done": result.get("done", False)
                }
        except httpx.HTTPError as e:
            return {
                "success": False,
                "error": f"HTTP error occurred: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating inference: {str(e)}"
            }
