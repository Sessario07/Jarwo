import asyncio
import os
import sys
import random
from faker import Faker
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.database import init_db_pool, close_db_pool, get_db_pool
fake = Faker()

async def seed_items(pool, count=10):
    print(f"Seeding {count} items...")
    query = """
        INSERT INTO items (item_name, item_customer_price, item_seller_price, item_link)
        VALUES ($1, $2, $3, $4)
        RETURNING item_id
    """
    inserted_ids = []

    for _ in range(count):
        seller_price = round(random.uniform(10.0, 100.0), 2) 
        customer_price = round(seller_price * random.uniform(1.2, 2.0), 2)
        item_id = await pool.fetchval(
            query,
            fake.word().capitalize() + " " + fake.word().capitalize(),
            customer_price,
            seller_price,
            fake.url()
        )
        inserted_ids.append(item_id)
    print("Items seeded SUCCESSFULLY!")
    return inserted_ids

async def seed_orders(pool, item_ids, count=20):
    if not item_ids:
        print("Error: No items found to link orders to. Seed items first!")
        return
        
    print(f"Seeding {count} orders...")
    query = """
        INSERT INTO orders (user_name, address, item_id, estimated_shipping, total_cost, order_status)
        VALUES ($1, $2, $3, $4, $5, $6)
    """
    orders_data = []

    for _ in range(count):
        orders_data.append((
            fake.name(),
            fake.address().replace('\n', ', '),
            random.choice(item_ids),
            round(random.uniform(5.0, 20.0), 2),
            round(random.uniform(50.0, 300.0), 2),
            fake.boolean(chance_of_getting_true=25)
        ))

    await pool.executemany(query, orders_data)
    print("Orders seeded SUCCESSFULLY!")

async def main():
    target = 'all'
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()

    print("Creating a Connection to DB...")
    await init_db_pool()
    pool = get_db_pool()

    try:
        if target in ['all', 'items']:
            await seed_items(pool, count=5)
            
        if target in ['all', 'orders']:
            query = "SELECT item_id FROM items"
            records = await pool.fetch(query)
            item_ids = [r['item_id'] for r in records]
            await seed_orders(pool, item_ids, count=15)
            
    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        print("Closing Connection to DB...")
        await close_db_pool()

if __name__ == "__main__":
    asyncio.run(main())