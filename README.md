# Using Sparks machine learning for fraud detection

# General
Notes
- This setup was tested on Macos 13.0.1, on a 2021 Macbook Pro 14" with an M1 Pro 8 cores
- The resource requirements are significant. Be prepared to see usage of at least one full core, and 4GB+ of RAM

# Installation

## Pre requisites

* Docker installed

* Docker compose v2 installed

## Build the images


```sh
docker compose build
```

## Start the services

```sh
docker compose -f airflow-compose.yaml -f docker-compose.yml up -d
```

## Access the components

Access the Spark UI at http://localhost:8080/

Access the kafka admin UI at http://localhost:3030/

Access the Airflow UI at http://localhost:18080/

# The spark jobs

An overview of the spark jobs. All jobs can be submitted from the spark container.

To run a shell in one of the worker containers:
```sh
docker exec -it spark-watchlist-spark-worker-a-1 /bin/bash
```
You will be in the `/opt/spark` directory. Run `cd bin` to descend into the `/opt/spark/bin` directory to run the `submit-job` command.

## stream-csv-to-kafka

```sh
./spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 --driver-memory 1G --executor-memory 1G /opt/spark-apps/stream-csv-to-kafka.py
```

This will start streaming the contents of `spark/data/transactions-dataset.csv` to kafka

# Sources and credits

Used this dataset for annotated transactions: https://www.kaggle.com/datasets/ealaxi/banksim1

Used https://github.com/mvillarrealb/docker-spark-cluster as starting point for the cluster setup

# Ideas and Todos

## Todo
- [ ] Use Apache Hive as data warehouse
- [x] Use Apache Cassandra as data warehouse _High memory usage, not ideal, but works for now_
- [x] Extract separate Spark steps for data preparation and model fitting
- [x] Make the parameters for the spark apps injectable
- [ ] Implement model validation
- [ ] Use Mleap as format for model
- [ ] Schedule monthly reports and backfill
- [ ] Use cross validations for finetuning
- [ ] Implement streaming classifier in Spark
- [ ] Fix airflow scheduler resource usage, see [here](https://stackoverflow.com/questions/42419834/airbnb-airflow-using-all-system-resources)

## Longlist
- [ ] streaming classifier should be perpetual job (remote supervisord style?)
- [ ] everything in k8s under tf files
- [ ] Use Parquet for transaction dataset?
- [ ] Use Scylladb for transaction dataset? Makes it faster to sample when the dataset grows very large
- [ ] Use dvc for dataset versioning?
- [ ] Data exploration: feature ranking and selection
- [ ] Use enterprise Kafka solutions: kafka connect for streaming to and from kafka when no other action is needed, Avro for message schemas

## Dead list
    Features that did not make it  (yet)
- [ ] use S3 compatible storage backend for model storage

    _using the hadoop-aws and aws-java-sdk-core jars should work, but doesn't (compiled hadoop version is 3.3.4, according to spark context)_