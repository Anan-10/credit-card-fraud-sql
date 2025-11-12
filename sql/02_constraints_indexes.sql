-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_txn_card ON raw.transactions(card_id);
CREATE INDEX IF NOT EXISTS idx_txn_merchant ON raw.transactions(merchant_id);
CREATE INDEX IF NOT EXISTS idx_txn_ts ON raw.transactions(txn_ts);
CREATE INDEX IF NOT EXISTS idx_cards_customer ON raw.cards(customer_id);
CREATE INDEX IF NOT EXISTS idx_cards_device ON raw.cards(device_id);
