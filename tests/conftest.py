import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    spark_session = SparkSession.getActiveSession()

    if spark_session  is None:
        spark_session = SparkSession.builder.getOrCreate()
    
    return spark_session
