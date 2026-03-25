from repositories.item_repository import ItemRepository
from services.graph.chat_state import ChatState

async def product_retriever_node(state: ChatState) -> dict:
    items = await ItemRepository.get_all_items()

    if not items:
        return {"retrieved_products" : "Produk habis lmaoooo jawa"}

    product_entries = []
    for item in items:
        entry = (
            f"- Product: {item['item_name']}\n"
            f" Price: IDR {item['item_customer_price']:,}\n"
            f" Link: {item.get('item_link', 'N/A')}"
        ) 
        product_entries.append(entry)

    formatted_context = "\n\n".join(product_entries)
    print(f"{len(items)} products retrieved")

    return {"retrieved_products": formatted_context}

    
