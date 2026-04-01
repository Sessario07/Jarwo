
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE items (
    item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_name VARCHAR(255) NOT NULL,
    item_customer_price NUMERIC(12,2) NOT NULL,
    item_seller_price NUMERIC(12,2) NOT NULL,
    item_link TEXT NOT NULL,
    item_subtitle TEXT,
    is_highlighted BOOLEAN DEFAULT FALSE
);

CREATE TABLE orders (
    order_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    item_id UUID NOT NULL,
    estimated_shipping NUMERIC(12,2),
    total_cost NUMERIC(12,2),
    image_proof TEXT,
    order_status BOOLEAN DEFAULT FALSE,
    shipping_id VARCHAR(255),

    CONSTRAINT fk_item
        FOREIGN KEY (item_id)
        REFERENCES items(item_id)
        ON DELETE CASCADE
);