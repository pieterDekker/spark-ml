from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, TimestampType

def transactions_dataset_schema():
    return StructType([
        StructField('id', IntegerType()),
        StructField('date', TimestampType()),
        StructField('step', IntegerType()),
        StructField('customer', StringType()),
        StructField('age', StringType()),
        StructField('gender', StringType()),
        StructField('zipCodeOri', StringType()),
        StructField('merchant', StringType()),
        StructField('zipMerchant', StringType()),
        StructField('category', StringType()),
        StructField('amount', DoubleType()),
        StructField('fraud', IntegerType())
    ])