from airflow.models.dag import DAG

from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.empty import EmptyOperator

with DAG(
    "logistic-regression-pipeline",
) as dag:
    keyspace = 'transactions'
    table = 'limit20'
    data_transformation_model_path = "models/transform-model"
    transformed_data_path = "datasets/transformed-dataset.parquet"
    logistic_regression_model_path = "models/logistic-regression-model"

    create_data_transformation_model = SparkSubmitOperator(
        task_id="submit_create_data_transformation_model_job",
        application="/opt/spark-apps/create-data-transformation-model.py",
        conn_id="spark_default",
        verbose=True,
        dag=dag,
        packages="com.datastax.spark:spark-cassandra-connector_2.12:3.4.1",
        conf={"spark.sql.extensions": "com.datastax.spark.connector.CassandraSparkExtensions"},
        application_args=['create-data-transformation-model', keyspace, table, data_transformation_model_path]
    )

    transform_data = SparkSubmitOperator(
        task_id="submit_transform_data_job",
        application="/opt/spark-apps/transform-data.py",
        conn_id="spark_default",
        verbose=True,
        dag=dag,
        packages="com.datastax.spark:spark-cassandra-connector_2.12:3.4.1",
        conf={"spark.sql.extensions": "com.datastax.spark.connector.CassandraSparkExtensions"},
        application_args=['transform-data', keyspace, table, data_transformation_model_path, transformed_data_path]
    )

    train_logistic_regression_model = SparkSubmitOperator(
        task_id="submit_train_logistic_regression_model_job",
        application="/opt/spark-apps/train-logistic-regression-model.py",
        conn_id="spark_default",
        verbose=True,
        dag=dag,
        application_args=['train-logistic-regression-model', transformed_data_path, logistic_regression_model_path]
    )

    evaluate_model = EmptyOperator(task_id="evaluate_model", dag=dag)

    create_data_transformation_model >> transform_data >> train_logistic_regression_model >> evaluate_model
