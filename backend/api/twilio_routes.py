import traceback
from fastapi import APIRouter, Form, BackgroundTasks, Response
from services.graph.chat_graph import app as graph_app
from typing import Annotated

router = APIRouter(prefix="/api/webhook", tags=["Twilio Webhook"])

async def run_graph_safe(state):
    try:
        await graph_app.ainvoke(state)
    except Exception as e:
        traceback.print_exc()

@router.post("/twilio")
async def twilio_webhook(
    background_tasks: BackgroundTasks,
    From: Annotated[str, Form(...)],
    Body: Annotated[str, Form(...)]
):
    initial_state = {
        "phone_number": From,
        "messages": [{"role": "user", "content": Body}],
        "retrieved_products": "",
        "response": ""
    }

    background_tasks.add_task(run_graph_safe, initial_state)

    twiml_content = '<?xml version="1.0" encoding="UTF-8"?><Response></Response>'
    return Response(content=twiml_content, media_type="application/xml")