#
#   @file : DefaultMetric.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides

from src.objects.Metric import Metric


class DefaultMetric(Metric):
    """
    The DefaultMetric class inherits from Metric, where the default metric functions have already been implemented.

    Public methods:
        - __init__ - Initialize a default metric object.
        - intDistance - Compute the distance between two integers.
        - floatDistance - Compute the distance between two floats.
        - strDistance - Compute the distance between two strings.
        - listDistance - Compute the distance between two lists.
        - distance - Compute the distance between any two values.
    """

    @overrides
    def __init__(self) -> None:
        """
        Initialize a default metric object.
        """
        super().__init__()
