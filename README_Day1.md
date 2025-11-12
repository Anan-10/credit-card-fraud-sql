# FraudGraph-SQL — Day 1 (Repo & Data)

This starter contains everything needed to spin up Postgres + pgAdmin, create schemas/tables, generate synthetic data, and load it to the **raw** schema.

## Prereqs (Windows)
- Install **Docker Desktop** and start it
- Install **Git**
- Install **Python 3.11+**

## Quickstart
```powershell
# 1) unzip project and cd into it
Copy-Item .env.example .env

# 2) Start Postgres + pgAdmin
docker compose up -d

# 3) Create schemas & tables
docker exec -i fraudsql-postgres psql -U app -d frauddb < sql/00_schemas.sql
docker exec -i fraudsql-postgres psql -U app -d frauddb < sql/01_ddl.sql
docker exec -i fraudsql-postgres psql -U app -d frauddb < sql/02_constraints_indexes.sql

# 4) Create virtual env and install deps
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt

# 5) Generate CSVs (fast defaults)
python etl/generate_data.py

# 6) Load into Postgres
python etl/load_raw.py

# 7) Verify (open pgAdmin at http://localhost:5050)
# Use admin@local / admin (from .env) to login and browse the raw schema.
```

> To control data size, set env vars before step 5: `setx N_TRANSACTIONS 100000` etc.
