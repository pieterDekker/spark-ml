FROM apache/airflow:2.8.1

USER root
RUN apt-get update
RUN apt-get install default-jdk curl -y

WORKDIR /downloads

# Download Spark
ARG SPARK_VERSION
ARG HADOOP_VERSION
ENV SPARK_VERSION=${SPARK_VERSION}
ENV HADOOP_VERSION=${HADOOP_VERSION}
ENV SPARK_HOME=/opt/spark
RUN curl -O https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Install Spark
RUN mkdir -p /opt/spark
RUN tar -xvf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /opt/spark --strip-components=1
RUN rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz
ENV PATH $PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

WORKDIR /

USER airflow

# Install additional packages
RUN pip install apache-airflow-providers-apache-spark
