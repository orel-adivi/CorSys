#
#   @file : HammingMetric.py
#   @date : 23 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from scipy.spatial.distance import hamming

from src.metrics.VectorMetric import VectorMetric


class HammingMetric(VectorMetric):

    def __init__(self):
        super().__init__(func=hamming, normalize=True)

    def strDistance(self, actual: str, expected: str) -> float:
        return self.listDistance(actual=list(actual), expected=list(expected))
