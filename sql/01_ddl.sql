-- Core tables in raw schema
CREATE TABLE IF NOT EXISTS raw.customers (
  customer_id BIGINT PRIMARY KEY,
  email VARCHAR(255),
  phone VARCHAR(32),
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw.cards (
  card_id BIGINT PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES raw.customers(customer_id),
  device_id BIGINT,
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw.merchants (
  merchant_id BIGINT PRIMARY KEY,
  category VARCHAR(64),
  country CHAR(2),
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw.devices (
  device_id BIGINT PRIMARY KEY,
  device_type VARCHAR(32),
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw.transactions (
  txn_id BIGINT PRIMARY KEY,
  card_id BIGINT NOT NULL REFERENCES raw.cards(card_id),
  merchant_id BIGINT NOT NULL REFERENCES raw.merchants(merchant_id),
  device_id BIGINT,
  ip VARCHAR(45),
  amount DECIMAL(12,2) CHECK (amount >= 0),
  currency CHAR(3),
  geo_country CHAR(2),
  txn_ts TIMESTAMP NOT NULL,
  label SMALLINT CHECK (label IN (0,1))
);
