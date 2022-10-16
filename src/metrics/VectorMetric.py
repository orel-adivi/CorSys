#
#   @file : VectorMetric.py
#   @date : 16 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides
import numpy as np
import scipy
import warnings

from src.objects.Metric import Metric


class VectorMetric(Metric):
    """
    The VectorMetric class implements the vector metric, which lets the user choose a vector distance function and then
    uses it to measure distance between values.

    Public methods:
        - __init__ - Initialize a vector metric object.
        - intDistance - Compute the distance between two integers using a chosen vector distance function.
        - floatDistance - Compute the distance between two floats using a chosen vector distance function.
        - strDistance - Compute the distance between two strings using a chosen vector distance function.
        - listDistance - Compute the distance between two lists using a chosen vector distance function.
        - distance - Compute the distance between any two values.
    """

    METRIC_FUNCTIONS = {
        "braycurtis": (scipy.spatial.distance.braycurtis, False),
        "canberra": (scipy.spatial.distance.canberra, True),
        "correlation": (scipy.spatial.distance.correlation, False),
        "cosine": (scipy.spatial.distance.cosine, False),
        "jensenshannon": (scipy.spatial.distance.jensenshannon, False),
        "hamming": (scipy.spatial.distance.hamming, True),
        "jaccard": (scipy.spatial.distance.jaccard, False),
        "russellrao": (scipy.spatial.distance.russellrao, False),
        "yule": (scipy.spatial.distance.yule, False)
    }

    @overrides
    def __init__(self, dist_func: str) -> None:
        """
        Initialize a vector metric object.

        :param dist_func: The vector distance function to be used by the object
        """
        super().__init__()
        np.seterr(all='raise')
        func, normalize = VectorMetric.METRIC_FUNCTIONS[dist_func]
        self.__func = func
        self.__normalize = normalize

    @overrides
    def intDistance(self, actual: int, expected: int) -> float:
        """
        Compute the distance between two integers according to the vector metric, by converting the integers into lists
        of characters and then using a vector distance function from METRIC_FUNCTIONS which was chosen at
        initialization.

        :param actual: Integer returned by the synthesized program.
        :param expected: Integer received as the desired output.
        :return: The distance between the integers actual and expected according to the chosen vector metric.
        """
        actual_list = list(str(actual))
        expected_list = list(str(expected))
        max_len = max(len(actual_list), len(expected_list))
        actual_list_padded = ['0'] * (max_len - len(actual_list)) + actual_list
        expected_list_padded = ['0'] * (max_len - len(expected_list)) + expected_list
        return self.listDistance(actual_list_padded, expected_list_padded)

    @overrides
    def floatDistance(self, actual: float, expected: float, EPS: float = 1e-3) -> float:
        """
        Compute the distance between two floats according to the vector metric, by converting the floats into lists of
        characters and then using a vector distance function from METRIC_FUNCTIONS which was chosen at initialization.

        :param actual: Float returned by the synthesized program.
        :param expected: Float received as the desired output.
        :param EPS: This value is ignored.
        :return: The distance between the floats actual and expected according to the chosen vector metric.
        """
        actual_list_whole = list(str(actual).split('.')[0])
        actual_list_fraction = list(str(actual).split('.')[1])
        expected_list_whole = list(str(expected).split('.')[0])
        expected_list_fraction = list(str(expected).split('.')[1])
        max_len_whole = max(len(actual_list_whole), len(expected_list_whole))
        actual_list_whole_padded = ['0'] * (max_len_whole - len(actual_list_whole)) + actual_list_whole
        expected_list_whole_padded = ['0'] * (max_len_whole - len(expected_list_whole)) + expected_list_whole
        max_len_fraction = max(len(actual_list_fraction), len(expected_list_fraction))
        actual_list_fraction_padded = actual_list_fraction + ['0'] * (max_len_fraction - len(actual_list_fraction))
        expected_list_fraction_padded = expected_list_fraction + ['0'] * \
            (max_len_fraction - len(expected_list_fraction))
        return self.listDistance(actual=actual_list_whole_padded + actual_list_fraction_padded,
                                 expected=expected_list_whole_padded + expected_list_fraction_padded)

    @overrides
    def listDistance(self, actual: list, expected: list) -> float:
        """
        Compute the distance between two lists according to the vector metric, using a vector distance function from
        METRIC_FUNCTIONS which was chosen at initialization.

        :param actual: List returned by the synthesized program.
        :param expected: List received as the desired output.
        :return: The distance between the integers actual and expected according to the chosen vector metric.
        """
        min_length = min(len(actual), len(expected))
        max_length = max(len(actual), len(expected))
        if min_length > 0:
            with warnings.catch_warnings():
                warnings.simplefilter(action='ignore', category=FutureWarning)
                shared_dist = min_length * self.__func(actual[0:min_length], expected[0:min_length])
        else:
            shared_dist = 0
        if not self.__normalize:
            return shared_dist + (max_length - min_length)
        return (shared_dist + (max_length - min_length)) / max_length
