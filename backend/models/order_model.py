from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class OrderModel(BaseModel):
    order_id: UUID
    user_name: str
    address: str
    item_id: UUID
    estimated_shipping: Optional[float] = None
    total_cost: Optional[float] = None
    image_proof: Optional[str] = None
    order_status: bool
    shipping_id: Optional[str] = None

    class Config:
        from_attributes = True
