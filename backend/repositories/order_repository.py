from typing import List, Optional
from uuid import UUID
import asyncpg
from core.database import get_db_pool


class OrderRepository:
    
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
        pool = get_db_pool()
        query = """
            INSERT INTO orders (user_name, address, item_id, estimated_shipping, total_cost, image_proof, shipping_id, order_status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, FALSE)
            RETURNING order_id, user_name, address, item_id, estimated_shipping, total_cost, image_proof, order_status, shipping_id
        """
        result = await pool.fetchrow(
            query,
            user_name,
            address,
            item_id,
            estimated_shipping,
            total_cost,
            image_proof,
            shipping_id
        )
        return dict(result) if result else None

    @staticmethod
    async def get_order_by_id(order_id: UUID) -> Optional[dict]:
        pool = get_db_pool()
        query = """
            SELECT order_id, user_name, address, item_id, estimated_shipping, total_cost, image_proof, order_status, shipping_id
            FROM orders
            WHERE order_id = $1
        """
        result = await pool.fetchrow(query, order_id)
        return dict(result) if result else None

    @staticmethod
    async def get_all_orders() -> List[dict]:
        pool = get_db_pool()
        query = """
            SELECT order_id, user_name, address, item_id, estimated_shipping, total_cost, image_proof, order_status, shipping_id
            FROM orders
            ORDER BY order_id
        """
        results = await pool.fetch(query)
        return [dict(row) for row in results]

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
        pool = get_db_pool()
        
        updates = []
        params = []
        param_count = 1
        
        if user_name is not None:
            updates.append(f"user_name = ${param_count}")
            params.append(user_name)
            param_count += 1
        if address is not None:
            updates.append(f"address = ${param_count}")
            params.append(address)
            param_count += 1
        if item_id is not None:
            updates.append(f"item_id = ${param_count}")
            params.append(item_id)
            param_count += 1
        if estimated_shipping is not None:
            updates.append(f"estimated_shipping = ${param_count}")
            params.append(estimated_shipping)
            param_count += 1
        if total_cost is not None:
            updates.append(f"total_cost = ${param_count}")
            params.append(total_cost)
            param_count += 1
        if image_proof is not None:
            updates.append(f"image_proof = ${param_count}")
            params.append(image_proof)
            param_count += 1
        if order_status is not None:
            updates.append(f"order_status = ${param_count}")
            params.append(order_status)
            param_count += 1
        if shipping_id is not None:
            updates.append(f"shipping_id = ${param_count}")
            params.append(shipping_id)
            param_count += 1
        
        if not updates:
            return await OrderRepository.get_order_by_id(order_id)
        
        params.append(order_id)
        query = f"""
            UPDATE orders
            SET {', '.join(updates)}
            WHERE order_id = ${param_count}
            RETURNING order_id, user_name, address, item_id, estimated_shipping, total_cost, image_proof, order_status, shipping_id
        """
        
        result = await pool.fetchrow(query, *params)
        return dict(result) if result else None

    @staticmethod
    async def delete_order(order_id: UUID) -> bool:
        pool = get_db_pool()
        query = "DELETE FROM orders WHERE order_id = $1"
        result = await pool.execute(query, order_id)
        return "1" in result

    @staticmethod
    async def get_orders_by_item(item_id: UUID) -> List[dict]:
        pool = get_db_pool()
        query = """
            SELECT order_id, user_name, address, item_id, estimated_shipping, total_cost, image_proof, order_status, shipping_id
            FROM orders
            WHERE item_id = $1
            ORDER BY order_id
        """
        results = await pool.fetch(query, item_id)
        return [dict(row) for row in results]
