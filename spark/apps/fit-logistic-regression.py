import spark_utils
import schemas

from pyspark.sql import SparkSession

from pyspark.ml.feature import VectorAssembler, OneHotEncoder, StringIndexer

from pyspark.ml.classification import LogisticRegression
from pyspark.ml.pipeline import Pipeline

def main():
    session: SparkSession
    session, _ = spark_utils.create_spark('fit-logistic-regression-model')

    df = session.read \
        .schema(schemas.transactions_dataset_schema()) \
        .format('csv') \
        .option('header', 'true') \
        .option('path', '/opt/spark-data/transactions-dataset.csv') \
        .load()

    categorical_column_names = ['customer','age', 'gender', 'merchant', 'category']
    string_indexed_column_names = [f'{column}_numeric' for column in categorical_column_names]
    encoded_column_names = [f'{column}_encoded' for column in string_indexed_column_names]

    feature_column_names = ['amount'] + encoded_column_names

    stringIndexer = StringIndexer(inputCols=categorical_column_names, outputCols=string_indexed_column_names)

    encoder = OneHotEncoder(inputCols=string_indexed_column_names, outputCols=encoded_column_names)

    assembler = VectorAssembler(inputCols=feature_column_names, outputCol='features')

    transform_pipeline = Pipeline(stages=[stringIndexer, encoder, assembler])

    transform_model = transform_pipeline.fit(df)
    transformed_df = transform_model.transform(df)

    train, test = transformed_df.randomSplit([0.7, 0.3])
    
    lr_estimator = LogisticRegression(featuresCol='features', labelCol='fraud')
    lr_model = lr_estimator.fit(train)

    results = lr_model.transform(test)
    results.select('fraud','prediction').show()

    transform_model.write().overwrite().save('/opt/spark-data/models/logistic-regression-transform')
    lr_model.write().overwrite().save('/opt/spark-data/models/logistic-regression-model')

    session.stop()

if __name__ == '__main__':
    main()