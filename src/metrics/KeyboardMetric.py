#
#   @file : KeyboardMetric.py
#   @date : 25 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides

from src.metrics.Metric import Metric


class KeyboardMetric(Metric):
    # Read https://codegolf.stackexchange.com/a/233633 for implementation details

    INDEX_MAPPING = '.lo,kimjunhybgtvfrcdexswzaq'
    SCALE_PARAMETER = 1 / 36

    @staticmethod
    def __letter_mapper(letter: str):
        index = KeyboardMetric.INDEX_MAPPING.find(letter)
        return (index % 3 * 4j) + index - ((-index) // 3)

    @staticmethod
    def __letter_dist(actual: str, expected: str):
        return abs(KeyboardMetric.__letter_mapper(actual) - KeyboardMetric.__letter_mapper(expected)) * \
               KeyboardMetric.SCALE_PARAMETER

    @overrides
    def __init__(self):
        super().__init__()

    @overrides
    def strDistance(self, actual: str, expected: str, penalty: float = 0.25) -> float:
        if len(actual) != len(expected):
            return 1.0
        score = 0.0
        for letter_actual, letter_expected in zip(actual.lower(), expected.lower()):
            if letter_actual == letter_expected:
                continue
            else:
                score = min(1.0, score + penalty * KeyboardMetric.__letter_dist(letter_actual, letter_expected))
        return score


if __name__ == "__main__":
    metric = KeyboardMetric()
    # print(metric.strDistance("abc", "abc"))
    # for s in ['AB', 'BQ', 'GC', 'HJ', 'LJ', 'PX', 'YY', 'PQ']:
    #     print(metric.strDistance(*s))

    res = []
    for l1 in '.lo,kimjunhybgtvfrcdexswzaqp':
        for l2 in '.lo,kimjunhybgtvfrcdexswzaqp':
            res.append(metric.strDistance(f'{l1}{l1}{l1}{l1}', f'{l2}{l2}{l2}'))
    print(res)
    print('\n\n')
    print(max(res))
    print(min(res))
