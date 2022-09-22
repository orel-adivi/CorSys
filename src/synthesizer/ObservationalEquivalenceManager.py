#
#   @file : ProgramGenerator.py
#   @date : 19 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast


class ObservationalEquivalenceManager(object):

    def __init__(self):
        self._equivalence_classes = {}
        self._program_stack = [[]]

    @staticmethod
    def __generateKey(key: object):
        if type(key) == list:
            return tuple([ObservationalEquivalenceManager.__generateKey(child) for child in key])
        return key

    def isObservationallyEquivalent(self, program: ast):
        return ObservationalEquivalenceManager.__generateKey(program.results) in self._equivalence_classes

    def addEquivalentClass(self, program: ast):
        assert(not self.isObservationallyEquivalent(program))
        self._equivalence_classes[ObservationalEquivalenceManager.__generateKey(program.results)] = program
        self._program_stack[-1].append(program)

    def getAllPreviousHeightPrograms(self):
        return sum(self._program_stack[0:-1], [])

    def getLastHeightPrograms(self):
        if len(self._program_stack) < 2:
            return []
        return self._program_stack[-2]

    def moveNextHeightPrograms(self):
        self._program_stack.append([])
