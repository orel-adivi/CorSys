#
#   @file : VectorMetric.py
#   @date : 25 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import scipy

from src.metrics.Metric import Metric


class VectorMetric(Metric):

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

    def __init__(self, dist_func: str):
        super().__init__()
        func, normalize = VectorMetric.METRIC_FUNCTIONS[dist_func]
        self.__func = func
        self.__normalize = normalize

    def intDistance(self, actual: int, expected: int) -> float:
        actual_list = list(str(actual))
        expected_list = list(str(expected))
        max_len = max(len(actual_list), len(expected_list))
        actual_list_padded = [0] * (max_len - len(actual_list)) + actual_list
        expected_list_padded = [0] * (max_len - len(expected_list)) + expected_list
        return self.listDistance(actual_list_padded, expected_list_padded)

    def floatDistance(self, actual: float, expected: float, EPS: float = 1e-3) -> float:
        actual_list_whole = list(str(actual).split('.')[0])
        actual_list_fraction = list(str(actual).split('.')[1])
        expected_list_whole = list(str(expected).split('.')[0])
        expected_list_fraction = list(str(expected).split('.')[1])
        max_len_whole = max(len(actual_list_whole), len(expected_list_whole))
        actual_list_whole_padded = [0] * (max_len_whole - len(actual_list_whole)) + actual_list_whole
        expected_list_whole_padded = [0] * (max_len_whole - len(expected_list_whole)) + expected_list_whole
        max_len_fraction = max(len(actual_list_fraction), len(expected_list_fraction))
        actual_list_fraction_padded = actual_list_fraction + [0] * (max_len_fraction - len(actual_list_fraction))
        expected_list_fraction_padded = expected_list_fraction + [0] * (max_len_fraction - len(expected_list_fraction))
        return self.listDistance(actual=actual_list_whole_padded + actual_list_fraction_padded,
                                 expected=expected_list_whole_padded + expected_list_fraction_padded)

    def listDistance(self, actual: list, expected: list) -> float:
        min_length = min(len(actual), len(expected))
        max_length = max(len(actual), len(expected))
        shared_dist = (self.__func(actual[0:min_length], expected[0:min_length]) * min_length)
        if not self.__normalize:
            return shared_dist + (max_length - min_length)
        return (shared_dist + (max_length - min_length)) / max_length
