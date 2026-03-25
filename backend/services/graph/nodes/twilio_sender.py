import os 
import asyncio
from twilio.rest import Client
from services.graph.chat_state import ChatState

async def twilio_sender_node(state: ChatState) -> dict:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
    recipient = state.get("phone_number")
    message_body = state.get("response")
    recipient = state.get("phone_number")
    message_body = state.get("response")

    if not recipient or not message_body:
        print(f"Error: Ora ada phone num, atau respons. State: {state}")
        return {}
    
    if not recipient.startswith("whatsapp:"):
        recipient = f"whatsapp:{recipient}"
    if not twilio_number.startswith("whatsapp:"):
        twilio_number = f"whatsapp:{twilio_number}"

    try: 
        client = Client(account_sid, auth_token)

        message = await asyncio.to_thread(
            client.messages.create,
            from_=twilio_number,
            to=recipient,
            body=message_body
        )
        print(f"Berhasil rek, SID: {message.sid}")

    except Exception as e:
        print(f"Gagal rek, Error: {str(e)}")

    return {}