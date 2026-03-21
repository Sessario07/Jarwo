from typing import List, Optional
from uuid import UUID
from core.database import get_db_pool


class ItemRepository:
    
    @staticmethod
    async def create_item(
        item_name: str,
        item_customer_price: float,
        item_seller_price: float,
        item_link: str
    ) -> dict:
        pool = get_db_pool()
        query = """
            INSERT INTO items (item_name, item_customer_price, item_seller_price, item_link)
            VALUES ($1, $2, $3, $4)
            RETURNING item_id, item_name, item_customer_price, item_seller_price, item_link
        """
        result = await pool.fetchrow(query, item_name, item_customer_price, item_seller_price, item_link)
        return dict(result) if result else None

    @staticmethod
    async def get_item_by_id(item_id: UUID) -> Optional[dict]:
        pool = get_db_pool()
        query = """
            SELECT item_id, item_name, item_customer_price, item_seller_price, item_link
            FROM items
            WHERE item_id = $1
        """
        result = await pool.fetchrow(query, item_id)
        return dict(result) if result else None

    @staticmethod
    async def get_all_items() -> List[dict]:
        pool = get_db_pool()
        query = """
            SELECT item_id, item_name, item_customer_price, item_seller_price, item_link
            FROM items
            ORDER BY item_id
        """
        results = await pool.fetch(query)
        return [dict(row) for row in results]

    @staticmethod
    async def update_item(
        item_id: UUID,
        item_name: str = None,
        item_customer_price: float = None,
        item_seller_price: float = None,
        item_link: str = None
    ) -> Optional[dict]:
        pool = get_db_pool()
        
        updates = []
        params = []
        param_count = 1
        
        if item_name is not None:
            updates.append(f"item_name = ${param_count}")
            params.append(item_name)
            param_count += 1
        if item_customer_price is not None:
            updates.append(f"item_customer_price = ${param_count}")
            params.append(item_customer_price)
            param_count += 1
        if item_seller_price is not None:
            updates.append(f"item_seller_price = ${param_count}")
            params.append(item_seller_price)
            param_count += 1
        if item_link is not None:
            updates.append(f"item_link = ${param_count}")
            params.append(item_link)
            param_count += 1
        
        if not updates:
            return await ItemRepository.get_item_by_id(item_id)
        
        params.append(item_id)
        query = f"""
            UPDATE items
            SET {', '.join(updates)}
            WHERE item_id = ${param_count}
            RETURNING item_id, item_name, item_customer_price, item_seller_price, item_link
        """
        
        result = await pool.fetchrow(query, *params)
        return dict(result) if result else None

    @staticmethod
    async def delete_item(item_id: UUID) -> bool:
        pool = get_db_pool()
        query = "DELETE FROM items WHERE item_id = $1"
        result = await pool.execute(query, item_id)
        return "1" in result
