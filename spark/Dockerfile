FROM openjdk:11.0.11-jre-slim-buster as builder

RUN apt update -y
# pyenv dependencies
RUN apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
# pyspark dependencies
RUN apt-get update && apt-get install -y curl vim wget software-properties-common ssh net-tools ca-certificates

# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ARG SPARK_VERSION
ARG HADOOP_VERSION

ENV SPARK_VERSION=${SPARK_VERSION}
ENV HADOOP_VERSION=${HADOOP_VERSION}
ENV SPARK_HOME=/opt/spark
ENV PYTHONHASHSEED=1

RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"
# COPY ./spark-3.5.0-bin-hadoop3.tgz apache-spark.tgz
RUN mkdir -p /opt/spark
RUN tar -xf apache-spark.tgz -C /opt/spark --strip-components=1
RUN rm apache-spark.tgz

ENV PYENV_ROOT=/opt/.pyenv

RUN git clone https://github.com/pyenv/pyenv.git ${PYENV_ROOT}
ENV PATH=${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}
# Specific version of python needed to match the version of python used in airflow (which is the driver in case of spark-submit DAGs)
RUN pyenv install 3.8.18
RUN pyenv global 3.8.18

# WORKDIR /opt/spark-apps
RUN pip install pyspark
RUN pip install mleap
RUN pip install apache-airflow
RUN pip install apache-airflow-providers-apache-spark
RUN pip install numpy
RUN pip install matplotlib
RUN pip install scipy
RUN pip install pandas
RUN pip install simpy

RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1

FROM builder as apache-spark

WORKDIR /opt/spark

ENV SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=8080 \
SPARK_LOG_DIR=/opt/spark/logs \
SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=8080 \
SPARK_WORKER_PORT=7000 \
SPARK_MASTER="spark://spark-master:7077" \
SPARK_WORKLOAD="master"

EXPOSE 8080 7077 7000

RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG

COPY start-spark.sh /

CMD ["/bin/bash", "/start-spark.sh"]
