# Implementasi Ekosistem Hadoop untuk Analisis Perdagangan Internasional Bahan Pangan (2024)

## 📌 Deskripsi Proyek

Proyek ini bertujuan membangun sistem big data berbasis Hadoop untuk menganalisis data impor bahan pangan Indonesia dari berbagai negara, menggunakan pendekatan batch processing dan arsitektur Medallion (Bronze, Silver, Gold). Sistem dirancang untuk memproses dataset besar dari UN Comtrade dan FAOSTAT, dengan pipeline data yang mencakup ingestion, transformasi, agregasi, dan visualisasi.

## 🧑‍💻 Tim Pengembang

Kelompok 13 - Institut Teknologi Sumatera (Program Studi Sains Data)

- Rangga Adi Putra (121450106)
- Cyntia Kristina Sidauruk (122450023)
- Azizah Kusumah Putri (122450068)
- Farrel Julio Akbar (122450110)

---

## 🗂 Arsitektur Sistem

Sistem dibangun menggunakan **Apache Hadoop Stack**:

- **HDFS** – Penyimpanan terdistribusi untuk semua lapisan data
- **Apache Spark** – Proses ETL dan analitik batch
- **Apache Hive** – SQL engine untuk eksplorasi dan query analitik
- **Apache Superset** – Dashboard interaktif
- **Docker Compose** – Orkestrasi cluster lokal
- **Airflow / Crontab** – Penjadwalan ingestion dan transformasi

### 🔄 Medallion Architecture

| Layer  | Tujuan                                                                 | Format Data       | Tools              |
|--------|------------------------------------------------------------------------|-------------------|--------------------|
| Bronze | Menyimpan data mentah dari sumber eksternal                           | CSV / JSON        | HDFS               |
| Silver | Data bersih & distandarisasi, siap analisis                           | Parquet / ORC     | Spark, Hive        |
| Gold   | Data agregasi akhir, siap dianalisis atau divisualisasikan            | Parquet / ORC     | Hive, Superset     |

---

## 🧬 Dataset

Sumber: [UN Comtrade](https://comtrade.un.org/), [FAOSTAT](https://www.fao.org/faostat)

Data mencakup:

- Tahun transaksi (refYear)
- Negara pelapor dan mitra dagang
- Deskripsi dan kode komoditas (HS Code)
- Nilai dan volume impor (qty, netWgt, cifvalue)
- Estimasi dan metadata impor

---

## ⚙️ Pipeline Alur Data

```
1. Fetch CSV dari UN Comtrade (curl/API)
2. Upload ke HDFS (Bronze Layer)
3. Transformasi dan validasi (Spark - Silver Layer)
4. Agregasi OLAP (Spark/Hive - Gold Layer)
5. Registrasi tabel Hive
6. Visualisasi dengan Apache Superset
```

---

## 🏗️ Implementasi Sistem

### Struktur Folder

```
/opt/bigdata/
├── docker-compose.yml
├── data/
│   ├── bronze/       # Raw CSV
│   ├── silver/       # Cleaned data (Parquet)
│   └── gold/         # Aggregated data
├── scripts/
│   ├── ingest.sh     # Script pengambilan data
│   └── etl_spark.py  # Script transformasi Spark
└── logs/             # Log ETL
```

### Teknologi Utama

| Komponen         | Fungsi                                 |
|------------------|-----------------------------------------|
| Docker + Compose | Virtualisasi cluster Hadoop             |
| Hive Metastore   | Metadata tabel Hive                     |
| Spark Submit     | Menjalankan job batch ETL               |
| Superset         | Visualisasi data impor                  |
| Crontab / Airflow| Penjadwalan batch job                   |

---

## 🔍 Fitur Utama

- 🔄 Otomatisasi pipeline batch
- 🧼 Data cleaning & transformasi format Parquet
- 📊 Visualisasi interaktif melalui Superset
- 🧠 Integrasi Spark MLlib untuk analisis prediktif
- 🔎 SQL query melalui Hive

---

## 🧪 Pengujian

| Jenis Tes             | Tujuan                                                   |
|------------------------|----------------------------------------------------------|
| Unit Test             | Validasi skrip ETL per modul                              |
| Integration Test      | Ingestion → HDFS → Spark → Hive                           |
| Data Quality Test     | Duplikasi, nilai null, dan validasi skema                 |
| Performance Test      | Waktu eksekusi batch ingestion & transformasi            |
| End-to-End Test       | Alur ingestion sampai dashboard Superset                 |

---

## 📈 Analitik Lanjutan (MLlib)

Model regresi menggunakan Spark MLlib digunakan untuk:

- 🔮 Memprediksi volume impor berdasarkan tren historis
- 🧾 Menilai fitur penting yang memengaruhi nilai impor

Output prediksi disimpan di Hive/Gold Layer untuk visualisasi lanjutan.

---

## 🚀 Cara Menjalankan (Local Deployment)

1. **Install Docker Desktop + WSL2**
2. Clone repositori ini:
   ```bash
   git clone https://github.com/sains-data/Analisis-Impor-Bahan-Pangan-dari-Global
   cd Analisis-Impor-Bahan-Pangan-dari-Global
   ```
3. Jalankan cluster Hadoop lokal:
   ```bash
   docker-compose up -d
   ```
4. Eksekusi pipeline:
   ```bash
   bash scripts/ingest.sh
   spark-submit scripts/etl_spark.py
   ```
5. Akses Superset di `http://localhost:8088` untuk visualisasi

---

## 🧾 Lisensi

Proyek ini dikembangkan untuk keperluan akademik di Institut Teknologi Sumatera. Bebas digunakan untuk pembelajaran dan riset dengan mencantumkan kredit kepada tim pengembang.

---

## 📚 Referensi

1. [UN Comtrade](https://comtrade.un.org/)
2. [FAOSTAT](https://www.fao.org/faostat)
3. [Apache Hadoop](https://hadoop.apache.org/)
4. [Apache Spark](https://spark.apache.org/)
5. [Apache Hive](https://hive.apache.org/)
6. [Apache Superset](https://superset.apache.org/)
