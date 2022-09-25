#
#   @file : Metric.py
#   @date : 25 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from abc import ABC, abstractmethod
from typing import final


class Metric(ABC):

    @abstractmethod
    def __init__(self):
        pass

    def intDistance(self, actual: int, expected: int) -> float:
        if actual == expected:
            return 0.0
        return 1.0

    def floatDistance(self, actual: float, expected: float, EPS: float = 1e-3) -> float:
        if abs(actual - expected) <= EPS:
            return 0.0
        return 1.0

    def strDistance(self, actual: str, expected: str) -> float:
        if actual == expected:
            return 0.0
        return 1.0

    def listDistance(self, actual: list, expected: list) -> float:
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
        if type(actual) == type(expected) == int:
            return self.intDistance(actual=actual, expected=expected)
        elif type(actual) == type(expected) == float:
            return self.floatDistance(actual=actual, expected=expected)
        elif type(actual) == type(expected) == str:
            return self.strDistance(actual=actual, expected=expected)
        elif type(actual) == type(expected) == list:
            return self.listDistance(actual=actual, expected=expected)
        return 1.0
