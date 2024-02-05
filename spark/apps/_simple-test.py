from pyspark.sql import SparkSession
from pyspark.sql.functions import col,date_format
import spark_utils

def main():
  sql,_ = spark_utils.create_spark('simple-test')

  df = sql.createDataFrame([(key, 'fvalue{key}') for key in range(0,1000)], ['key', 'value'])
  df.rollup('key').count().show()
  
  
if __name__ == '__main__':
  main()