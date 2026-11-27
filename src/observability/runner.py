class ObservabilityRunner():

    def __init__(self, metrics: list, df):
        self.metrics = metrics
        self.df = df

    def run(self):

        expressions = []

        for metric in self.metrics:

            expressions.append(metric.get_expression())

        return self.df.agg(*expressions)
