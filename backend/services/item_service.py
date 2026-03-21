from typing import List, Optional
from uuid import UUID
from repositories.item_repository import ItemRepository


class ItemService:
    
    @staticmethod
    async def create_item(
        item_name: str,
        item_customer_price: float,
        item_seller_price: float,
        item_link: str
    ) -> dict:
        return await ItemRepository.create_item(
            item_name=item_name,
            item_customer_price=item_customer_price,
            item_seller_price=item_seller_price,
            item_link=item_link
        )

    @staticmethod
    async def get_item(item_id: UUID) -> Optional[dict]:
        return await ItemRepository.get_item_by_id(item_id)

    @staticmethod
    async def list_items() -> List[dict]:
        return await ItemRepository.get_all_items()

    @staticmethod
    async def update_item(
        item_id: UUID,
        item_name: str = None,
        item_customer_price: float = None,
        item_seller_price: float = None,
        item_link: str = None
    ) -> Optional[dict]:
        return await ItemRepository.update_item(
            item_id=item_id,
            item_name=item_name,
            item_customer_price=item_customer_price,
            item_seller_price=item_seller_price,
            item_link=item_link
        )

    @staticmethod
    async def delete_item(item_id: UUID) -> bool:
        return await ItemRepository.delete_item(item_id)
