-- Create cart_items table
CREATE TABLE IF NOT EXISTS cart_items (
    id CHAR(32) PRIMARY KEY,
    quantity INTEGER NOT NULL DEFAULT 1,
    product_id CHAR(32) NOT NULL,
    cart_id CHAR(32) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE
);

-- Create indexes for cart_items table
CREATE INDEX IF NOT EXISTS ix_cart_items_id ON cart_items(id);
CREATE INDEX IF NOT EXISTS ix_cart_items_product_id ON cart_items(product_id);
CREATE INDEX IF NOT EXISTS ix_cart_items_cart_id ON cart_items(cart_id);