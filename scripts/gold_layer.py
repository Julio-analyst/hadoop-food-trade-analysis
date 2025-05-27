from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, col, year

def main():
    spark = SparkSession.builder \
        .appName("GoldLayerAggregation") \
        .getOrCreate()

    hdfs_silver_path = "hdfs://namenode:9000/data/silver/imports_clean"


    hdfs_gold_path = "hdfs://namenode:9000/data/gold/imports_aggregated" 

    print(f"Reading cleaned data from HDFS Silver layer: {hdfs_silver_path}")
    try:
        df_silver = spark.read.format("parquet").load(hdfs_silver_path)

        print("Performing aggregation...")

        df_aggregated = df_silver.groupBy("reporterDesc", "refYear", "cmdDesc") \
            .agg(sum("cifvalue").alias("total_cifvalue"),
                 sum("qty").alias("total_quantity")) \
            .orderBy("reporterDesc", "refYear", "cmdDesc")

        print(f"Saving aggregated data to HDFS Gold layer (Parquet): {hdfs_gold_path}")
        df_aggregated.write.format("parquet") \
            .mode("overwrite") \
            .save(hdfs_gold_path)

        print("Gold layer aggregation complete.")
        df_aggregated.show(10)

    except Exception as e:
        print(f"Error during Gold layer aggregation: {e}")

    spark.stop()

if __name__ == "__main__":
    main()