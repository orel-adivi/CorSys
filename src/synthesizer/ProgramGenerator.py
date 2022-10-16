#
#   @file : ProgramGenerator.py
#   @date : 16 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from itertools import product

from src.synthesizer.ObservationalEquivalenceManager import ObservationalEquivalenceManager


class ProgramGenerator(object):
    """
    This class implements the basic program generator, which finds a program that precisely matches every given
    input-output example.

    Public methods:
        - __init__ - Initialize a ProgramGenerator object.
        - current_height - Return the current height of programs being generated.
        - program_counter - Return how many programs have been generated.
        - enumerate - Generate programs contained in the generator's search space.
        - findProgram - Find a program matching the given input-output examples.
    """

    def __init__(self, search_space: list[list], max_height: int):
        """
        Initialize a ProgramGenerator object.

        :param search_space: The search space to be used by the generator.
        :param max_height: Maximal height of generated programs.
        """
        self._search_space = search_space
        self._max_height = max_height
        self._current_height = 0
        self._program_counter = 0

    @property
    def current_height(self) -> int:
        """
        Return the current height of programs being generated.

        :return: The current height.
        """
        return self._current_height

    @property
    def program_counter(self) -> int:
        """
        Return how many programs have been generated.

        :return: The number of programs have been generated so far.
        """
        return self._program_counter

    def enumerate(self, assignments: list[dict]):
        """
        Generate programs contained in the generator's search space, from programs of height 1 up to the maximal height
        given at initialization.

        :param assignments: Input examples (variables and their assigned values).
        :return: Synthesized programs (using yield, not return).
        """
        observational_equivalence = ObservationalEquivalenceManager()
        for program in [func(children=[], assignments=assignments) for func in self._search_space[0]]:
            if not observational_equivalence.isObservationallyEquivalent(program):
                observational_equivalence.addEquivalentClass(program)
                yield program
        observational_equivalence.moveNextHeightPrograms()
        for height in range(1, self._max_height + 1):
            self._current_height = height
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
                            self._program_counter += 1
                            if not observational_equivalence.isObservationallyEquivalent(program):
                                observational_equivalence.addEquivalentClass(program)
                                yield program
                        except ArithmeticError:
                            continue
                        except BufferError:
                            continue
                        except LookupError:
                            continue
                        except TypeError:
                            continue
                        except ValueError:
                            continue
            observational_equivalence.moveNextHeightPrograms()

    def findProgram(self, assignments: list[dict], evaluations: list):
        """
        Find a program matching the given input-output examples.

        :param assignments: Input examples (variables and their assigned values).
        :param evaluations: Output examples.
        :return: Program matching the given input-output pairs.
        """
        for program in self.enumerate(assignments=assignments):
            if program.value == evaluations:
                return program
