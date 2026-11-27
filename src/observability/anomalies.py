from abc import ABC, abstractmethod

class AnomalyDetector(ABC):
    def __init__(self, threshold: dict):
        self.threshold = threshold
    
    @abstractmethod
    def look_for_anomaly(self):
        pass

class RowCountAnomalyDetector(AnomalyDetector):
    def __init__(self, threshold: dict, current_run: dict, previous_run: dict):
        super().__init__(threshold = threshold["row_count"])
        self.current_run = current_run
        self.previous_run = previous_run

    def look_for_anomaly(self):
        previous_row_count = self.previous_run["row_count"]
        current_run_count = self.current_run["row_count"]

        difference = (
            (current_run_count - previous_row_count) / previous_row_count
            ) * 100
        
        result = abs(difference) > self.threshold

        return {
                "anomaly_type": "row_count",
                "is_anomaly": result,
                "current_value": float(current_run_count),
                "previous_value": float(previous_row_count),
                "percentage_change": float(difference),
                "threshold": float(self.threshold)
            }   

    
class NullRateAnomalyDetector(AnomalyDetector):

    def __init__(self, threshold: dict, current_run: dict, previous_run: dict):
        super().__init__(threshold = threshold["null_rate"])
        self.current_run = current_run
        self.previous_run = previous_run
    
    def look_for_anomaly(self):

        current_null_rate = self.current_run["null_rate_amount"]
        previous_null_rate = self.previous_run["null_rate_amount"]
        
        result = current_null_rate > self.threshold

        return {
                "anomaly_type": "null_rate",
                "is_anomaly": result,
                "current_value": float(current_null_rate),
                "previous_value": float(previous_null_rate),
                "percentage_change": None,
                "threshold": float(self.threshold)
            }


class PerformanceRunTimeAnomalyDetector(AnomalyDetector):

    def __init__(self, threshold: dict, ten_last_runtime_median: float, last_runtime: float):
        super().__init__(threshold = threshold["runtime_performance"])
        self.ten_last_runtime_median = ten_last_runtime_median
        self.last_runtime = last_runtime

    def look_for_anomaly(self):

        if self.ten_last_runtime_median == 0:
            return {
                "anomaly_type": "run_time",
                "is_anomaly": False,
                "current_value": float(self.last_runtime),
                "previous_value": 0.0,
                "percentage_change": None,
                "threshold": float(self.threshold)
            }


        difference = (
            (self.last_runtime - self.ten_last_runtime_median) / self.ten_last_runtime_median
                      ) * 100
        result = difference > self.threshold

        return {
                "anomaly_type": "run_time",
                "is_anomaly": result,
                "current_value": float(self.last_runtime),
                "previous_value": float(self.ten_last_runtime_median),
                "percentage_change": float(difference),
                "threshold": float(self.threshold)
            }
