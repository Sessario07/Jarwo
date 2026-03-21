from fastapi import APIRouter, Query
from pydantic import BaseModel
from services.ollama_service import OllamaService

router = APIRouter(prefix="/api/ollama", tags=["ollama"])
ollama_service = OllamaService()

class InferenceRequest(BaseModel):
    prompt: str
    system_prompt: str = "You are a helpful assistant."

@router.post("")
async def generate_inference(request: InferenceRequest):
    return await ollama_service.generate_inference(request.prompt, request.system_prompt)

@router.get("")
async def generate_inference_get(
    prompt: str = Query(..., description="The prompt for inference"),
    system_prompt: str = Query("You are a helpful assistant.", description="System prompt for context")
):
    return await ollama_service.generate_inference(prompt, system_prompt)
