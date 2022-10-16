#
#   @file : LevenshteinMetric.py
#   @date : 16 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides
import numpy as np

from src.objects.Metric import Metric


class LevenshteinMetric(Metric):
    """
    The LevenshteinMetric class implements the Levenshtein metric, which computes the Levensthein distance between
    strings and normalizes it according to the strings' length. For other data types it uses the default metric.

    Public methods:
        - __init__ - Initialize a Levenshtein metric object.
        - intDistance - Compute the distance between two integers.
        - floatDistance - Compute the distance between two floats.
        - strDistance - Compute the normalized Levenshtein distance between two strings.
        - listDistance - Compute the distance between two lists.
        - distance - Compute the distance between any two values.
    """

    @staticmethod
    def __calcLevenshteinDistRecursive(actual: str, expected: str):
        """
        Compute the Levenshtein distance between two strings recursively.

        :param actual: String returned by the synthesized program.
        :param expected: String received as the desired output.
        :return: The Levenshtein distance between actual and expected.
        """
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
        """
        Compute the Levenshtein distance between two strings using dynamic programming.

        :param actual: String returned by the synthesized program.
        :param expected: String received as the desired output.
        :return: The Levenshtein distance between actual and expected.
        """
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

    @overrides
    def __init__(self, solve_recursively: bool = False):
        """
        Initialize a Levenshtein metric object.

        :param solve_recursively: determines whether the object will compute Levenshtein distance using a recursive or
                                  a dynamic-programming based implementation.
        """
        super().__init__()
        if solve_recursively:
            self.__solver = LevenshteinMetric.__calcLevenshteinDistRecursive
        else:
            self.__solver = LevenshteinMetric.__calcLevenshteinDistDP

    @overrides
    def intDistance(self, actual: int, expected: int) -> float:
        """
        Compute the distance between two integer values according to the Levenshtein metric, by converting the integers
        into strings and then using the string-specific Levenshtein distance function.

        :param actual: Integer value returned by the synthesized program.
        :param expected: Integer value received as the desired output.
        :return: The distance between the integers actual and expected according to the Levenshtein metric.
        """
        return self.strDistance(actual=str(actual), expected=str(expected))

    @overrides
    def floatDistance(self, actual: float, expected: float, EPS: float = 1e-3) -> float:
        """
        Compute the distance between two float values according to the Levenshtein metric, by converting the floats
        into strings and then using the string-specific Levenshtein distance function.

        :param actual: Float value returned by the synthesized program.
        :param expected: Float value received as the desired output.
        :return: The distance between the floats actual and expected according to the Levenshtein metric.
        """
        return self.strDistance(actual=str(actual), expected=str(expected))

    @overrides
    def strDistance(self, actual: str, expected: str) -> float:
        """
        Compute the distance between two string values according to the Levenshtein metric, which is the Levenshtein
        distance between the strings divided by the length of the longer string.

        :param actual: String returned by the synthesized program.
        :param expected: String received as the desired output.
        :return: The distance between the strings actual and expected according to the Levenshtein metric.
        """
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
