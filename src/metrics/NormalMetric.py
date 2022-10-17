#
#   @file : NormalMetric.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides
import numpy as np
import scipy.stats

from src.objects.Metric import Metric


class NormalMetric(Metric):
    """
    The NormalMetric class implements the normal metric, which uses a normal
    distribution function to determine the relative distance between two numbers.

    Public methods:
        - __init__ - Initialize a normal metric object.
        - intDistance - Compute the distance between two integers using a normal distribution function.
        - floatDistance - Compute the distance between two floats using a normal distribution function.
        - strDistance - Compute the distance between two strings.
        - listDistance - Compute the distance between two lists.
        - distance - Compute the distance between any two values.
    """

    @overrides
    def __init__(self) -> None:
        """
        Initialize a normal metric object.
        """
        super().__init__()
        np.seterr(all='raise')

    @overrides
    def intDistance(self, actual: int, expected: int) -> float:
        """
        Compute the distance between two integer values according to the normal metric, which uses a normal
        distribution function. Firstly, the function computes the probability of receiving the first value in a normal
        distribution where the mean is the second value.
        Then the distance is normalized, so it lies between 0 and 1.

        :param actual: Integer value returned by the synthesized program.
        :param expected: Integer value received as the desired output.
        :return: The distance between the integers actual and expected according to the normal metric.
        """
        return self.floatDistance(actual=float(actual), expected=float(expected))

    @overrides
    def floatDistance(self, actual: float, expected: float, EPS: float = 1e-3, STD_DEV: float = 1.0) -> float:
        """
        Compute the distance between two float values according to the normal metric, which uses a normal distribution
        function. Firstly, the function computes the probability of receiving the first value in a normal distribution
        where the mean is the second value.
        Then the distance is normalized, so it lies between 0 and 1.

        :param actual: Float value returned by the synthesized program.
        :param expected: Float value received as the desired output.
        :param EPS: Unused in this metric.
        :param STD_DEV: The desired standard deviation of the normal distribution the function uses.
        :return: The distance between the floats actual and expected according to the normal metric.
        """
        try:
            res = scipy.stats.norm.pdf(x=actual, loc=expected, scale=STD_DEV)
            max_val = scipy.stats.norm.pdf(x=expected, loc=expected, scale=STD_DEV)
        except FloatingPointError:
            return 1.0
        return (max_val - res) / max_val
