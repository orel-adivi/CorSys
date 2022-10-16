#
#   @file : SearchSpace.py
#   @date : 16 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from functools import partial

from src.synthesizer.ExpressionGenerator import *  # todo


class SearchSpace(object):
    """
    A SearchSpace object represents a certain search space for the synthesizer - meaning what variables, literals and
    functions the synthesized program may contain.

    Public methods:
        - __init__ - Initialize a SearchSpace objects with no symbols.
        - symbols - Return the symbols (variables, literals, functions) representing the current search space.
        - addVariables - Add variable symbols to the object.
        - addLiterals - Add literal symbols to the object.
        - addFunction - Add a function symbol to the object.
    """

    OPERATION_DICT = [
        {},
        {
            '-': generateInverseNode,
            '[]': generateListNode,
            'len': generateLenCallNode,
            'sorted': generateSortedListNode,
            'reversed': generateReversedListNode
        },
        {
            '+': generateAdditionNode,
            '-': generateSubtractionNode,
            '*': generateMultiplicationNode,
            '/': generateDivisionNode,
            '//': generateFloorDivisionNode,
            '%': generateModuloNode,
            '**': generatePowerNode,
            '[]': generateListNode,
            'subscript': generateSubscriptListNode,
            'index': generateIndexCallNode,
        },
        {
            '[]': generateListNode
        },
        {
            '[]': generateListNode,
            'slice': generateSliceListNode
        }
    ]

    def __init__(self):
        """
        Initialize a SearchSpace objects with no symbols.
        """
        self._symbols = [[]]

    @property
    def symbols(self) -> list[list]:
        """
        Return the symbols (variables, literals, functions) representing the current search space.

        :return: List of input examples (assignments to variables).
        """
        return self._symbols

    def addVariables(self, variables: list[str]) -> None:
        """
        Add variable symbols to the object.

        :param variables: List of symbols to be added.
        :return: None.
        """
        self._symbols[0] = [partial(generateVariableNode, name=variable) for variable in variables] + self._symbols[0]

    def addLiterals(self, literals: list[object]) -> None:
        """
        Add literal symbols to the object.

        :param literals: List of symbols to be added.
        :return: None.
        """
        self._symbols[0] += [partial(generateLiteralNode, value=literal) for literal in literals]

    def addFunction(self, identifier: str, arity: int) -> None:
        """
        Add a function symbol to the object.

        :param identifier: Name of function (in string form).
        :param arity: Arity of function.
        :return: None.
        """
        for _ in range((arity + 1) - len(self._symbols)):
            self._symbols.append([])
        self._symbols[arity].append(SearchSpace.OPERATION_DICT[arity][identifier])
