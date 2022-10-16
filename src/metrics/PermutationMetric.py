#
#   @file : PermutationMetric.py
#   @date : 16 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides

from src.objects.Metric import Metric


class PermutationMetric(Metric):
    """
    The PermutationMetric class implements the permutation metric, which considered lists equal if they contain the same
    elements, regardless of order.

    Public methods:
        - __init__ - Initialize a permutation metric object.
        - intDistance - Computes the distance between two integers.
        - floatDistance - Computes the distance between two floats.
        - strDistance - Computes the distance between two strings.
        - listDistance - Computes the distance between two lists, while disregarding order.
        - distance - Computes the distance between any two values.
    """

    @overrides
    def __init__(self):
        """
        Initialize a permutation metric object.
        """
        super().__init__()

    @overrides
    def listDistance(self, actual: list, expected: list) -> float:
        """
        Compute the distance between two lists according to the permutation metric, which disregards order between list
        elements.

        :param actual: List returned by the synthesized program.
        :param expected: List received as the desired output.
        :return: 0.0 if the lists contain the same elements at any order, otherwise 1.0.
        """
        if sorted(actual) == sorted(expected):
            return 0.0
        return 1.0
