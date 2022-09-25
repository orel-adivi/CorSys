#
#   @file : HomophoneMetric.py
#   @date : 25 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from src.metrics.Metric import Metric


class HomophoneMetric(Metric):

    HOMOPHONE_PAIRS = {
        'a': ['e', 'i', 'o', 'u'],
        'b': ['p'],
        'c': ['k', 'q'],
        'd': ['t'],
        'e': ['a', 'i', 'o', 'u'],
        'f': ['v'],
        'g': ['j'],
        'i': ['a', 'e', 'o', 'u'],
        'j': ['g'],
        'k': ['c', 'q'],
        'm': ['n'],
        'n': ['m'],
        'o': ['a', 'e', 'i', 'u'],
        'p': ['b'],
        'q': ['c', 'k'],
        's': ['z'],
        't': ['d'],
        'u': ['a', 'e', 'i', 'o'],
        'v': ['f'],
        'y': ['i', 'j'],
        'z': ['s']
    }

    def __init__(self):
        super().__init__()

    def strDistance(self, actual: str, expected: str, penalty: float = 0.25) -> float:
        if len(actual) != len(expected):
            return 1.0
        score = 0.0
        for letter_actual, letter_expected in zip(actual.lower(), expected.lower()):
            if letter_actual == letter_expected:
                continue
            elif letter_actual not in HomophoneMetric.HOMOPHONE_PAIRS or \
                    letter_expected not in HomophoneMetric.HOMOPHONE_PAIRS:
                if letter_actual != letter_expected:
                    return 1.0
            else:
                if letter_actual in HomophoneMetric.HOMOPHONE_PAIRS[letter_expected]:
                    score = min(1.0, score + penalty)
                else:
                    return 1.0
        return score
