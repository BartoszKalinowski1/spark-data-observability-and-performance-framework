import sys
sys.path.append("../src")
from observability.metrics import (
    RowCountMetric, 
    NullRateMetric, 
    DistinctCountMetric
    )

def  test_row_count_metric(spark):

    df = spark.createDataFrame(
        [
            (1, "PL"),
            (2, "DE"),
            (3, "UK"),
        ],
        ["id", "country"]
    )

    metric = RowCountMetric()

    result = (
        df
        .agg(
            metric.get_expression()
        )
        .first()["row_count"]
    )

    assert result == 3

def test_null_rate_metric(spark):

    df = spark.createDataFrame(
        [
            (1, None),
            (2, "DE"),
            (3, "UK"),
            (3, None)
        ],
        ["id", "country"]
    )

    metric = NullRateMetric("country")

    result = (
        df.agg(
        metric.get_expression().alias("null_rate")
        )
        .first()["null_rate"]
    )

    assert result == 50

def test_distinct_count_metric(spark):

    df = spark.createDataFrame(
        [
            (1, "PL"),
            (2, "DE"),
            (3, "DE"),
        ],
        ["id", "country"]
    )

    metric = DistinctCountMetric("country")

    result = (
        df.agg(
        metric.get_expression().alias("distinct_count")
        )
        .first()["distinct_count"]
    )

    assert result == 2