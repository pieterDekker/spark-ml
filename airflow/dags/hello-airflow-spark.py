from airflow.models.dag import DAG

from airflow.operators.empty import EmptyOperator

from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

with DAG(
    "hello-airflow-spark",
) as dag:
    start = EmptyOperator(task_id="start", dag=dag)
    submit_job = SparkSubmitOperator(
        task_id="submit_job",
        application="/opt/spark-apps/hello-spark.py",
        conn_id="spark_default",
        verbose=True,
        dag=dag,
    )
    end = EmptyOperator(task_id="end", dag=dag)
    start >> submit_job >> end
