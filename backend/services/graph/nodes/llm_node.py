from services.ollama_service import OllamaService
from services.graph.chat_state import ChatState

async def llm_node(state: ChatState) -> dict:
    ollama_service = OllamaService()

    last_user_message = state["messages"][-1]["content"] if state["messages"] else ""


    """
    Prompt mesti dibagusin, karena jawabannya mayan jelek
    well at least imo, prolly gwen shi or ionno. def needs some tweak
    """
    system_prompt = (
        "You are a helpful customer service assistant for Jarwo. "
        "Use the following product list to answer the user's question accurately. "
        "If a product is not listed, politely tell the customer we don't carry it yet. "
        "Format prices clearly and be concise.\n\n"
        f"--- INVENTORY DATA ---\n"
        f"{state.get('retrieved_products', 'No products currently available.')}\n"
        f"--- END OF DATA ---"
    )

    result = await ollama_service.generate_inference (
        prompt=last_user_message,
        system_prompt=system_prompt 
    )

    if result.get("success"):
        ai_response = result["response"]
    else:
        ai_response = "Gagal mas"

    return {
        "response": ai_response,
        "messages": [{"role": "assistant", "content": ai_response}]
    }