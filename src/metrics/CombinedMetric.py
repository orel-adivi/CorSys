#
#   @file : CombinedMetric.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides

from src.objects.Metric import Metric
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
    """
    The CombinedMetric class allows users to use different metrics for each type.

    Public methods:
        - __init__ - Initialize a combined metric object, assigning each supported type of variable its own metric.
        - intDistance - Computes the distance between two integers according to the user's chosen integer metric.
        - floatDistance - Computes the distance between two integers according to the user's chosen float metric.
        - strDistance - Computes the distance between two strings according to the user's chosen string metric.
        - listDistance - Computes the distance between two lists according to the user's chosen list metric.
        - distance - Computes the distance between any two values.
    """

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

    @overrides
    def __init__(self, int_metric: str = 'DefaultMetric', float_metric: str = 'DefaultMetric',
                 str_metric: str = 'DefaultMetric', list_metric: str = 'DefaultMetric'):
        """
        Initialize a combined metric object, assigning each supported type of variable its own metric.

        :param int_metric: The metric to be used for integers.
        :param float_metric: The metric to be used for floats.
        :param str_metric: The metric to be used for strings.
        :param list_metric: The metric to be used for lists.
        """
        Metric.__init__(self)
        for class_name, class_object in CombinedMetric.REGULAR_METRICS.items():
            class_object.__init__(self)
        self.__int_metric_class = CombinedMetric.REGULAR_METRICS[int_metric]
        self.__float_metric_class = CombinedMetric.REGULAR_METRICS[float_metric]
        self.__str_metric_class = CombinedMetric.REGULAR_METRICS[str_metric]
        self.__list_metric_class = CombinedMetric.REGULAR_METRICS[list_metric]

    @overrides
    def intDistance(self, actual: int, expected: int, *args, **kwargs) -> float:
        """
        Compute the distance between two integer values according to the integer metric received at initialization.

        :param actual: Integer value returned by the synthesized program.
        :param expected: Integer value received as the desired output.
        :param args: Additional arguments needed for the integer metric.
        :param kwargs: Additional keyword arguments needed for the integer metric.
        :return: The distance between the integers actual and expected.
        """
        return self.__int_metric_class.intDistance(self, actual=actual, expected=expected, *args, *kwargs)

    @overrides
    def floatDistance(self, actual: float, expected: float, EPS: float = 1e-3, *args, **kwargs) -> float:
        """
        Compute the distance between two integer values according to the float metric received at initialization.

        :param actual: Float value returned by the synthesized program.
        :param expected: Float value received as the desired output.
        :param EPS: The maximal numerical error allowed.
        :param args: Additional arguments needed for the float metric.
        :param kwargs: Additional keyword arguments needed for the float metric.
        :return: The distance between the floats actual and expected.
        """
        return self.__float_metric_class.floatDistance(self, actual=actual, expected=expected, EPS=EPS, *args, *kwargs)

    @overrides
    def strDistance(self, actual: str, expected: str, *args, **kwargs) -> float:
        """
        Compute the distance between two strings according to the string metric received at initialization.

        :param actual: String returned by the synthesized program.
        :param expected: String received as the desired output.
        :param args: Additional arguments needed for the string metric.
        :param kwargs: Additional keyword arguments needed for the string metric.
        :return: The distance between the strings actual and expected.
        """
        return self.__str_metric_class.strDistance(self, actual=actual, expected=expected, *args, *kwargs)

    @overrides
    def listDistance(self, actual: list, expected: list, *args, **kwargs) -> float:
        """
        Compute the distance between two lists according to the list metric received at initialization.

        :param actual: List returned by the synthesized program.
        :param expected: List received as the desired output.
        :param args: Additional arguments needed for the list metric.
        :param kwargs: Additional keyword arguments needed for the list metric.
        :return: The distance between the lists actual and expected.
        """
        return self.__list_metric_class.listDistance(self, actual=actual, expected=expected, *args, *kwargs)
