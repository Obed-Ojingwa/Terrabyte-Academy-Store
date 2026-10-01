-- Create order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id CHAR(32) PRIMARY KEY,
    order_id CHAR(32) NOT NULL,
    product_id CHAR(32) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    total_price NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Create indexes for order_items table
CREATE INDEX IF NOT EXISTS ix_order_items_id ON order_items(id);
CREATE INDEX IF NOT EXISTS ix_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS ix_order_items_product_id ON order_items(product_id);