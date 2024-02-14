import argparse
from os import path

import sys
import spark_utils
import schemas

from pyspark.sql import SparkSession
from pyspark.sql import Row

from pyspark.ml.feature import VectorAssembler, OneHotEncoder, StringIndexer

from pyspark.ml.pipeline import Pipeline

def main(app_name, keyspace, table, model_path):
    session: SparkSession
    session = spark_utils.create_spark(app_name)

    df = session.read \
        .format('org.apache.spark.sql.cassandra') \
        .options(keyspace=keyspace, table=table) \
        .load()

    # TODO: inject columns to use
    # TODO: determine which columns are categorical based on data types
    categorical_column_names = ['customer','age', 'gender', 'merchant', 'category']
    string_indexed_column_names = [f'{column}_numeric' for column in categorical_column_names]
    encoded_column_names = [f'{column}_encoded' for column in string_indexed_column_names]

    feature_column_names = ['amount'] + encoded_column_names

    stringIndexer = StringIndexer(inputCols=categorical_column_names, outputCols=string_indexed_column_names)

    encoder = OneHotEncoder(inputCols=string_indexed_column_names, outputCols=encoded_column_names)

    assembler = VectorAssembler(inputCols=feature_column_names, outputCol='features')

    transform_pipeline = Pipeline(stages=[stringIndexer, encoder, assembler])

    transform_model = transform_pipeline.fit(df)
    transform_model.write().overwrite().save(path.join('hdfs://namenode:8020/',model_path))

    session.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('app_name', help='The name of the application')
    parser.add_argument('keyspace', help='The keyspace to use')
    parser.add_argument('table', help='The table to use')
    parser.add_argument('model_path', help='The path to save the model')

    main(**vars(parser.parse_args()))
