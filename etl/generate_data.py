import os, math, random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from tqdm import tqdm

# Config (fast defaults for Day 1)
N_CUSTOMERS = int(os.getenv("N_CUSTOMERS", "2000"))
N_CARDS_PER_CUST = (1, 3)  # inclusive range
N_MERCHANTS = int(os.getenv("N_MERCHANTS", "400"))
N_DEVICES = int(os.getenv("N_DEVICES", "1500"))
N_TRANSACTIONS = int(os.getenv("N_TRANSACTIONS", "50000"))
FRAUD_RATE = float(os.getenv("FRAUD_RATE", "0.02"))  # 2%
SEED = int(os.getenv("SEED", "42"))

rng = np.random.default_rng(SEED)
random.seed(SEED)

def gen_customers(n):
    rows = []
    now = datetime.utcnow()
    for cid in range(1, n+1):
        email = f"user{cid}@example.com"
        phone = f"+1-804-{rng.integers(200,999):03d}-{rng.integers(1000,9999):04d}"
        created = now - timedelta(days=int(rng.integers(0, 365)))
        rows.append((cid, email, phone, created))
    return pd.DataFrame(rows, columns=["customer_id","email","phone","created_at"])

def gen_devices(n):
    types = ["mobile","desktop","tablet"]
    rows = [(did, random.choice(types), datetime.utcnow()-timedelta(days=int(rng.integers(0,365))))
            for did in range(1, n+1)]
    return pd.DataFrame(rows, columns=["device_id","device_type","created_at"])

def gen_cards(customers, devices):
    rows = []
    card_id = 1
    for _, c in customers.iterrows():
        k = rng.integers(N_CARDS_PER_CUST[0], N_CARDS_PER_CUST[1]+1)
        for _ in range(int(k)):
            dev = int(devices.sample(1, random_state=int(rng.integers(0,1e9))).device_id.values[0])
            rows.append((card_id, int(c.customer_id), dev,
                         datetime.utcnow()-timedelta(days=int(rng.integers(0,365)))))
            card_id += 1
    return pd.DataFrame(rows, columns=["card_id","customer_id","device_id","created_at"])

def gen_merchants(n):
    cats = ["grocery","electronics","fashion","fuel","travel","online","dining"]
    countries = ["US","CA","GB","MX"]
    rows = [(mid, random.choice(cats), random.choice(countries),
             datetime.utcnow()-timedelta(days=int(rng.integers(0,365)))) for mid in range(1, n+1)]
    return pd.DataFrame(rows, columns=["merchant_id","category","country","created_at"])

def gen_transactions(n, cards, merchants, devices):
    rows = []
    start = datetime.utcnow() - timedelta(days=90)
    for tid in tqdm(range(1, n+1), desc="Generating transactions"):
        card_row = cards.sample(1, random_state=int(rng.integers(0,1e9))).iloc[0]
        card_id = int(card_row.card_id)
        device_id = int(card_row.device_id) if rng.random() < 0.85 else int(devices.sample(1).device_id.values[0])
        merchant_id = int(merchants.sample(1, random_state=int(rng.integers(0,1e9))).merchant_id.values[0])
        ip = f"192.168.{rng.integers(0,255)}.{rng.integers(1,255)}"
        amount = float(max(1, rng.normal(60, 40)))
        currency = "USD"
        geo_country = random.choice(["US","CA","GB","MX"] if rng.random()>0.95 else ["US"])
        ts = start + timedelta(seconds=int(rng.integers(0, 90*24*3600)))
        # Label fraud based on a few heuristics (synthetic)
        fraud = 1 if (rng.random() < FRAUD_RATE or (amount>400 and rng.random()<0.15)) else 0
        rows.append((tid, card_id, merchant_id, device_id, ip, round(amount,2), currency, geo_country, ts, fraud))
    return pd.DataFrame(rows, columns=["txn_id","card_id","merchant_id","device_id","ip","amount","currency","geo_country","txn_ts","label"])

def main(outdir="data/generated"):
    os.makedirs(outdir, exist_ok=True)
    customers = gen_customers(N_CUSTOMERS)
    devices = gen_devices(N_DEVICES)
    cards = gen_cards(customers, devices)
    merchants = gen_merchants(N_MERCHANTS)
    txns = gen_transactions(N_TRANSACTIONS, cards, merchants, devices)

    customers.to_csv(os.path.join(outdir,"customers.csv"), index=False)
    devices.to_csv(os.path.join(outdir,"devices.csv"), index=False)
    cards.to_csv(os.path.join(outdir,"cards.csv"), index=False)
    merchants.to_csv(os.path.join(outdir,"merchants.csv"), index=False)
    txns.to_csv(os.path.join(outdir,"transactions.csv"), index=False)
    print(f"Wrote CSVs to {outdir}")

if __name__ == "__main__":
    main()
