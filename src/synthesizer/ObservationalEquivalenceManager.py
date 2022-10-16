#
#   @file : ProgramGenerator.py
#   @date : 16 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast


class ObservationalEquivalenceManager(object):
    """
    This class tracks the equivalence classes of generated programs and allows to check whether a given program is in an
    already existing equivalence class.

    Public methods:
        - __init__ - Initialize a new ObservationalEquivalenceManager object.
        - isObservationallyEquivalent - Check if a given program is equivalent to some previously generated program.
        - addEquivalentClass - Add a new equivalence class.
        - getAllPreviousHeightPrograms - Retrieve the generated programs with a lower height than the current height
          being generated.
        - getLastHeightPrograms - Retrieve the generated programs with a height smaller by one than the current height
          being generated.
        - moveNextHeightPrograms - Update the inner fields of the object when the generator moves on to generate
          programs of the next height.
    """

    def __init__(self) -> None:
        """
        Initialize a new ObservationalEquivalenceManager object.
        """
        self._equivalence_classes = {}
        self._program_stack = [[]]

    @staticmethod
    def __generateKey(key: object) -> object:
        """
        Recursively convert a given value into a valid dictionary key.

        :param key: The value to convert.
        :return: A valid dictionary key.
        """
        if type(key) == list:
            return tuple([ObservationalEquivalenceManager.__generateKey(child) for child in key])
        return key

    def isObservationallyEquivalent(self, program: ast) -> bool:
        """
        Check if a given program is equivalent to some previously generated program.

        :param program: New program to be checked.
        :return: True if the program is equivalent to a previous one and otherwise False.
        """
        return ObservationalEquivalenceManager.__generateKey(program.results) in self._equivalence_classes

    def addEquivalentClass(self, program: ast) -> None:
        """
        Add a new equivalence class of programs.

        :param program: A program representing the new equivalence class.
        :return: None.
        """
        assert(not self.isObservationallyEquivalent(program))
        self._equivalence_classes[ObservationalEquivalenceManager.__generateKey(program.results)] = program
        self._program_stack[-1].append(program)

    def getAllPreviousHeightPrograms(self) -> list:
        """
        Retrieve the generated programs with a lower height than the current height being generated.

        :return: A list of the generated programs with a lower height than the current height being generated.
        """
        return sum(self._program_stack[0:-1], [])

    def getLastHeightPrograms(self) -> list:
        """
        Retrieve the generated programs with a height smaller by one than the current height being generated.

        :return: A list of the generated programs with a height smaller by one than the current height being generated.
        """
        if len(self._program_stack) < 2:
            return []
        return self._program_stack[-2]

    def moveNextHeightPrograms(self) -> None:
        """
        Update the inner fields of the object when the generator moves on to generate programs of the next height.

        :return: None.
        """
        self._program_stack.append([])
