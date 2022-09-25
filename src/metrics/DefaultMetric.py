#
#   @file : DefaultMetric.py
#   @date : 25 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides

from src.metrics.Metric import Metric


class DefaultMetric(Metric):

    @overrides
    def __init__(self):
        super().__init__()
