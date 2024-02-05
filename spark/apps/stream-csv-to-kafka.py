from pyspark.sql.functions import to_json, struct, to_varchar

import spark_utils

def main():
    sql, sc = spark_utils.create_spark('stream-csv-to-kafka')
    df = sql.read \
        .schema('id INT, step INT, customer STRING, age STRING, gender STRING, zipCodeOri STRING, merchant STRING, zipMerchant STRING, category STRING, amount DOUBLE, fraud INT') \
        .format('csv') \
        .option('header', 'true') \
        .option('path', '/opt/spark-data/first-20.csv') \
        .load()
    df.printSchema()

    df\
        .withColumn('key', df['id'].cast('string').alias('key')) \
        .select('key', to_json(struct("*")).alias("value")) \
        .write \
        .mode('append') \
        .format('kafka') \
        .option('kafka.bootstrap.servers', 'kafka_box:9092') \
        .option('topic', 'test-topic') \
        .save()
    
    # df\
    #     .select(to_json(struct("*")).alias("value")) \
    #     .writeTo \
    #     .using('kafka') \
    #     .option('kafka.bootstrap.servers', 'localhost:9092') \
    #     .option('topic', 'test-topic') \
    #     .create()

if __name__ == '__main__':
    main()