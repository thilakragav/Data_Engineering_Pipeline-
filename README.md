# 🚀 End-to-End Data Engineering Pipeline (PoC)

An end-to-end **Data Engineering Proof of Concept (PoC)** built using the **Medallion Architecture** (Bronze → Silver → Gold) to demonstrate modern data engineering practices including data ingestion, validation, transformations, Slowly Changing Dimensions (SCD), staging, orchestration, and automated email reporting.

---

## 📌 Project Overview

This project simulates a real-world data engineering pipeline for an e-commerce dataset. The pipeline ingests raw data, validates it, transforms it into analytics-ready datasets, stores the results in PostgreSQL, and generates automated execution reports through email.

---

## 🏗️ Architecture

```text
                   Source Data
                (CSV / JSON Files)
                        │
                        ▼
              Data Ingestion Layer
                        │
                        ▼
                 Bronze Layer
          (Raw Data in Parquet)
                        │
                        ▼
              Data Validation
      • Schema Validation
      • Null Validation
      • Duplicate Validation
      • Datatype Validation
      • Primary Key Validation
                        │
                        ▼
                 Silver Layer
      • Data Cleaning
      • Standardization
      • Lookup Mapping
      • Business Transformations
      • SCD Type 1
      • SCD Type 2
                        │
                        ▼
                 Gold Layer
      • Fact Tables
      • Dimension Tables
      • Business Aggregations
      • Analytics Ready Data
                        │
                        ▼
                 Staging Layer
      • Load Process
      • Incremental Updates
      • Data Verification
                        │
                        ▼
                PostgreSQL Database
                        │
                        ▼
             Automated Email Report
                        │
                        ▼
                 Apache Airflow
           (Pipeline Orchestration)
```

---

# ✨ Features

- End-to-End ETL Pipeline
- Medallion Architecture
- Apache Airflow Orchestration
- Data Validation Framework
- Bronze, Silver & Gold Layers
- Staging Layer
- PostgreSQL Integration
- Slowly Changing Dimensions (Type 1 & Type 2)
- Business Transformations
- Incremental Processing
- Metadata & Audit Logging
- Automated Email Notifications
- Parquet Storage Format

---

# 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Workflow | Apache Airflow |
| Database | PostgreSQL |
| Storage | Parquet |
| Processing | Pandas |
| Validation | Custom Validation Framework |
| Orchestration | Airflow DAG |
| Email | SMTP Email Automation |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```text
DataEngineeringPoC/
│
├── airflow/
│   ├── dags/
│   └── logs/
│
├── config/
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── staging/
│
├── metadata/
│
├── scripts/
│   ├── ingestion/
│   ├── validation/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── staging/
│   ├── postgres/
│   ├── email/
│   └── utils/
│
├── sql/
│
├── requirements.txt
│
├── README.md
│
└── docker-compose.yaml
```

---

# ⚙️ Pipeline Workflow

### 1. Data Ingestion

- Reads raw datasets
- Converts data into Parquet format
- Stores data in Bronze Layer

---

### 2. Data Validation

The validation framework performs:

- Schema Validation
- Null Value Validation
- Duplicate Check
- Datatype Validation
- Primary Key Validation

---

### 3. Silver Layer

The cleaned data undergoes:

- Data Cleaning
- Standardization
- Lookup Mapping
- Data Joins
- Business Rules
- Derived Columns

---

### 4. Business Transformations

Implemented transformations include:

- Customer Sales
- Product Sales
- Monthly Sales
- Category Sales
- Running Totals
- Moving Average
- Customer Ranking
- Dense Ranking

---

### 5. Slowly Changing Dimensions

Implemented:

✅ SCD Type 1

- Overwrites old values
- Maintains latest information

✅ SCD Type 2

- Preserves complete historical data
- Tracks effective dates
- Maintains current record flag

---

### 6. Gold Layer

Creates analytics-ready datasets:

- Fact Tables
- Dimension Tables
- Aggregated Reports

---

### 7. Staging Layer

The staging layer acts as an intermediate loading area before data is published to the target database.

Features:

- Incremental loading
- Data consistency checks
- Temporary storage
- Pre-load validation
- Ready for PostgreSQL loading

---

### 8. PostgreSQL Loading

Final processed data is loaded into PostgreSQL for reporting and analytics.

---

### 9. Automated Email Generation

Once the pipeline completes successfully, an automated email report is generated containing:

- Pipeline execution status
- Execution timestamp
- Tables processed
- Validation results
- Number of records processed
- Success/Failure status
- Execution summary

This enables real-time monitoring of pipeline executions.

---

### 10. Apache Airflow

The complete workflow is orchestrated using Apache Airflow.

Pipeline tasks include:

```
Ingestion
      ↓
Bronze Layer
      ↓
Validation
      ↓
Silver Layer
      ↓
SCD Processing
      ↓
Gold Layer
      ↓
Staging
      ↓
PostgreSQL Load
      ↓
Email Notification
```

---

# 📊 Data Engineering Concepts Demonstrated

- ETL Pipeline
- Medallion Architecture
- Data Validation
- Data Cleaning
- Incremental Loading
- Lookup Mapping
- Window Functions
- Aggregations
- Slowly Changing Dimensions
- Metadata Management
- Audit Logging
- Staging Layer
- Data Warehousing Concepts
- Workflow Orchestration
- Automated Reporting

---

# 🚀 How to Run

Clone the repository

```bash
git clone https://github.com/your-username/DataEngineeringPoC.git
```

Navigate to the project

```bash
cd DataEngineeringPoC
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Airflow DAG or execute the pipeline

```bash
python scripts/run_pipeline.py
```

---

# 📈 Future Enhancements

- PySpark Integration
- Delta Lake Support
- AWS S3 Data Lake
- Snowflake Data Warehouse
- Apache Kafka Streaming
- dbt Transformations
- Great Expectations Validation
- Power BI Dashboard
- CI/CD Pipeline
- Docker & Kubernetes Deployment
- AI-powered Data Quality Monitoring
- AI-based Email Classification Integration

---

# 👨‍💻 Author

**Thilak Ragav**

Data Engineering | Python | SQL | Apache Airflow | PostgreSQL | ETL | Data Warehousing | Generative AI

---

# ⭐ Key Highlights

- ✅ End-to-End Data Engineering Pipeline
- ✅ Bronze, Silver & Gold Architecture
- ✅ Data Validation Framework
- ✅ SCD Type 1 & Type 2
- ✅ Staging Layer
- ✅ PostgreSQL Integration
- ✅ Apache Airflow Orchestration
- ✅ Automated Email Generation
- ✅ Metadata & Audit Logging
- ✅ Analytics-Ready Gold Layer

---

## 📄 License

This project is created for learning purposes and demonstrates industry-standard Data Engineering concepts and best practices.
