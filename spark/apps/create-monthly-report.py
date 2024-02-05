import spark_utils
from pyspark.sql.functions import date_format, count, sum
def main():
    start_date = '2023-01-01'
    end_date = '2023-02-01'
    session, _ = spark_utils.create_spark('create-monthly-report')

    url, properties = spark_utils.create_database_parameters('transactions')

    df = session.read.jdbc(url=url, table='transactions', properties=properties)

    df = df\
        .withColumn('month', date_format('date', 'yyyy-MM'))\
        .filter(f'date >= "{start_date}" and date < "{end_date}"')\
        .groupBy('month')\
        .agg(
            count('id').alias('total_transactions'),
            sum('amount').alias('total_amount')
        )

    df.write.jdbc(url=url, table='monthly_report', mode='overwrite', properties=properties)

if __name__ == '__main__':
    main()
