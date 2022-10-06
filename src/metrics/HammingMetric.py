#
#   @file : HammingMetric.py
#   @date : 25 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides

from src.metrics.VectorMetric import VectorMetric


class HammingMetric(VectorMetric):

    @overrides
    def __init__(self):
        super().__init__(dist_func="hamming")

    @overrides
    def strDistance(self, actual: str, expected: str) -> float:
        return self.listDistance(actual=list(actual), expected=list(expected))


if __name__ == '__main__':
    metric = HammingMetric()
    print(metric.strDistance('abc', 'abd'))
    print(metric.listDistance(['a', 'b', 'c'], ['a', 'bb', 'c']))
