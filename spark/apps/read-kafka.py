from pyspark.sql import SparkSession
from pyspark.sql.functions import col,date_format
import spark_utils

def main():
  sql,sc = spark_utils.create_spark('read-kafka')

  df = sql.readStream.format('kafka') \
    .option('kafka.bootstrap.servers', 'kafka_box:9092') \
    .option('subscribe', 'test-topic') \
    .load()
  
  df.selectExpr('CAST(key AS STRING)', 'CAST(value AS STRING)')\
    .writeStream \
    .format('console') \
    .start() \
    .awaitTermination()
  
if __name__ == '__main__':
  main()