from abc import ABC, abstractmethod
from pyspark.sql import functions as F

class Metric(ABC):

    def __init__(self, metric_name):
        self.metric_name = metric_name

    @abstractmethod
    def get_expression(self):
        pass

class RowCountMetric(Metric):

    def __init__(self):
        super().__init__(metric_name="Row count")
    
    def get_expression(self):
        return F.count("*").alias("row_count")


class NullRateMetric(Metric):

    def __init__(self, column_name):
        super().__init__(metric_name="Null rate")
        self.column_name = column_name

    def get_expression(self):
        """
        Returns specific column null rate (%).  
        """
        return (
            F.sum(
                F.when(F.col(self.column_name).isNull(), 1).otherwise(0)
            ) / F.count("*")
            * 100
        ).alias(f"null_rate_{self.column_name}")

class DistinctCountMetric(Metric):

    def __init__(self, column_name):
        super().__init__(metric_name="Distinct row count")
        self.column_name = column_name

    def get_expression(self):
        return (
            F.countDistinct(F.col(self.column_name))
        ).alias(f"distinct_count_{self.column_name}")
        