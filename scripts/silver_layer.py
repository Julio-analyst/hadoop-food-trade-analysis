from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def main():
    spark = SparkSession.builder \
        .appName("SilverLayerProcessing") \
        .getOrCreate()

    hdfs_bronze_path = "hdfs://namenode:9000/data/bronze/imports_raw"

    hdfs_silver_path = "hdfs://namenode:9000/data/silver/imports_clean" 

    print(f"Reading raw data from HDFS Bronze layer: {hdfs_bronze_path}")
    try:
        df_bronze = spark.read.format("csv") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .load(hdfs_bronze_path)

        print("Performing cleaning and transformation...")

        df_cleaned = df_bronze.dropDuplicates() \
                               .na.fill("N/A", subset=[col_name for col_name, dtype in df_bronze.dtypes if dtype == 'string']) \
                               .na.fill(0, subset=[col_name for col_name, dtype in df_bronze.dtypes if dtype in ['int', 'double', 'long', 'float']])


        print(f"Saving cleaned data to HDFS Silver layer (Parquet): {hdfs_silver_path}")
        df_cleaned.write.format("parquet") \
            .mode("overwrite") \
            .save(hdfs_silver_path)

        print("Silver layer processing complete.")
        df_cleaned.show(5)
        df_cleaned.printSchema()

    except Exception as e:
        print(f"Error during Silver layer processing: {e}")

    spark.stop()

if __name__ == "__main__":
    main()