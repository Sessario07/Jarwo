from typing import List, Optional
from uuid import UUID
from repositories.order_repository import OrderRepository


class OrderService:
    
    @staticmethod
    async def create_order(
        user_name: str,
        address: str,
        item_id: UUID,
        estimated_shipping: float = None,
        total_cost: float = None,
        image_proof: str = None,
        shipping_id: str = None
    ) -> dict:
        return await OrderRepository.create_order(
            user_name=user_name,
            address=address,
            item_id=item_id,
            estimated_shipping=estimated_shipping,
            total_cost=total_cost,
            image_proof=image_proof,
            shipping_id=shipping_id
        )

    @staticmethod
    async def get_order(order_id: UUID) -> Optional[dict]:
        return await OrderRepository.get_order_by_id(order_id)

    @staticmethod
    async def list_orders() -> List[dict]:
        return await OrderRepository.get_all_orders()

    @staticmethod
    async def update_order(
        order_id: UUID,
        user_name: str = None,
        address: str = None,
        item_id: UUID = None,
        estimated_shipping: float = None,
        total_cost: float = None,
        image_proof: str = None,
        order_status: bool = None,
        shipping_id: str = None
    ) -> Optional[dict]:
        return await OrderRepository.update_order(
            order_id=order_id,
            user_name=user_name,
            address=address,
            item_id=item_id,
            estimated_shipping=estimated_shipping,
            total_cost=total_cost,
            image_proof=image_proof,
            order_status=order_status,
            shipping_id=shipping_id
        )

    @staticmethod
    async def delete_order(order_id: UUID) -> bool:
        return await OrderRepository.delete_order(order_id)

    @staticmethod
    async def get_orders_by_item(item_id: UUID) -> List[dict]:
        return await OrderRepository.get_orders_by_item(item_id)
