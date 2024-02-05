# Using Sparks machine learning for fraud detection

# General
Notes
- This setup was tested on Macos 13.0.1, on a 2021 Macbook Pro 14" with an M1 Pro 8 cores
- The resource requirements are significant. Be prepared to see usage of at least one full core, and 4GB+ of RAM

# Installation

## Pre requisites

* Docker installed

* Docker compose  installed

## Build the images


```sh
docker-compose build
```

## Start the services

```sh
docker-compose up -d
```

## Access the components

Access the Spark UI at http://localhost:8080/

Access the kafka admin UI at http://localhost:3030/


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
