from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import os, sys, time

#create spark session
spark = SparkSession.builder.master("spark://192.168.0.1:7077").getOrCreate()
print("Spark Session Started")

#spark.conf.set("spark.executor.instances", 1)

#initialize dataset
q2=spark.read.parquet("./data/yellow_tripdata_2022-prwtoi6.parquet")
q2=q2.filter((month(col("tpep_pickup_datetime")) >= 1) & (month(col("tpep_pickup_datetime")) <= 6))

#add column for month
q2new = q2.withColumn("month", month("tpep_pickup_datetime"))

#sql query
q2new.createOrReplaceTempView("data")
query2 = spark.sql("""SELECT *, row_number() OVER (PARTITION BY month ORDER BY Tolls_amount) as Maxtolls
FROM data
WHERE Tolls_amount != 0 and Maxtolls == 1""")

start = time.time()
query2.show()
time_elapsed = time.time() - start

print("Time elapsed: ", time_elapsed) 