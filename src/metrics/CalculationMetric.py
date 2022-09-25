#
#   @file : CalculationMetric.py
#   @date : 25 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from overrides import overrides

from src.metrics.Metric import Metric


class CalculationMetric(Metric):

    @overrides
    def __init__(self):
        super().__init__()

    @overrides
    def intDistance(self, actual: int, expected: int, penalty_off_by_one: float = 0.25,
                    penalty_units: float = 0.5) -> float:
        actual_list = list(str(actual))
        expected_list = list(str(expected))
        max_len = max(len(actual_list), len(expected_list))
        actual_list_padded = [0] * (max_len - len(actual_list)) + actual_list
        expected_list_padded = [0] * (max_len - len(expected_list)) + expected_list
        score = 0.0
        if actual_list_padded[-1] != expected_list_padded[-1]:
            if abs(int(actual_list_padded[-1]) - int(expected_list_padded[-1])) == 1:
                score += penalty_units
            else:
                return 1.0
        for actual_digit, expected_digit in zip(actual_list_padded[0:-1], expected_list_padded[0:-1]):
            if actual_digit != expected_digit:
                if abs(int(actual_digit) - int(expected_digit)) == 1:
                    score = min(1.0, score + penalty_off_by_one)
                else:
                    return 1.0
        return score

    @overrides
    def floatDistance(self, actual: float, expected: float, EPS: float = 1e-3, STD_DEV: float = 1.0,
                      penalty_off_by_one: float = 0.25, penalty_right_digit: float = 0.5) -> float:
        actual_list_whole, actual_list_fraction = list(str(actual).split('.')[0]), list(str(actual).split('.')[1])
        expected_list_whole = list(str(expected).split('.')[0])
        expected_list_fraction = list(str(expected).split('.')[1])
        max_len_whole = max(len(actual_list_whole), len(expected_list_whole))
        max_len_fraction = max(len(actual_list_fraction), len(expected_list_fraction))
        actual_list_whole_padded = ['0'] * (max_len_whole - len(actual_list_whole)) + actual_list_whole
        expected_list_whole_padded = ['0'] * (max_len_whole - len(expected_list_whole)) + expected_list_whole
        actual_list_fraction_padded = actual_list_fraction + ['0'] * (max_len_fraction - len(actual_list_fraction))
        expected_list_fraction_padded = expected_list_fraction + ['0'] * (max_len_fraction - len(expected_list_fraction))
        actual_equivalent_int = int(''.join(actual_list_whole_padded) + ''.join(actual_list_fraction_padded))
        expected_equivalent_int = int(''.join(expected_list_whole_padded) + ''.join(expected_list_fraction_padded))
        return self.intDistance(actual=actual_equivalent_int, expected=expected_equivalent_int,
                                penalty_off_by_one=penalty_off_by_one, penalty_units=penalty_right_digit)


if __name__ == "__main__":
    metric = CalculationMetric()
    print(metric.intDistance(0, 5))
    print(metric.intDistance(0, 1))
    print(metric.intDistance(0, 0))
    print(metric.intDistance(10, 11))
    print(metric.intDistance(21, 11))
    print(metric.intDistance(1121, 11))
    print()
    print(metric.floatDistance(0.0, 0.5))
    print(metric.floatDistance(0.0, 0.1))
    print(metric.floatDistance(1.0, 0.0))
    print(metric.floatDistance(0.0, 0.0))
    print(metric.floatDistance(1.0, 1.1))
    print(metric.floatDistance(0.1, 0.11))
    print(metric.floatDistance(0.21, 0.11))
    print(metric.floatDistance(0.21, 11.11))
