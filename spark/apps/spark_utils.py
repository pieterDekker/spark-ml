from pyspark.sql import SparkSession
from pyspark import SparkContext

def create_spark(app_name: str) -> SparkSession:
  session = SparkSession.builder\
    .appName(app_name)\
    .enableHiveSupport()\
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions") \
    .getOrCreate()
  return session

def create_database_parameters(database):
    url = f'jdbc:postgresql://demo-database:5432/{database}'
    properties = {
      'user': 'postgres',
      'password': 'casa1234',
      'driver': 'org.postgresql.Driver'
    }
    return url, properties
