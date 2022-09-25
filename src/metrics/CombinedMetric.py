#
#   @file : CombinedMetric.py
#   @date : 25 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from src.metrics.Metric import Metric
from src.metrics.DefaultMetric import DefaultMetric
from src.metrics.NormalMetric import NormalMetric
from src.metrics.CalculationMetric import CalculationMetric
from src.metrics.HammingMetric import HammingMetric
from src.metrics.LevenshteinMetric import LevenshteinMetric
from src.metrics.PermutationMetric import PermutationMetric
from src.metrics.KeyboardMetric import KeyboardMetric
from src.metrics.HomophoneMetric import HomophoneMetric


class CombinedMetric(DefaultMetric, NormalMetric, CalculationMetric, HammingMetric,
                     LevenshteinMetric, PermutationMetric, KeyboardMetric, HomophoneMetric):

    REGULAR_METRICS = {
        'DefaultMetric': DefaultMetric,
        'NormalMetric': NormalMetric,
        'CalculationMetric': CalculationMetric,
        'HammingMetric': HammingMetric,
        'LevenshteinMetric': LevenshteinMetric,
        'PermutationMetric': PermutationMetric,
        'KeyboardMetric': KeyboardMetric,
        'HomophoneMetric': HomophoneMetric
    }

    def __init__(self, int_metric: str = 'DefaultMetric', float_metric: str = 'DefaultMetric',
                 str_metric: str = 'DefaultMetric', list_metric: str = 'DefaultMetric'):
        Metric.__init__(self)
        for class_name, class_object in CombinedMetric.REGULAR_METRICS.items():
            class_object.__init__(self)
        self.__int_metric_class = CombinedMetric.REGULAR_METRICS[int_metric]
        self.__float_metric_class = CombinedMetric.REGULAR_METRICS[float_metric]
        self.__str_metric_class = CombinedMetric.REGULAR_METRICS[str_metric]
        self.__list_metric_class = CombinedMetric.REGULAR_METRICS[list_metric]

    def intDistance(self, actual: int, expected: int, *args, **kwargs) -> float:
        return self.__int_metric_class.intDistance(self, actual=actual, expected=expected, *args, *kwargs)

    def floatDistance(self, actual: float, expected: float, EPS: float = 1e-3, *args, **kwargs) -> float:
        return self.__float_metric_class.floatDistance(self, actual=actual, expected=expected, EPS=EPS, *args, *kwargs)

    def strDistance(self, actual: str, expected: str, *args, **kwargs) -> float:
        return self.__str_metric_class.strDistance(self, actual=actual, expected=expected, *args, *kwargs)

    def listDistance(self, actual: list, expected: list, *args, **kwargs) -> float:
        return self.__list_metric_class.listDistance(self, actual=actual, expected=expected, *args, *kwargs)


if __name__ == "__main__":
    metric = CombinedMetric(int_metric='CalculationMetric', float_metric='NormalMetric', str_metric='LevenshteinMetric',
                            list_metric='PermutationMetric')
    print(metric.intDistance(0, 1))
    print(metric.floatDistance(0.0, 1.0))
    print(metric.strDistance('hello', 'hi'))
    print(metric.listDistance(['a', 'b'], ['b', 'a']))
