from pyspark.sql import functions as F
from pyspark.sql.window import Window

class AnomalyDetectorRunner():

    def __init__(self, spark, METRIC_HISTORY_TABLE: str, PERFORMANCE_HISTORY_TABLE: str, ANOMALIES: list, PERFORMANCE_ANOMALY, thresholds: dict):
        self.spark = spark
        self.METRIC_HISTORY_TABLE = METRIC_HISTORY_TABLE
        self.PERFORMANCE_HISTORY_TABLE = PERFORMANCE_HISTORY_TABLE
        self.ANOMALIES = ANOMALIES
        self.PERFORMANCE_ANOMALY = PERFORMANCE_ANOMALY
        self.thresholds = thresholds
    
    def run_anomaly_detector(self):
        hisotry_df = self.spark.read.table(self.METRIC_HISTORY_TABLE)
        last_runtime_df = self.spark.read.table(self.PERFORMANCE_HISTORY_TABLE)

        runs = (
            hisotry_df.select("row_count", "null_rate_amount", "executed_at")
            .orderBy(F.col("executed_at").desc())
            .limit(2)
            .collect()
        )

        last_runtimes = (
                 last_runtime_df.select("runtime_seconds", "executed_at")
                 .orderBy(F.col("executed_at").desc())
                 .limit(11)
        )

        window = Window.orderBy(F.col("executed_at").desc())

        ranked = last_runtimes.withColumn(
            "rn",
            F.row_number().over(window)
        )

        last_runtime = (
                        ranked
                        .filter(F.col("rn") == 1)
                        .select("runtime_seconds")
                        .first()["runtime_seconds"]
                        )

        ten_last_runtimes_median = (
            ranked
            .filter(F.col("rn").between(2, 11))
            .agg(
                F.median("runtime_seconds").alias("median_runtime")
            )
            .first()["median_runtime"]
            )


        current_run = runs[0].asDict()
        previous_run = runs[1].asDict()

        results = []

        for anomaly_class in self.ANOMALIES:
            detector = anomaly_class(self.thresholds, current_run, previous_run)
            result = detector.look_for_anomaly()
            results.append(result)

        if ten_last_runtimes_median is not None:
            performance_run_time_detector = self.PERFORMANCE_ANOMALY(self.thresholds, ten_last_runtimes_median, last_runtime)

            results.append(performance_run_time_detector.look_for_anomaly())
        else:
            results.append({
                "anomaly_type": "run_time",
                "is_anomaly": False,
                "current_value": float(last_runtime),
                "previous_value": None,
                "percentage_change": None,
                "threshold": float(self.thresholds["runtime_performance"])
            })

        return results