#
#   @file : HammingMetric.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides

from src.metrics.VectorMetric import VectorMetric


class HammingMetric(VectorMetric):
    """
    The HammingMetric class implements the Hamming metric, which computes the Hamming distance between strings and
    normalizes it according to the strings' length. For other data types it uses the default metric.

    Public methods:
        - __init__ - Initialize a Hamming metric object.
        - intDistance - Computes the distance between two integers.
        - floatDistance - Computes the distance between two floats.
        - strDistance - Computes the normalized Hamming distance between two strings.
        - listDistance - Computes the distance between two lists.
        - distance - Computes the distance between any two values.
    """

    @overrides
    def __init__(self) -> None:
        """
        Initialize a Hamming metric object.
        """
        super().__init__(dist_func="hamming")

    @overrides
    def strDistance(self, actual: str, expected: str) -> float:
        """
        Compute the distance between two string values according to the Hamming metric. If string lengths are
        different the distance is 1, otherwise it is the Hamming distance between the strings divided by their length.

        :param actual: String returned by the synthesized program.
        :param expected: String received as the desired output.
        :return: The distance between the strings actual and expected according to the Hamming metric.
        """
        return self.listDistance(actual=list(actual), expected=list(expected))
