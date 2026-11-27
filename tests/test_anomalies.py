import sys
sys.path.append("../src")
from observability.anomalies import (
    RowCountAnomalyDetector,
    NullRateAnomalyDetector,
    PerformanceRunTimeAnomalyDetector
)

def test_row_count_anomaly_detector():

    threshold = {
        "row_count": 30
    }

    current_run = {
        "row_count": 1_100_000
    }

    previous_run = {
        "row_count": 1_000_000
    }

    detector = RowCountAnomalyDetector(
        threshold = threshold,
        current_run = current_run,
        previous_run = previous_run
    )

    result = detector.look_for_anomaly()

    assert result["is_anomaly"] is False
    assert result["percentage_change"] == 10.0

def test_null_rate_anomaly_detector():

    threshold = {
        "null_rate": 10
    }

    current_run = {
        "null_rate_amount": 15
    }

    previous_run = {
        "null_rate_amount": 5
    }

    detector = NullRateAnomalyDetector(
        threshold = threshold,
        current_run = current_run,
        previous_run = previous_run
    )

    result = detector.look_for_anomaly()

    assert result["is_anomaly"] is True
    assert result["percentage_change"] is None

def test_performance_runtime_anomaly_detector():

    threshold = {
        "runtime_performance": 10
    }

    ten_last_runtime_median = 2.0
    last_runtime = 4.0

    detector = PerformanceRunTimeAnomalyDetector(
        threshold = threshold,
        ten_last_runtime_median = ten_last_runtime_median,
        last_runtime = last_runtime
    )

    result = detector.look_for_anomaly()

    assert result["is_anomaly"] is True
    assert result["percentage_change"] == 100.0