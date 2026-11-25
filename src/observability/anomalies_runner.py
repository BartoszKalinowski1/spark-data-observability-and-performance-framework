from pyspark.sql import functions as F

class AnomalyDetectorRunner():

    def __init__(self, spark, METRIC_HISTORY_TABLE: str, ANOMALIES: list, anomalies_type: dict, thresholds: dict):
        self.spark = spark
        self.METRIC_HISTORY_TABLE = METRIC_HISTORY_TABLE
        self.ANOMALIES = ANOMALIES
        self.anomalies_type = anomalies_type
        self. thresholds = thresholds
    
    def run_anomaly_detector(self):
        hisotry_df = self.spark.read.table(self.METRIC_HISTORY_TABLE)

        runs = (
            hisotry_df.select("row_count", "null_rate_amount", "executed_at")
            .orderBy(F.col("executed_at").desc())
            .limit(2)
            .collect()
        )

        current_run = runs[0].asDict()
        previous_run = runs[1].asDict()

        results = []

        for anomaly_class in self.ANOMALIES:
            detector = anomaly_class(self.thresholds, current_run, previous_run)
            result = detector.look_for_anomaly()
            results.append(result)

        return results
