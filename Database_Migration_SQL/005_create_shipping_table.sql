-- Create shipping table
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

-- Create indexes for shipping table
CREATE INDEX IF NOT EXISTS ix_shipping_id ON shipping(id);
CREATE INDEX IF NOT EXISTS ix_shipping_order_id ON shipping(order_id);
CREATE INDEX IF NOT EXISTS ix_shipping_tracking_number ON shipping(tracking_number);