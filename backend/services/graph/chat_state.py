from typing import TypedDict, List, Annotated
import operator

class ChatState(TypedDict):
    phone_number: str
    messages: Annotated[List[dict], operator.add]
    retrieved_products: str
    response: str