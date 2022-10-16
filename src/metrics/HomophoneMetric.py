#
#   @file : HomophoneMetric.py
#   @date : 16 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides

from src.objects.Metric import Metric


class HomophoneMetric(Metric):
    """
    The HomophoneMetric class implements the homophone metric, which considers two strings closer if they are
    pronounced similarly. For other data types it uses the default metric.

    Public methods:
        - __init__ -Initialize a homophone metric object.
        - intDistance - Computes the distance between two integers.
        - floatDistance - Computes the distance between two floats.
        - strDistance - Computes the distance between two strings while considering similarly pronounced letters.
        - listDistance - Computes the distance between two lists.
        - distance - Computes the distance between any two values.
    """

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

    @overrides
    def __init__(self) -> None:
        """
        Initialize a homophone metric object.
        """
        super().__init__()

    @overrides
    def strDistance(self, actual: str, expected: str, penalty: float = 0.25) -> float:
        """
        Compute the distance between two string values according to the homophone metric, which considers
        similar-sounding strings to be closer than different-sounding ones.
        If string lengths are different the distance is 1. If the lengths are equal, a "penalty" is given for each
        substitution of a character with a similar-sounding one (similar characters are defined in HOMOPHONE_PAIRS).
        In that case, the distance is the minimum between the sum of all penalties given and 1. If a character is
        substituted with a non-similar character, the distance is also 1.

        :param actual: String returned by the synthesized program.
        :param expected: String received as the desired output.
        :param penalty: Penalty given for substituting a character with a similar-sounding character.
        :return: The distance between the strings actual and expected according to the homophone metric.
        """
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
