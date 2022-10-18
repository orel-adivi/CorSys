#
#   @file : MetricReader.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from src.objects.Metric import Metric
from src.metrics.DefaultMetric import DefaultMetric
from src.metrics.NormalMetric import NormalMetric
from src.metrics.CalculationMetric import CalculationMetric
from src.metrics.VectorMetric import VectorMetric
from src.metrics.HammingMetric import HammingMetric
from src.metrics.LevenshteinMetric import LevenshteinMetric
from src.metrics.PermutationMetric import PermutationMetric
from src.metrics.KeyboardMetric import KeyboardMetric
from src.metrics.HomophoneMetric import HomophoneMetric


class MetricReader(object):
    """
    A class which parse a metric name and metric parameter to a single Metric object.

    Public method:
        - parseMetric - Convert metric name and parameter from string form to a metric object.
    """

    METRIC_DICTIONARY = {
        'DefaultMetric': lambda parameter: DefaultMetric(),
        'NormalMetric': lambda parameter: NormalMetric(STD_DEV=float(eval(parameter))),
        'CalculationMetric': lambda parameter: CalculationMetric(),
        'VectorMetric': lambda parameter: VectorMetric(dist_func=str(parameter)),
        'HammingMetric': lambda parameter: HammingMetric(),
        'LevenshteinMetric': lambda parameter: LevenshteinMetric(solve_recursively=bool(eval(parameter))),
        'PermutationMetric': lambda parameter: PermutationMetric(),
        'KeyboardMetric': lambda parameter: KeyboardMetric(),
        'HomophoneMetric': lambda parameter: HomophoneMetric(),
    }

    @staticmethod
    def parseMetric(metric_name: str, metric_parameter: str) -> Metric:
        """
        Convert metric name and parameter from string form to a metric object.

        :param metric_name: Metric name is string form
        :param metric_parameter: Metric parameter (if there is one) in string form
        :return: A metric object
        """
        return MetricReader.METRIC_DICTIONARY[metric_name](metric_parameter)
