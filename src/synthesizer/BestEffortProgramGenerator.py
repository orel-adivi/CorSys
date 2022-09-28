#
#   @file : BestEffortProgramGenerator.py
#   @date : 28 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import time
import pathlib

from src.synthesizer.ProgramGenerator import ProgramGenerator
from src.io.SearchSpaceReader import SearchSpaceReader
from src.metrics.Metric import Metric
from src.metrics.DefaultMetric import DefaultMetric


class BestEffortProgramGenerator(ProgramGenerator):

    def __init__(self, search_space: list[list], max_height: int):
        super().__init__(search_space=search_space, max_height=max_height)

    @staticmethod
    def __get_distance(actual: list, expected: list, metric: Metric):
        res = [metric.distance(actual=actual_example, expected=expected_example)
               for actual_example, expected_example in zip(actual, expected)]
        return sum(res)

    def findBestEffortMatchProgram(self, assignments: list[dict], evaluations: list, error_sum: int,
                                   metric: Metric = DefaultMetric()):
        for program in self.enumerate(assignments=assignments):
            if BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                         expected=evaluations,
                                                         metric=metric) <= error_sum:
                return program

    def findBestEffortAccuracyProgram(self, assignments: list[dict], evaluations: list, error_rate: float,
                                      metric: Metric = DefaultMetric()):
        for program in self.enumerate(assignments=assignments):
            if BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                         expected=evaluations,
                                                         metric=metric) <= error_rate * len(evaluations):
                return program

    def findBestEffortByHeightProgram(self, assignments: list[dict], evaluations: list,
                                      metric: Metric = DefaultMetric()):
        best_program = None
        best_score = len(evaluations) + 1
        for program in self.enumerate(assignments=assignments):
            curr_score = BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                                   expected=evaluations,
                                                                   metric=metric)
            if curr_score < best_score:
                best_program = program
                best_score = curr_score
        return best_program

    def findBestEffortPrograms(self, assignments: list[dict], evaluations: list, programs: int = 5,
                               metric: Metric = DefaultMetric()):
        best_programs = []
        for program in self.enumerate(assignments=assignments):
            curr_score = BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                                   expected=evaluations,
                                                                   metric=metric)
            if len(best_programs) < programs or best_programs[-1][1] > curr_score:
                best_programs.append((program, curr_score))
                best_programs = sorted(best_programs, key=lambda prog: prog[1])[:programs]
        return [program[0] for program in best_programs]

    def findBestEffortByHeightPrograms(self, assignments: list[dict], evaluations: list,
                                       metric: Metric = DefaultMetric()):
        best_programs = [None]
        best_scores = [len(evaluations) + 1]
        for program in self.enumerate(assignments=assignments):
            if len(best_programs) < self._curr_height + 1:
                best_programs += [None] * ((self._curr_height + 1) - len(best_programs))
                best_scores = [len(evaluations) + 1] * ((self._curr_height + 1) - len(best_scores))
            curr_score = BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                                   expected=evaluations,
                                                                   metric=metric)
            if curr_score < best_scores[-1]:
                best_programs[-1] = program
                best_scores[-1] = curr_score
        return best_programs

    def findBestEffortPrioritizingHeightProgram(self, assignments: list[dict], evaluations: list, penalty: float = 0.75,
                                                metric: Metric = DefaultMetric()):
        best_program = None
        best_score = (len(evaluations) + 1) * (penalty ** self._max_height)
        for program in self.enumerate(assignments=assignments):
            curr_score = BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                                   expected=evaluations,
                                                                   metric=metric)
            curr_score *= penalty ** self._curr_height
            if curr_score < best_score:
                best_program = program
                best_score = curr_score
        return best_program

    def findBestEffortUntilInterruptProgram(self, assignments: list[dict], evaluations: list,
                                            metric: Metric = DefaultMetric()):
        best_program = None
        best_score = len(evaluations) + 1
        try:
            for program in self.enumerate(assignments=assignments):
                curr_score = BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                                       expected=evaluations,
                                                                       metric=metric)
                if curr_score < best_score:
                    best_program = program
                    best_score = curr_score
        except KeyboardInterrupt:
            pass
        return best_program


if __name__ == '__main__':
    import ast
    inputs = [{'x': 1, 'y': 2, 'z': 3}, {'x': 2, 'y': 4, 'z': 5}, {'x': 11, 'y': 22, 'z': 3},
              {'x': 0, 'y': -1, 'z': 0}, {'x': 11, 'y': 22, 'z': 4}]
    outputs = list(map(lambda env: env['x'] + env['y'] + env['z'], inputs))
    outputs[-1] -= 1
    search_space1 = SearchSpaceReader.readCSV(pathlib.Path('../../utils/grammars/CsvGrammar.csv')).symbols
    generator = BestEffortProgramGenerator(search_space1, 3)
    # result = generator.findBestEffortAccuracyProgram(inputs, outputs, 0.2)
    # print(ast.unparse(result))
    # result = generator.findBestEffortPrograms(inputs, outputs)
    result = generator.findBestEffortByHeightPrograms(inputs, outputs)
    for res in result:
        print(ast.unparse(res))
    # result = generator.findBestEffortPrioritizingHeightProgram(inputs, outputs, 2)
    # result = generator.findBestEffortUntilInterruptProgram(inputs, outputs)
    # print(ast.unparse(result))
