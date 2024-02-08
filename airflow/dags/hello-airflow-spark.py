from airflow.models.dag import DAG

from airflow.operators.dummy_operator import DummyOperator

from airflow.operators.bash import BashOperator

from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

with DAG(
    "hello-airflow-spark",
) as dag:
    start = DummyOperator(task_id="start", dag=dag)
    submit_job = SparkSubmitOperator(
        task_id="submit_job",
        application="/opt/spark-apps/hello-spark.py",
        conn_id="spark_default",
        verbose=True,
        dag=dag,
    )
    end = DummyOperator(task_id="end", dag=dag)
    start >> submit_job >> end
