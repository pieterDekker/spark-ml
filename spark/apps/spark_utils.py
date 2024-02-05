from pyspark.sql import SparkSession
from pyspark import SparkContext

def create_spark(app_name: str) -> (SparkSession, SparkContext):
  session = SparkSession.builder\
    .appName(app_name)\
    .getOrCreate()
  context = session.sparkContext
  return session,context

def create_database_parameters(database):
    url = f'jdbc:postgresql://demo-database:5432/{database}'
    properties = {
      'user': 'postgres',
      'password': 'casa1234',
      'driver': 'org.postgresql.Driver'
    }
    return url, properties