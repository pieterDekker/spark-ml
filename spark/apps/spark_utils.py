from pyspark.sql import SparkSession
from pyspark import SparkContext

def create_spark(app_name: str) -> SparkSession:
    # .config("spark.cassandra.auth.username", "my_username") \
    # .config("spark.cassandra.auth.password", "my_password") \
  session = SparkSession.builder\
    .appName(app_name)\
    .enableHiveSupport()\
    .config("spark.sql.warehouse.dir", "/opt/spark-data/warehouse")\
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions") \
    .getOrCreate()
  return session

def add_minio_config(spark_context: SparkContext):
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.access.key", "minio")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "minio123")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://minio:9000")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "true")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.attempts.maximum", "1")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.connection.establish.timeout", "5000")
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.connection.timeout", "10000")

def create_database_parameters(database):
    url = f'jdbc:postgresql://demo-database:5432/{database}'
    properties = {
      'user': 'postgres',
      'password': 'casa1234',
      'driver': 'org.postgresql.Driver'
    }
    return url, properties
