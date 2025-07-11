# 📁 Implementasi Ekosistem Hadoop untuk Analisis Perdagangan Internasional Bahan Pangan (2024)

> 🚀 Big data pipeline for batch processing of food import datasets using Hadoop ecosystem, Spark, and Superset.

---

## 📌 Overview

This project builds a **Hadoop-based data platform** to analyze Indonesia's international food import data. It leverages **batch processing**, **Medallion architecture**, and a modern open-source stack for scalable data ingestion, transformation, and visualization.

- 🌐 Dataset: UN Comtrade & FAOSTAT (food import data)
- 🏢 Stack: Hadoop, Spark, Hive, Superset, Docker
- 🤖 Goal: End-to-end pipeline from raw data to dashboard

---

## 💼 Team

Developed by **Kelompok 13 – Institut Teknologi Sumatera (Prodi Sains Data)**
- Rangga Adi Putra
- Cyntia Kristina Sidauruk
- Azizah Kusumah Putri
- Farrel Julio Akbar

---

## 🛠️ System Architecture

### 🔄 Medallion Architecture

| Layer  | Description                                     | Format           | Tools             |
|--------|--------------------------------------------------|------------------|--------------------|
| Bronze | Raw external data                               | CSV / JSON       | HDFS               |
| Silver | Cleaned, structured data                        | Parquet / ORC    | Spark, Hive        |
| Gold   | Aggregated, analytics-ready data                | Parquet / ORC    | Hive, Superset     |

### 🏗️ Stack Components

- **HDFS** – Distributed file storage
- **Apache Spark** – ETL, transformation, MLlib
- **Apache Hive** – SQL engine and table registry
- **Apache Superset** – Dashboard visualization
- **Docker Compose** – Local cluster orchestration
- **Crontab / Airflow** – Batch job scheduling

---

## 📈 Datasets

- **UN Comtrade** – Global food trade data
- **FAOSTAT** – Food agriculture stats (volume/value)

Key fields:
- Year (refYear)
- Country (reporter, partner)
- Commodity code (HS Code)
- Import value (cifvalue), quantity (qty), weight (netWgt)
- Metadata & source flags

---

## 🔄 Data Pipeline

```
1. Fetch data via API / curl
2. Store in HDFS (Bronze)
3. Transform & clean via Spark (Silver)
4. Aggregate via Hive (Gold)
5. Register Hive tables
6. Visualize via Superset dashboard
```

---

## 📁 Folder Structure

```
/opt/bigdata/
├── docker-compose.yml
├── data/
│   ├── bronze/       # Raw CSVs
│   ├── silver/       # Cleaned Parquet
│   └── gold/         # Aggregated OLAP results
├── scripts/
│   ├── ingest.sh     # Data ingestion script
│   └── etl_spark.py  # Spark ETL transformation
└── logs/             # ETL logs
```

---

## 🔧 Technologies Used

| Component       | Function                            |
|----------------|-------------------------------------|
| Docker Compose | Virtual Hadoop cluster orchestration |
| Hive Metastore | Table metadata registry              |
| Spark Submit   | Run ETL batch jobs                   |
| Superset       | Build interactive dashboards         |
| Crontab        | Job automation                       |

---

## 🔍 Features

- ✅ Automated batch ingestion
- ✅ Clean & efficient Parquet transformation
- ✅ SQL-ready Hive tables
- ✅ Interactive dashboard via Superset
- ✅ ML-ready data for Spark MLlib

---

## 📅 Testing Strategy

| Test Type           | Purpose                                |
|---------------------|----------------------------------------|
| Unit Test           | Validate ETL script functions           |
| Integration Test    | Ingestion ➔ Spark ➔ Hive linkage         |
| Data Quality Test   | Handle nulls, duplicates, schema check |
| Performance Test    | Monitor batch execution times          |
| End-to-End Test     | Verify from fetch to Superset view     |

---

## 🤖 Advanced Analytics (Optional MLlib)

- Use **Spark MLlib regression** to predict future import volume
- Feature engineering to analyze influential factors
- Save prediction output to Hive Gold layer

---

## 🚀 Deployment Guide (Local)

1. **Install Docker Desktop**
2. Clone repository:
```bash
git clone https://github.com/sains-data/Analisis-Impor-Bahan-Pangan-dari-Global
cd Analisis-Impor-Bahan-Pangan-dari-Global
```
3. Launch Hadoop stack:
```bash
docker-compose up -d
```
4. Run pipeline:
```bash
bash scripts/ingest.sh
spark-submit scripts/etl_spark.py
```
5. Open Superset: `http://localhost:8088`

---

## 📄 License

MIT License — Academic purpose (Institut Teknologi Sumatera)  
Open for learning, with credit to original authors

---

## 📖 References

1. [UN Comtrade](https://comtrade.un.org/)
2. [FAOSTAT](https://www.fao.org/faostat)
3. [Apache Hadoop](https://hadoop.apache.org/)
4. [Apache Spark](https://spark.apache.org/)
5. [Apache Hive](https://hive.apache.org/)
6. [Apache Superset](https://superset.apache.org/)
