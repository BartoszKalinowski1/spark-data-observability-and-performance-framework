from abc import ABC, abstractmethod

class AnomalyDetector(ABC):
    def __init__(self, threshold: dict, current_run: dict, previous_run: dict):
        self.threshold = threshold
        self.current_run = current_run
        self.previous_run = previous_run
    
    @abstractmethod
    def look_for_anomaly(self):
        pass

class RowCountAnomalyDetector(AnomalyDetector):
    def __init__(self, threshold: dict, current_run: str, previous_run: str):
        super().__init__(threshold = threshold["row_count"], current_run = current_run, previous_run = previous_run)

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
                "current value": current_run_count,
                "previous_value": previous_row_count,
                "percentage_change": difference,
                "threshold": self.threshold
            }   

    
class NullRateAnomalyDetector(AnomalyDetector):

    def __init__(self, threshold: dict, current_run: dict, previous_run: dict):
        super().__init__(threshold = threshold["null_rate"], current_run = current_run, previous_run = previous_run)
    
    def look_for_anomaly(self):

        current_null_rate = self.current_run["null_rate_amount"]

        result = current_null_rate > self.threshold

        return {
                "anomaly_type": "null_rate",
                "is_anomaly": result,
                "current value": current_null_rate,
                "threshold": self.threshold
            }   
