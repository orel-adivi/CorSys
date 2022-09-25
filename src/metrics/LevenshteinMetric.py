#
#   @file : LevenshteinMetric.py
#   @date : 25 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import numpy as np

from src.metrics.Metric import Metric


class LevenshteinMetric(Metric):

    @staticmethod
    def __calcLevenshteinDistRecursive(actual: str, expected: str):
        if len(actual) == 0:
            return len(expected)
        elif len(expected) == 0:
            return len(actual)
        elif actual[0] == expected[0]:
            return LevenshteinMetric.__calcLevenshteinDistRecursive(actual=actual[1:], expected=expected[1:])
        return 1 + min(
            LevenshteinMetric.__calcLevenshteinDistRecursive(actual=actual[1:], expected=expected),
            LevenshteinMetric.__calcLevenshteinDistRecursive(actual=actual, expected=expected[1:]),
            LevenshteinMetric.__calcLevenshteinDistRecursive(actual=actual[1:], expected=expected[1:])
        )

    @staticmethod
    def __calcLevenshteinDistDP(actual: str, expected: str):
        dims = (len(actual) + 1, len(expected) + 1)
        dp_matrix = np.zeros(dims, dtype=np.int64)
        for index_actual in range(1, dims[0]):
            dp_matrix[index_actual][0] = index_actual
        for index_expected in range(1, dims[1]):
            dp_matrix[0][index_expected] = index_expected
        for index_actual in range(1, dims[0]):
            for index_expected in range(1, dims[1]):
                if actual[index_actual - 1] == expected[index_expected - 1]:
                    dp_matrix[index_actual][index_expected] = dp_matrix[index_actual - 1][index_expected - 1]
                else:
                    dp_matrix[index_actual][index_expected] = 1 + min(
                        dp_matrix[index_actual - 1][index_expected],
                        dp_matrix[index_actual][index_expected - 1],
                        dp_matrix[index_actual - 1][index_expected - 1]
                    )
        return dp_matrix[-1][-1]

    def __init__(self, solve_recursively: bool = False):
        super().__init__()
        if solve_recursively:
            self.__solver = LevenshteinMetric.__calcLevenshteinDistRecursive
        else:
            self.__solver = LevenshteinMetric.__calcLevenshteinDistDP

    def intDistance(self, actual: int, expected: int) -> float:
        return self.strDistance(actual=str(actual), expected=str(expected))

    def floatDistance(self, actual: float, expected: float, EPS: float = 1e-3) -> float:
        return self.strDistance(actual=str(actual), expected=str(expected))

    def strDistance(self, actual: str, expected: str) -> float:
        if actual == expected == "":
            return 0.0
        return self.__solver(actual=actual, expected=expected) / max(len(actual), len(expected))


if __name__ == "__main__":
    metric1, metric2 = LevenshteinMetric(), LevenshteinMetric(solve_recursively=True)
    print(metric1.distance("kelm", "hello"), metric2.distance("kelm", "hello"))
    print(metric1.distance("hello", "hello"), metric2.distance("hello", "hello"))
    print(metric1.distance("hello", "hellow"), metric2.distance("hello", "hellow"))
    print(metric1.distance("hello", "helo"), metric2.distance("hello", "helo"))
    print(metric1.distance("hello", "abcde"), metric2.distance("hello", "abcde"))
    print(metric1.distance("", "hello"), metric2.distance("", "hello"))
    print(metric1.distance("hello", ""), metric2.distance("hello", ""))
    print(metric1.distance("", ""), metric2.distance("", ""))
