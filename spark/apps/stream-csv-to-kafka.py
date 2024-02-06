from pyspark.sql.functions import to_json, struct, date_format
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, TimestampType
import spark_utils
import schemas

def main():
    session, _ = spark_utils.create_spark('stream-csv-to-kafka')

    df = session.read \
        .schema(schemas.transactions_dataset_schema()) \
        .format('csv') \
        .option('header', 'true') \
        .option('path', '/opt/spark-data/transactions-dataset.csv') \
        .load()

    df = df\
        .select(list(set(df.columns) - {'step', 'fraud'}))\
        .withColumn('date', date_format('date', "yyyy-MM-dd'T'HH:mm:ssZZZZZ"))\
        .withColumn('key', df['id'].cast('string').alias('key')) \
        .select('key', to_json(struct("*")).alias("value"))

    df\
        .write \
        .mode('append') \
        .format('kafka') \
        .option('kafka.bootstrap.servers', 'kafka_box:9092') \
        .option('topic', 'transactions') \
        .save()
    
if __name__ == '__main__':
    main()