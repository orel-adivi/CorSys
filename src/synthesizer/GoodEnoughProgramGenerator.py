#
#   @file : ProgramGenerator.py
#   @date : 23 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from src.synthesizer.ProgramGenerator import ProgramGenerator
from src.synthesizer.SearchSpace import SearchSpace
import ast


class GoodEnoughProgramGenerator(ProgramGenerator):

    def __init__(self, search_space: list[list], max_height: int):
        super().__init__(search_space=search_space, max_height=max_height)

    @staticmethod
    def default_metric(actual: list, expected: list):
        return len([res for res in zip(actual, expected) if res[0] == res[1]])

    def findGoodEnoughNumberProgram(self, assignments: list[dict], evaluations: list, success_number: int):
        for program in self.enumerate(assignments=assignments):
            if GoodEnoughProgramGenerator.default_metric(program.results, evaluations) >= success_number:
                return program

    def findGoodEnoughRateProgram(self, assignments: list[dict], evaluations: list, success_rate: float):
        for program in self.enumerate(assignments=assignments):
            if GoodEnoughProgramGenerator.default_metric(program.results, evaluations) >=\
                    success_rate * len(evaluations):
                return program


if __name__ == '__main__':
    inputs = [{'x': 1, 'y': 2, 'z': 3}, {'x': 2, 'y': 4, 'z': 5}, {'x': 11, 'y': 22, 'z': 3},
              {'x': 0, 'y': -1, 'z': 0}, {'x': 11, 'y': 22, 'z': 4}]
    outputs = list(map(lambda env: env['x'] + env['y'] + env['z'], inputs))
    outputs[-1] -= 1
    search_space1 = SearchSpace.readGrammarFromFile('../../utils/grammars/IntegerGrammar.txt')
    generator = GoodEnoughProgramGenerator(search_space1, 10)
    result = generator.findGoodEnoughRateProgram(inputs, outputs, 0.7)
    print(ast.unparse(result))
