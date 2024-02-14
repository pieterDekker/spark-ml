import spark_utils
import argparse
from os import path

from pyspark.sql import SparkSession

from pyspark.ml.classification import LogisticRegression

def main(app_name, model_path, transformed_data_path):
    session: SparkSession
    session, _ = spark_utils.create_spark(app_name)

    transformed_df = session.read \
        .parquet(path.join('hdfs://namenode:8020/', transformed_data_path))

    train, _ = transformed_df.randomSplit([0.7, 0.3])

    lr_estimator = LogisticRegression(featuresCol='features', labelCol='fraud')
    lr_model = lr_estimator.fit(train)

    lr_model.save(path.join('hdfs://namenode:8020/', model_path))

    session.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('app_name', help='The name of the application')
    parser.add_argument('transformed_data_path', help='The path to save the transformed data')
    parser.add_argument('model_path', help='The path to save the model')

    main(**vars(parser.parse_args()))
