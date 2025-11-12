# 🏦 Credit Card Fraud Detection — SQL ETL Pipeline

## 📘 Overview
This project sets up a **complete ETL (Extract, Transform, Load) pipeline** using **Docker, PostgreSQL, and pgAdmin**, designed for analyzing and detecting potential **credit card fraud patterns**.

The pipeline automatically loads raw CSV data into PostgreSQL, performs SQL-based transformations, and prepares enriched datasets for analytics and modeling.

---

## 🧱 Architecture

**Components**
| Service | Description |
|----------|-------------|
| **PostgreSQL** | Stores raw and transformed transaction data |
| **pgAdmin** | Web-based database management UI |
| **Docker Compose** | Manages the containerized setup for both services |
| **SQL Scripts** | Define schemas, data loading, and transformation logic |
| **ETL** | Contains SQL pipeline steps for transformation & feature creation |

---

## 📂 Project Structure

```
credit-card-fraud-sql/
│
├── data/
│   └── generated/           # CSV source files
│
├── etl/                     # SQL transformation and enrichment logic
│
├── sql/                     # Schema, raw table creation scripts
│
├── docker-compose.yml       # Docker container orchestration
├── .env.example             # Environment variable template
├── requirements.txt         # Python or dependency file if used
├── README.md                # You are here
└── Email and password PGAdmin.txt # Quick access credentials (local only)
```

---

## 🚀 Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/credit-card-fraud-sql.git
cd credit-card-fraud-sql
```

### 2️⃣ Start the containers
```bash
docker-compose up -d
```
This spins up:
- PostgreSQL on **port 5433**
- pgAdmin on **port 5050**

### 3️⃣ Access pgAdmin
- Open your browser → [http://localhost:5050](http://localhost:5050)
- Login using credentials from `Email and password PGAdmin.txt`

### 4️⃣ Register your database in pgAdmin
- **Host name:** `fraudsql-postgres`
- **Database:** `frauddb`
- **Username:** `app`
- **Password:** `app`

### 5️⃣ Verify data load
Run this inside pgAdmin’s query tool:
```sql
SELECT COUNT(*) FROM raw.transactions;
```

---

## 🧩 ETL Flow Summary

1. **Extract:** Load CSV files (customers, cards, devices, merchants, transactions) into raw PostgreSQL tables.
2. **Transform:** SQL transformations clean, join, and enrich raw data into staging and view layers:
   - `transactions_enriched`
   - `txn_flags`
   - `txn_velocity`
   - `device_cards_7d`
   - `ip_cards_7d`
3. **Load:** The transformed views are ready for data analysis or machine learning ingestion.

---

## 🧠 Key Learnings
- How to build an **ETL pipeline with SQL and Docker**
- Database schema design for **fraud detection systems**
- Using **pgAdmin** for data exploration and validation
- Applying **SQL transformations** to detect anomalies (velocity, device/IP patterns)

---

## 📅 Progress Log
| Day | Focus |
|-----|--------|
| **Day 1** | Setup PostgreSQL, pgAdmin, Docker Compose, and loaded CSVs into raw schema |
| **Day 2** | Built transformation views and intermediate data models in PostgreSQL |
| **Next** | Day 3: Fraud feature engineering & anomaly analytics |

---

## 🧑‍💻 Author
**Gazi Mohd Nayeem**  
📧 [sabrianan101@gmail.com](mailto:gazimohdnayeem@gmail.com)
