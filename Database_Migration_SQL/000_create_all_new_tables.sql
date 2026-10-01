-- Create all new tables for Milestone 2 and 3 implementation
-- Run these in order to create the necessary tables

-- 1. Create carts table
CREATE TABLE IF NOT EXISTS carts (
    id CHAR(32) PRIMARY KEY,
    session_id VARCHAR(255) NULL,
    user_id CHAR(32) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_checked_out BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 2. Create cart_items table
CREATE TABLE IF NOT EXISTS cart_items (
    id CHAR(32) PRIMARY KEY,
    quantity INTEGER NOT NULL DEFAULT 1,
    product_id CHAR(32) NOT NULL,
    cart_id CHAR(32) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE
);

-- 3. Create order_items table
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

-- 4. Create payments table
CREATE TABLE IF NOT EXISTS payments (
    id CHAR(32) PRIMARY KEY,
    amount NUMERIC(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    payment_method VARCHAR(50) NOT NULL,
    transaction_id VARCHAR(255) NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP WITH TIME ZONE NULL,
    order_id CHAR(32) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- 5. Create shipping table
CREATE TABLE IF NOT EXISTS shipping (
    id CHAR(32) PRIMARY KEY,
    service VARCHAR(100) NOT NULL,
    cost NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    tracking_number VARCHAR(255) NULL UNIQUE,
    tracking_url VARCHAR(500) NULL,
    address_line_1 VARCHAR(255) NOT NULL,
    address_line_2 VARCHAR(255) NULL,
    city VARCHAR(100) NOT NULL,
    state_province VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    shipped_at TIMESTAMP WITH TIME ZONE NULL,
    delivered_at TIMESTAMP WITH TIME ZONE NULL,
    order_id CHAR(32) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- Create indexes for all tables

-- Indexes for carts table
CREATE INDEX IF NOT EXISTS ix_carts_id ON carts(id);
CREATE INDEX IF NOT EXISTS ix_carts_session_id ON carts(session_id);
CREATE INDEX IF NOT EXISTS ix_carts_user_id ON carts(user_id);
CREATE INDEX IF NOT EXISTS ix_carts_is_active ON carts(is_active);

-- Indexes for cart_items table
CREATE INDEX IF NOT EXISTS ix_cart_items_id ON cart_items(id);
CREATE INDEX IF NOT EXISTS ix_cart_items_product_id ON cart_items(product_id);
CREATE INDEX IF NOT EXISTS ix_cart_items_cart_id ON cart_items(cart_id);

-- Indexes for order_items table
CREATE INDEX IF NOT EXISTS ix_order_items_id ON order_items(id);
CREATE INDEX IF NOT EXISTS ix_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS ix_order_items_product_id ON order_items(product_id);

-- Indexes for payments table
CREATE INDEX IF NOT EXISTS ix_payments_id ON payments(id);
CREATE INDEX IF NOT EXISTS ix_payments_order_id ON payments(order_id);
CREATE INDEX IF NOT EXISTS ix_payments_transaction_id ON payments(transaction_id);

-- Indexes for shipping table
CREATE INDEX IF NOT EXISTS ix_shipping_id ON shipping(id);
CREATE INDEX IF NOT EXISTS ix_shipping_order_id ON shipping(order_id);
CREATE INDEX IF NOT EXISTS ix_shipping_tracking_number ON shipping(tracking_number);