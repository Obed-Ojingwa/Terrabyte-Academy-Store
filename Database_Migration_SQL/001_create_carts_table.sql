-- Create carts table
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

-- Create indexes for carts table
CREATE INDEX IF NOT EXISTS ix_carts_id ON carts(id);
CREATE INDEX IF NOT EXISTS ix_carts_session_id ON carts(session_id);
CREATE INDEX IF NOT EXISTS ix_carts_user_id ON carts(user_id);
CREATE INDEX IF NOT EXISTS ix_carts_is_active ON carts(is_active);