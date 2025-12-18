-- 1. The Raw Lake (No changes, just dump the JSON)
CREATE TABLE IF NOT EXISTS raw_listings (
    token VARCHAR(20) PRIMARY KEY,
    raw_data JSONB NOT NULL,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. The Clean Warehouse (Updated for Rent vs Sell)
CREATE TABLE IF NOT EXISTS listings (
    token VARCHAR(20) PRIMARY KEY REFERENCES raw_listings(token),
    
    -- Core Data
    title TEXT,
    district TEXT,
    city TEXT,
    -- Extracted Features
    area INTEGER,               -- Extracted from title (e.g., 85)
    rooms INTEGER,              -- Extracted from title/desc
    -- Financials (The complex part)
    price_sell BIGINT,          -- For sales (NULL if rent)
    price_deposit BIGINT,       -- For mortgage/vadie (NULL if sell)
    price_rent BIGINT,          -- For monthly rent (NULL if sell)
    -- Metadata
    is_urgent BOOLEAN DEFAULT FALSE, -- Derived from tags if any
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create a helpful view for debugging (Optional but Recommended)
-- This lets you see the raw JSON keys easily in the future
CREATE INDEX IF NOT EXISTS idx_raw_listings_gin ON raw_listings USING gin (raw_data);