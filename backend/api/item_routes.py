from fastapi import APIRouter, HTTPException
from uuid import UUID
from pydantic import BaseModel
from models.item_model import ItemModel
from services.item_service import ItemService

router = APIRouter(prefix="/api/items", tags=["items"])


class CreateItemRequest(BaseModel):
    item_name: str
    item_customer_price: float
    item_seller_price: float
    item_link: str


class UpdateItemRequest(BaseModel):
    item_name: str = None
    item_customer_price: float = None
    item_seller_price: float = None
    item_link: str = None


@router.post("")
async def create_item(request: CreateItemRequest):
    try:
        item = await ItemService.create_item(
            item_name=request.item_name,
            item_customer_price=request.item_customer_price,
            item_seller_price=request.item_seller_price,
            item_link=request.item_link
        )
        return {"success": True, "data": item}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{item_id}")
async def get_item(item_id: UUID):
    try:
        item = await ItemService.get_item(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"success": True, "data": item}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
async def list_items():
    try:
        items = await ItemService.list_items()
        return {"success": True, "data": items}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{item_id}")
async def update_item(item_id: UUID, request: UpdateItemRequest):
    try:
        item = await ItemService.update_item(
            item_id=item_id,
            item_name=request.item_name,
            item_customer_price=request.item_customer_price,
            item_seller_price=request.item_seller_price,
            item_link=request.item_link
        )
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"success": True, "data": item}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{item_id}")
async def delete_item(item_id: UUID):
    try:
        deleted = await ItemService.delete_item(item_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"success": True, "message": "Item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/highlighted")
async def get_highlighted():
    item = await ItemRepository.get_highlighted_items()
    if not item:
        return {"error": "No highlighted item found"}
    return item
