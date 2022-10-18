#
#   @file : CombinedMetric.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides

from src.objects.Metric import Metric
from src.io.MetricReader import MetricReader


class CombinedMetric(Metric):
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

    @overrides
    def __init__(self, int_metric: str, int_metric_parameter: str,
                 float_metric: str, float_metric_parameter: str,
                 str_metric: str, str_metric_parameter: str,
                 list_metric: str, list_metric_parameter: str):
        """
        Initialize a combined metric object, assigning each supported type of variable its own metric.

        :param int_metric: The metric to be used for integers.
        :param int_metric_parameter:
        :param float_metric: The metric to be used for floats.
        :param float_metric_parameter:
        :param str_metric: The metric to be used for strings.
        :param str_metric_parameter:
        :param list_metric: The metric to be used for lists.
        :param list_metric_parameter:
        """
        Metric.__init__(self)
        self.__int_metric_class = MetricReader.METRIC_DICTIONARY[int_metric](int_metric_parameter)
        self.__float_metric_class = MetricReader.METRIC_DICTIONARY[float_metric](float_metric_parameter)
        self.__str_metric_class = MetricReader.METRIC_DICTIONARY[str_metric](str_metric_parameter)
        self.__list_metric_class = MetricReader.METRIC_DICTIONARY[list_metric](list_metric_parameter)

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
