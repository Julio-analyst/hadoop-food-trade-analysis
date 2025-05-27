from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("BronzeLayerIngestion") \
        .getOrCreate()


    local_csv_path = "/opt/data_local/dataset.csv"


    hdfs_bronze_path = "hdfs://namenode:9000/data/bronze/imports_raw" 

    print(f"Reading CSV from {local_csv_path}")
    try:
        df_raw = spark.read.format("csv") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .load(local_csv_path)

        print(f"Saving raw data to HDFS Bronze layer: {hdfs_bronze_path}")
        df_raw.write.format("csv") \
            .option("header", "true") \
            .mode("overwrite") \
            .save(hdfs_bronze_path)

        print("Bronze layer ingestion complete.")
        df_raw.show(5)

    except Exception as e:
        print(f"Error during Bronze layer ingestion: {e}")

    spark.stop()

if __name__ == "__main__":
    main()