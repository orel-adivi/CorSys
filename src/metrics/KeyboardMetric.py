#
#   @file : KeyboardMetric.py
#   @date : 16 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
import functools

from overrides import overrides

from src.objects.Metric import Metric


class KeyboardMetric(Metric):
    """
    The KeyboardMetric class implements the keyboard metric, which computes the distance between two characters based on
    the physical distance between their keys on a QWERTY keyboard. This metric only implements the distance method for
    strings, since its main purpose is to account for typing mistakes. For other data types it uses the default metric.

    Please read https://codegolf.stackexchange.com/a/233633 for implementation details

    Public methods:
        - __init__ - Initialize a keyboard metric object.
        - intDistance - Compute the distance between two integers.
        - floatDistance - Compute the distance between two floats.
        - strDistance - Compute the distance between two strings while considering the location of characters on the
          keyboard.
        - listDistance - Compute the distance between two lists.
        - distance - Compute the distance between any two values.
    """

    LETTER_MAPPING = {character: (index % 3 * 4j) + index - ((-index) // 3)
                      for character, index
                      in [(character, '.lo,kimjunhybgtvfrcdexswzaq'.find(character))
                          for character
                          in '1234567890-=qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./']}
    SCALE_PARAMETER = 1 / 36

    @staticmethod
    @functools.cache
    def __letter_dist(actual: str, expected: str):
        """
        Computes the relative distance between two characters on a QWERTY keyboard (such that the maximal distance
        is 1)

        :param actual: First letter.
        :param expected: Second letter.
        :return: The relative keyboard distance between actual and expected.
        """
        return abs(KeyboardMetric.LETTER_MAPPING[actual] - KeyboardMetric.LETTER_MAPPING[expected]) * \
               KeyboardMetric.SCALE_PARAMETER

    @overrides
    def __init__(self) -> None:
        """
        Initialize a keyboard metric object.
        """
        super().__init__()

    @overrides
    def strDistance(self, actual: str, expected: str, penalty: float = 0.25) -> float:
        """
        Compute the distance between two string values according to the keyboard metric, which takes into account
        typing errors stemming from two characters being close on a keyboard.
        If string lengths are different the distance is 1. If the lengths are equal, a "penalty" is given for each
        substitution of a character. Each penalty is proportional to the distance between the actual and expected
        characters on a keyboard. The total distance is the maximum between the sum of all penalties and 1.

        :param actual: String returned by the synthesized program.
        :param expected: String received as the desired output.
        :param penalty: The maximal penalty given for substituting a character (actual penalty depends on keyboard
                        distance).
        :return: The distance between the strings actual and expected according to the homophone metric.
        """
        if len(actual) != len(expected):
            return 1.0
        score = 0.0
        for letter_actual, letter_expected in zip(actual.lower(), expected.lower()):
            if letter_actual == letter_expected:
                continue
            else:
                score += penalty * KeyboardMetric.__letter_dist(letter_actual, letter_expected)
                if score >= 1.0:
                    return 1.0
        return score
