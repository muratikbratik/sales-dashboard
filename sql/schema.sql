CREATE TABLE IF NOT EXISTS sales (
    order_id    INTEGER PRIMARY KEY,
    date        DATE NOT NULL,
    category    TEXT NOT NULL,
    product     TEXT NOT NULL,
    region      TEXT NOT NULL,
    channel     TEXT NOT NULL,
    quantity    INTEGER NOT NULL,
    unit_price  REAL NOT NULL,
    revenue     REAL NOT NULL,
    cost        REAL NOT NULL,
    profit      REAL NOT NULL,
    month       TEXT,
    year        INTEGER
);
