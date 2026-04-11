CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    segment TEXT,
    signup_date DATE,
    region TEXT,
    channel TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    cost_price NUMERIC,
    retail_price NUMERIC
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT REFERENCES customers(customer_id),
    order_date DATE,
    product_id TEXT REFERENCES products(product_id),
    quantity INTEGER,
    discount NUMERIC,
    channel TEXT,
    warehouse TEXT
);

CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    warehouse TEXT,
    product_id TEXT REFERENCES products(product_id),
    on_hand INTEGER,
    reorder_point INTEGER,
    lead_time_days INTEGER
);

CREATE TABLE IF NOT EXISTS marketing_spend (
    campaign_id TEXT PRIMARY KEY,
    channel TEXT,
    month DATE,
    spend NUMERIC,
    attributed_revenue NUMERIC,
    impressions INTEGER,
    clicks INTEGER,
    conversions INTEGER
);

CREATE TABLE IF NOT EXISTS logistics (
    shipment_id TEXT PRIMARY KEY,
    order_id TEXT REFERENCES orders(order_id),
    carrier TEXT,
    status TEXT,
    ship_date DATE,
    delivery_date DATE,
    warehouse TEXT,
    region TEXT,
    tracking_number TEXT
);
