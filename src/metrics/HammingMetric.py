#
#   @file : HammingMetric.py
#   @date : 25 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from src.metrics.VectorMetric import VectorMetric


class HammingMetric(VectorMetric):

    def __init__(self):
        super().__init__(dist_func="hamming")

    def strDistance(self, actual: str, expected: str) -> float:
        return self.listDistance(actual=list(actual), expected=list(expected))
