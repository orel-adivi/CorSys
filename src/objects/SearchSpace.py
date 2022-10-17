#
#   @file : SearchSpace.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from functools import partial

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

    OPERATION_DICT = [
        {},
        {
            '+': ExpressionGenerator.UnaryOperations.generatePlusNode,
            '-': ExpressionGenerator.UnaryOperations.generateInverseNode,
            'not': ExpressionGenerator.UnaryOperations.generateLogicalNotNode,
            '~': ExpressionGenerator.UnaryOperations.generateBitwiseNotNode,
            '[]': ExpressionGenerator.Subscripting.generateListNode,
            'len': ExpressionGenerator.Functions.generateLenCallNode,
            'sorted': ExpressionGenerator.Functions.generateSortedListNode,
            'reversed': ExpressionGenerator.Functions.generateReversedListNode,
            'capitalize': ExpressionGenerator.Functions.generateCapitalizeCallNode,
            'casefold': ExpressionGenerator.Functions.generateCasefoldCallNode,
            'lower': ExpressionGenerator.Functions.generateLowerCallNode,
            'title': ExpressionGenerator.Functions.generateTitleCallNode,
            'upper': ExpressionGenerator.Functions.generateUpperCallNode,
            'abs': ExpressionGenerator.Functions.generateAbsCallNode
        },
        {
            '+': ExpressionGenerator.BinaryOperations.generateAdditionNode,
            '-': ExpressionGenerator.BinaryOperations.generateSubtractionNode,
            '*': ExpressionGenerator.BinaryOperations.generateMultiplicationNode,
            '/': ExpressionGenerator.BinaryOperations.generateDivisionNode,
            '//': ExpressionGenerator.BinaryOperations.generateFloorDivisionNode,
            '%': ExpressionGenerator.BinaryOperations.generateModuloNode,
            '**': ExpressionGenerator.BinaryOperations.generatePowerNode,
            '<<': ExpressionGenerator.BinaryOperations.generateLeftShiftNode,
            '>>': ExpressionGenerator.BinaryOperations.generateRightShiftNode,
            '|': ExpressionGenerator.BinaryOperations.generateBitwiseOrNode,
            '^': ExpressionGenerator.BinaryOperations.generateBitwiseXorNode,
            '&': ExpressionGenerator.BinaryOperations.generateBitwiseAndNode,
            '@': ExpressionGenerator.BinaryOperations.generateMatrixMultiplicationNode,
            'and': ExpressionGenerator.BooleanOperations.generateLogicalAndNode,
            'or': ExpressionGenerator.BooleanOperations.generateLogicalOrNode,
            '[]': ExpressionGenerator.Subscripting.generateListNode,
            'subscript': ExpressionGenerator.Subscripting.generateSubscriptListNode,
            'index': ExpressionGenerator.Functions.generateIndexCallNode,
            'count': ExpressionGenerator.Functions.generateCountCallNode,
            'join': ExpressionGenerator.Functions.generateJoinCallNode
        },
        {
            'and': ExpressionGenerator.BooleanOperations.generateLogicalAndNode,
            'or': ExpressionGenerator.BooleanOperations.generateLogicalOrNode,
            '[]': ExpressionGenerator.Subscripting.generateListNode
        },
        {
            'and': ExpressionGenerator.BooleanOperations.generateLogicalAndNode,
            'or': ExpressionGenerator.BooleanOperations.generateLogicalOrNode,
            '[]': ExpressionGenerator.Subscripting.generateListNode,
            'slice': ExpressionGenerator.Subscripting.generateSliceListNode
        },
        {
            'and': ExpressionGenerator.BooleanOperations.generateLogicalAndNode,
            'or': ExpressionGenerator.BooleanOperations.generateLogicalOrNode,
            '[]': ExpressionGenerator.Subscripting.generateListNode
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
