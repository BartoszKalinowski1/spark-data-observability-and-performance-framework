class ObservabilityRunner():

    def __init__(self, metrics: list, df):
        self.metrics = metrics
        self.df = df

    def run(self):

        results = []

        for metric in self.metrics:
            result = metric.calculate(self.df)

            results.append({
                "metric_name": metric.metric_name,
                "value": result
            })

        return results
