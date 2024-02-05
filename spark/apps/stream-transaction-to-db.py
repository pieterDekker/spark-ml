import spark_utils

def main():
    ss, sc = spark_utils.create_spark('stream-transaction-to-db')
    df = ss.readStream.format('kafka') \
        .option('kafka.bootstrap.servers', 'kafka_box:9092') \
        .option('subscribe', 'test-topic') \
        .load()
    df.selectExpr('CAST(value AS STRING)')\
        .writeStream \
        .format('console') \
        .start() \
        .awaitTermination()

if __name__ == '__main__':
    main()