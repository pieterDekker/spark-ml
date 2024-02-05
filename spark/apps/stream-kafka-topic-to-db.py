import spark_utils
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *

def main():
    spark_session, _ = spark_utils.create_spark('stream-transaction-to-db')
    df = spark_session \
        .readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers', 'kafka_box:9092') \
        .option('subscribe', 'transactions') \
        .option('startingOffsets', 'earliest') \
        .load()

    schema = StructType([
        StructField('id', IntegerType()),
        StructField('date', TimestampType()),
        StructField('customer', StringType()),
        StructField('age', StringType()),
        StructField('gender', StringType()),
        StructField('zipCodeOri', StringType()),
        StructField('merchant', StringType()),
        StructField('zipMerchant', StringType()),
        StructField('category', StringType()),
        StructField('amount', DoubleType()),
    ])

    url, properties = spark_utils.create_database_parameters('transactions')
    df\
        .withColumn('value', df.value.cast('string'))\
        .withColumn('value', from_json('value', schema))\
        .select(col('value.*')) \
        .writeStream \
        .foreachBatch(lambda df, _: df.write.jdbc(url=url,table='transactions',properties=properties))\
        .start() \
        .awaitTermination()

if __name__ == '__main__':
    main()