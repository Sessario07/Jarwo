from fastapi import APIRouter, HTTPException
from uuid import UUID
from pydantic import BaseModel
from services.order_service import OrderService

router = APIRouter(prefix="/api/orders", tags=["orders"])


class CreateOrderRequest(BaseModel):
    user_name: str
    address: str
    item_id: UUID
    estimated_shipping: float = None
    total_cost: float = None
    image_proof: str = None
    shipping_id: str = None


class UpdateOrderRequest(BaseModel):
    user_name: str = None
    address: str = None
    item_id: UUID = None
    estimated_shipping: float = None
    total_cost: float = None
    image_proof: str = None
    order_status: bool = None
    shipping_id: str = None


@router.get("")
async def list_orders():
    try:
        orders = await OrderService.list_orders()
        return {"success": True, "data": orders}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("")
async def create_order(request: CreateOrderRequest):
    try:
        order = await OrderService.create_order(
            user_name=request.user_name,
            address=request.address,
            item_id=request.item_id,
            estimated_shipping=request.estimated_shipping,
            total_cost=request.total_cost,
            image_proof=request.image_proof,
            shipping_id=request.shipping_id
        )
        return {"success": True, "data": order}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/item/{item_id}")
async def get_orders_by_item(item_id: UUID):
    try:
        orders = await OrderService.get_orders_by_item(item_id)
        return {"success": True, "data": orders}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{order_id}")
async def get_order(order_id: UUID):
    try:
        order = await OrderService.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"success": True, "data": order}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{order_id}")
async def update_order(order_id: UUID, request: UpdateOrderRequest):
    try:
        order = await OrderService.update_order(
            order_id=order_id,
            user_name=request.user_name,
            address=request.address,
            item_id=request.item_id,
            estimated_shipping=request.estimated_shipping,
            total_cost=request.total_cost,
            image_proof=request.image_proof,
            order_status=request.order_status,
            shipping_id=request.shipping_id
        )
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"success": True, "data": order}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}")
async def delete_order(order_id: UUID):
    try:
        deleted = await OrderService.delete_order(order_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"success": True, "message": "Order deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
