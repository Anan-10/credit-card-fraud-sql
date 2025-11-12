import os
import psycopg
from psycopg import sql
from dotenv import load_dotenv

load_dotenv()
DB_DSN = os.getenv("DATABASE_URL", "postgresql+psycopg://app:app@localhost:5432/frauddb")

# psycopg expects postgresql:// not sqlalchemy-style driver part
DB_DSN = DB_DSN.replace("postgresql+psycopg://", "postgresql://")

DATA_DIR = os.getenv("DATA_DIR", "data/generated")

TABLES = [
    ("raw.customers", "customers.csv"),
    ("raw.devices", "devices.csv"),
    ("raw.cards", "cards.csv"),
    ("raw.merchants", "merchants.csv"),
    ("raw.transactions", "transactions.csv"),
]

def copy_csv(cur, table, path):
    with open(path, "r", encoding="utf-8") as f:
        cur.copy(sql.SQL("COPY {} FROM STDIN WITH (FORMAT CSV, HEADER TRUE)").format(sql.SQL(table)), f)

def main():
    with psycopg.connect(DB_DSN) as conn:
        with conn.cursor() as cur:
            for table, fname in TABLES:
                path = os.path.join(DATA_DIR, fname)
                print(f"Loading {path} into {table}...")
                copy_csv(cur, table, path)
        conn.commit()
    print("Done.")

if __name__ == "__main__":
    main()
