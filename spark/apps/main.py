from pyspark.sql.functions import col,date_format
import spark_utils

def main():
  url = 'jdbc:postgresql://demo-database:5432/mta_data'
  properties = {
    'user': 'postgres',
    'password': 'casa1234',
    'driver': 'org.postgresql.Driver'
  }
  file = '/opt/spark-data/MTA_2014_08_01.csv'
  sql,sc = spark_utils.create_spark('persist-mta-data')

  df = sql.read.load(file,format = 'csv', inferSchema='true', sep='|', header='true'
      ) \
      .withColumn('report_hour',date_format(col('time_received'),'yyyy-MM-dd HH:00:00')) \
      .withColumn('report_date',date_format(col('time_received'),'yyyy-MM-dd'))
  
  # Filter invalid coordinates
  df.where('latitude <= 90 AND latitude >= -90 AND longitude <= 180 AND longitude >= -180') \
    .where('latitude != 0.000000 OR longitude !=  0.000000 ') \
    .write \
    .jdbc(url=url, table='mta_reports', mode='append', properties=properties)
  
if __name__ == '__main__':
  main()