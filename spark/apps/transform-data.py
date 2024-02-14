import argparse
from os import path

import spark_utils
import schemas

from pyspark.sql import SparkSession

from pyspark.ml.pipeline import PipelineModel

import mleap.pyspark
from mleap.pyspark.spark_support import SimpleSparkSerializer

def main(app_name, keyspace, table, model_path, transformed_data_path):
    session: SparkSession
    session = spark_utils.create_spark(app_name)

    df = session.read \
        .format('org.apache.spark.sql.cassandra') \
        .options(keyspace=keyspace, table=table) \
        .load()

    transform_model: PipelineModel = PipelineModel.load(path.join('hdfs://namenode:8020/',model_path))
    transform_model.transform(df).write.mode('overwrite').parquet(path.join('hdfs://namenode:8020/',transformed_data_path))

    session.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('app_name', help='The name of the application')
    parser.add_argument('keyspace', help='The keyspace to use')
    parser.add_argument('table', help='The table to use')
    parser.add_argument('model_path', help='The path to save the model')
    parser.add_argument('transformed_data_path', help='The path to save the transformed data')

    main(**vars(parser.parse_args()))
