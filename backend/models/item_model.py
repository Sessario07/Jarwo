from pydantic import BaseModel
from uuid import UUID

class ItemModel(BaseModel):
    item_id: UUID
    item_name: str
    item_customer_price: float
    item_seller_price: float
    item_link: str

    class Config:
        from_attributes = True
