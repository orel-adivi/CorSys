#
#   @file : ProgramGenerator.py
#   @date : 19 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from functools import partial
from itertools import combinations_with_replacement

from src.synthesizer.AstNodes import *  # todo limit
from src.synthesizer.ObservationalEquivalenceManager import ObservationalEquivalenceManager


class ProgramGenerator(object):

    def __init__(self, literal: list[int], variables: list[str], max_height: int):
        self._search_space = [
            [partial(generateIntLiteralNode, value=num) for num in literal] +
                [partial(generateVariableNode, name=name) for name in variables],
            [generateInverseNode],
            [generateAdditionNode, generateSubtractionNode, generateMultiplicationNode, generateDivisionNode,
             generateModuloNode, generatePowerNode]
        ]
        self._max_height = max_height

    def enumerate(self, assignments: list[dict]):
        observational_equivalence = ObservationalEquivalenceManager()
        for program in [func(children=[], assignments=assignments) for func in self._search_space[0]]:
            if not observational_equivalence.isObservationallyEquivalent(program):
                observational_equivalence.addEquivalentClass(program)
                yield program
        observational_equivalence.moveNextHeightPrograms()
        for height in range(1, self._max_height):
            for arity, functions in zip(range(1, len(self._search_space) + 1), self._search_space[1:]):
                for func in functions:
                    last_height_programs = observational_equivalence.getLastHeightPrograms()
                    prev_height_programs = observational_equivalence.getAllPreviousHeightPrograms()
                    children_list = [list(children)[0:i] + [last_height_program] + list(children)[i:]
                                     for i in range(arity)
                                     for last_height_program in last_height_programs
                                     for children in combinations_with_replacement(prev_height_programs, arity - 1)]
                    for children in children_list:
                        try:
                            program = func(children=children, assignments=assignments)
                            if not observational_equivalence.isObservationallyEquivalent(program):
                                observational_equivalence.addEquivalentClass(program)
                                yield program
                        except ZeroDivisionError:
                            continue

    def findProgram(self, assignments: list[dict], evaluations: list):
        for program in self.enumerate(assignments=assignments):
            if program.results == evaluations:
                return program


if __name__ == '__main__':
    inputs = [{'x': 1, 'y': 2}, {'x': 11, 'y': 20}]
    outputs = [3, 221]
    generator = ProgramGenerator([0, 1, 2], list(inputs[0].keys()), 10)
    result = generator.findProgram(inputs, outputs)
    print(ast.unparse(result))
