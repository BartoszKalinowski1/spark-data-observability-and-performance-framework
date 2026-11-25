from abc import ABC, abstractmethod
from pyspark.sql import functions as F

class Metric(ABC):

    def __init__(self, metric_name):
        self.metric_name = metric_name

    @abstractmethod
    def calculate(self, df):
        pass

class RowCountMetric(Metric):

    def __init__(self):
        super().__init__(metric_name="Row count")
    
    def calculate(self, df):
        return df.count()


class NullRateMetric(Metric):

    def __init__(self, column_name):
        super().__init__(metric_name="Null rate")
        self.column_name = column_name

    def calculate(self, df):
        """
        Returns specific column null rate (%).  
        """
        return (df.filter(F.col(self.column_name).isNull()).count() / df.count())*100

class DistinctCountMetric(Metric):

    def __init__(self, column_name):
        super().__init__(metric_name="Distinct row count")
        self.column_name = column_name

    def calculate(self, df):
        return df.select(self.column_name).distinct().count()
        