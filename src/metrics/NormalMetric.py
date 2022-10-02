#
#   @file : NormalMetric.py
#   @date : 25 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides
import scipy.stats
import numpy

from src.metrics.Metric import Metric


class NormalMetric(Metric):

    @overrides
    def __init__(self):
        super().__init__()
        numpy.seterr(all='raise')

    @overrides
    def intDistance(self, actual: int, expected: int) -> float:
        return self.floatDistance(actual=float(actual), expected=float(expected))

    @overrides
    def floatDistance(self, actual: float, expected: float, EPS: float = 1e-3, STD_DEV: float = 1.0) -> float:
        try:
            res = scipy.stats.norm.pdf(x=actual, loc=expected, scale=STD_DEV)
            max_val = scipy.stats.norm.pdf(x=expected, loc=expected, scale=STD_DEV)
        except FloatingPointError:
            return 1.0
        return (max_val - res) / max_val


if __name__ == "__main__":
    metric = NormalMetric()
    print(metric.intDistance(0, 5))
