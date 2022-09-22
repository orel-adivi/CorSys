#
#   @file : ProgramGenerator.py
#   @date : 22 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from src.synthesizer.ProgramGenerator import ProgramGenerator


class GoodEnoughProgramGenerator(ProgramGenerator):

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
