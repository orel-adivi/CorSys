#
#   @file : SearchSpace.py
#   @date : 28 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from functools import partial

from src.synthesizer.AstNodes import *  # todo


class SearchSpace(object):

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
            '//': generateDivisionNode,
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
        self._symbols = [[]]

    @property
    def symbols(self) -> list[list]:
        return self._symbols

    def addVariables(self, variables: list[str]) -> None:
        self._symbols[0] = [partial(generateVariableNode, name=variable) for variable in variables] + self._symbols[0]

    def addLiterals(self, literals: list[object]) -> None:
        self._symbols[0] += [partial(generateLiteralNode, value=literal) for literal in literals]

    def addFunction(self, identifier: str, arity: int) -> None:
        for _ in range((arity + 1) - len(self._symbols)):
            self._symbols.append([])
        self._symbols[arity].append(SearchSpace.OPERATION_DICT[arity][identifier])
