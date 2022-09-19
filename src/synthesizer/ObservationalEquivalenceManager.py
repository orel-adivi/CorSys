#
#   @file : ProgramGenerator.py
#   @date : 19 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast

"""
addNewHeightLevel
getPrevHeightLevel
"""


class ObservationalEquivalenceManager(object):

    def __init__(self):
        self._equivalence_classes = {}
        self._program_stack = [[]]

    def isObservationallyEquivalent(self, program: ast):
        return tuple(program.results) in self._equivalence_classes

    def addEquivalentClass(self, program: ast):
        assert(not self.isObservationallyEquivalent(program))
        self._equivalence_classes[tuple(program.results)] = program
        self._program_stack[-1].append(program)

    def getAllPreviousHeightPrograms(self):
        return sum(self._program_stack[0:-1], [])

    def getLastHeightPrograms(self):
        if len(self._program_stack) < 2:
            return []
        return self._program_stack[-2]

    def moveNextHeightPrograms(self):
        self._program_stack.append([])
