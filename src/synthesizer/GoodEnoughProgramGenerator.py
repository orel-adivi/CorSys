#
#   @file : ProgramGenerator.py
#   @date : 23 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from src.synthesizer.ProgramGenerator import ProgramGenerator
from src.synthesizer.SearchSpace import SearchSpace
from src.metrics.Metric import Metric
from src.metrics.DefaultMetric import DefaultMetric


class GoodEnoughProgramGenerator(ProgramGenerator):

    def __init__(self, search_space: list[list], max_height: int):
        super().__init__(search_space=search_space, max_height=max_height)

    @staticmethod
    def get_distance(actual: list, expected: list, metric: Metric):
        res = [metric.distance(actual=actual_example, expected=expected_example)
               for actual_example, expected_example in zip(actual, expected)]
        return sum(res)

    def findGoodEnoughNumberProgram(self, assignments: list[dict], evaluations: list, error_sum: int,
                                    metric: Metric = DefaultMetric()):
        for program in self.enumerate(assignments=assignments):
            if GoodEnoughProgramGenerator.get_distance(actual=program.results,
                                                       expected=evaluations,
                                                       metric=metric) <= error_sum:
                return program

    def findGoodEnoughRateProgram(self, assignments: list[dict], evaluations: list, error_rate: float,
                                  metric: Metric = DefaultMetric()):
        for program in self.enumerate(assignments=assignments):
            if GoodEnoughProgramGenerator.get_distance(actual=program.results,
                                                       expected=evaluations,
                                                       metric=metric) <= error_rate * len(evaluations):
                return program


if __name__ == '__main__':
    import ast
    inputs = [{'x': 1, 'y': 2, 'z': 3}, {'x': 2, 'y': 4, 'z': 5}, {'x': 11, 'y': 22, 'z': 3},
              {'x': 0, 'y': -1, 'z': 0}, {'x': 11, 'y': 22, 'z': 4}]
    outputs = list(map(lambda env: env['x'] + env['y'] + env['z'], inputs))
    outputs[-1] -= 1
    search_space1 = SearchSpace.readGrammarFromFile('../../utils/grammars/IntegerGrammar.txt')
    generator = GoodEnoughProgramGenerator(search_space1, 10)
    result = generator.findGoodEnoughRateProgram(inputs, outputs, 0.2)
    print(ast.unparse(result))
