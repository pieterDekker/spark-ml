import spark_utils
from pyspark import SparkContext
from pyspark.sql import DataFrame
from pyspark.sql.types import IntegerType

def main():
    context: SparkContext
    _, context = spark_utils.create_spark('stream-csv-to-kafka')

    df: DataFrame
    rdd = context.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    df = rdd.toDF(schema=IntegerType())

    df.show()
    df.agg({'value': 'sum'}).show()

if __name__ == '__main__':
    main()
