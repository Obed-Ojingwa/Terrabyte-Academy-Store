-- Create payments table
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

-- Create indexes for payments table
CREATE INDEX IF NOT EXISTS ix_payments_id ON payments(id);
CREATE INDEX IF NOT EXISTS ix_payments_order_id ON payments(order_id);
CREATE INDEX IF NOT EXISTS ix_payments_transaction_id ON payments(transaction_id);