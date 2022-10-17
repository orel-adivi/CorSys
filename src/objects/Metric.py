#
#   @file : Metric.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from abc import ABC, abstractmethod
from overrides import final


class Metric(ABC):
    """
    The base class of all metrics, implementing the default metric for computing distance between two values.

    Public methods:
        - intDistance - Compute the distance between two integers.
        - floatDistance - Compute the distance between two floats.
        - strDistance - Compute the distance between two strings.
        - listDistance - Compute the distance between two lists.
        - distance - Compute the distance between any two values.
    """

    @abstractmethod
    def __init__(self):
        """
        Initialize a metric object (abstract).
        """
        pass

    def intDistance(self, actual: int, expected: int) -> float:
        """
        Computes the distance between two integer values according to the default metric (0 for equal
        values and 1 for different values).

        :param actual: Integer value returned by the synthesized program.
        :param expected: Integer value received as the desired output.
        :return: 0.0 if values are equal, otherwise 1.0.
        """
        if actual == expected:
            return 0.0
        return 1.0

    def floatDistance(self, actual: float, expected: float, EPS: float = 1e-3) -> float:
        """
        Compute the distance between two float values according to the default metric (0 for equal
        values and 1 for different values), while taking into account numerical errors.

        :param actual: Float value returned by the synthesized program.
        :param expected: Float value received as the desired output.
        :param EPS: The maximal numerical error allowed.
        :return: 0.0 if the difference between values is at most EPS, otherwise 1.0.
        """
        if abs(actual - expected) <= EPS:
            return 0.0
        return 1.0

    def strDistance(self, actual: str, expected: str) -> float:
        """
        Compute the distance between two string values according to the default metric (0 for equal
        values and 1 for different values).

        :param actual: String returned by the synthesized program.
        :param expected: String received as the desired output.
        :return: 0.0 if the strings are identical, otherwise 1.0.
        """
        if actual == expected:
            return 0.0
        return 1.0

    def listDistance(self, actual: list, expected: list) -> float:
        """
        Compute the distance between two lists according to the default metric (0 for identical
        lists and 1 for different lists).

        :param actual: List returned by the synthesized program.
        :param expected: List received as the desired output.
        :return: 0.0 if the lists have equal lengths and the elements at every index are equal, otherwise 1.0.
        """
        if len(actual) != len(expected):
            return 1.0
        dist = [self.distance(actual_element, expected_element)
                for actual_element, expected_element in zip(actual, expected)]
        sum_dist = sum(dist)
        if sum_dist > 1.0:
            return 1.0
        return sum_dist

    @final
    def distance(self, actual: object, expected: object) -> float:
        """
        Compute the distance between two values according to the default metric. For values of the same type computes
        the distance using type-specific functions, for values of different types returns a distance of 1.

        :param actual: Value returned by the synthesized program.
        :param expected: Value received as the desired output.
        :return: 0.0 if the values are equal according to the metric, otherwise 1.0.
        """
        if type(actual) == type(expected) == int:
            return self.intDistance(actual=actual, expected=expected)
        elif type(actual) == type(expected) == float:
            return self.floatDistance(actual=actual, expected=expected)
        elif type(actual) == type(expected) == str:
            return self.strDistance(actual=actual, expected=expected)
        elif type(actual) == type(expected) == list:
            return self.listDistance(actual=actual, expected=expected)
        return 1.0
