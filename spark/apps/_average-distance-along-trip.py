from pyspark.sql import SparkSession
from pyspark.sql.functions import col,date_format
import spark_utils

def main():
  sql,_ = spark_utils.create_spark()

  df = sql\
    .read\
    .format('jdbc')\
    .option('url', 'jdbc:postgresql://demo-database:5432/mta_data')\
    .option('driver', 'org.postgresql.Driver')\
    .option('dbtable', 'mta_reports')\
    .option('user', 'postgres')\
    .option('password', 'casa1234')\
    .load()
  
  df.agg({'distance_along_trip': 'avg'}).show()
  
if __name__ == '__main__':
  main()