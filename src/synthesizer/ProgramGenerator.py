#
#   @file : ProgramGenerator.py
#   @date : 22 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from itertools import product

from src.synthesizer.ObservationalEquivalenceManager import ObservationalEquivalenceManager


class ProgramGenerator(object):

    def __init__(self, search_space: list[list], max_height: int):
        self._search_space = search_space
        self._max_height = max_height

    def enumerate(self, assignments: list[dict]):
        observational_equivalence = ObservationalEquivalenceManager()
        for program in [func(children=[], assignments=assignments) for func in self._search_space[0]]:
            if not observational_equivalence.isObservationallyEquivalent(program):
                observational_equivalence.addEquivalentClass(program)
                yield program
        observational_equivalence.moveNextHeightPrograms()
        for _ in range(1, self._max_height):
            for arity, functions in zip(range(1, len(self._search_space) + 1), self._search_space[1:]):
                for func in functions:
                    last_height_programs = observational_equivalence.getLastHeightPrograms()
                    prev_height_programs = observational_equivalence.getAllPreviousHeightPrograms()
                    children_list = [list(children)[0:i] + [last_height_program] + list(children)[i:]
                                     for i in range(arity)
                                     for last_height_program in last_height_programs
                                     for children in product(prev_height_programs, repeat=arity-1)]
                    for children in children_list:
                        try:
                            program = func(children=children, assignments=assignments)
                            if not observational_equivalence.isObservationallyEquivalent(program):
                                observational_equivalence.addEquivalentClass(program)
                                yield program
                        except Exception:
                            continue
            observational_equivalence.moveNextHeightPrograms()

    def findProgram(self, assignments: list[dict], evaluations: list):
        for program in self.enumerate(assignments=assignments):
            if program.results == evaluations:
                return program
