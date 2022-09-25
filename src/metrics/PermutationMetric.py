#
#   @file : PermutationMetric.py
#   @date : 25 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides

from src.metrics.Metric import Metric


class PermutationMetric(Metric):

    @overrides
    def __init__(self):
        super().__init__()

    @overrides
    def listDistance(self, actual: list, expected: list) -> float:
        if sorted(actual) == sorted(expected):
            return 0.0
        return 1.0
