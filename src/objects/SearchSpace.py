#
#   @file : SearchSpace.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from functools import partial
from typing import Callable

from src.synthesizer.ExpressionGenerator import ExpressionGenerator


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
        self._symbols[0] = [partial(ExpressionGenerator.Terminal.generateVariableNode, name=variable)
                            for variable in variables] + self._symbols[0]

    def addLiterals(self, literals: list[object]) -> None:
        """
        Add literal symbols to the object.

        :param literals: List of symbols to be added.
        :return: None.
        """
        self._symbols[0] += [partial(ExpressionGenerator.Terminal.generateLiteralNode, value=literal)
                             for literal in literals]

    def addFunction(self, function: Callable, arity: int) -> None:
        """
        Add a function symbol to the object.

        :param function: The function.
        :param arity: Arity of function.
        :return: None.
        """
        for _ in range((arity + 1) - len(self._symbols)):
            self._symbols.append([])
        self._symbols[arity].append(function)
