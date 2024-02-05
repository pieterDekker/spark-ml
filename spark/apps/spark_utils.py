from pyspark.sql import SparkSession
from pyspark import SparkContext

def create_spark(app_name: str) -> (SparkSession, SparkContext):
    # .config('spark.jars', '/opt/spark-apps/postgresql-42.2.22.jar')\
  sql = SparkSession.builder\
    .appName(app_name)\
    .getOrCreate()
  sc = sql.sparkContext
  return sql,sc