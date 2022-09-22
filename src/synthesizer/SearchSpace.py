#
#   @file : SearchSpace.py
#   @date : 19 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
from functools import partial

from src.synthesizer.AstNodes import *


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

    @staticmethod
    def getIntegerOperations(literal: list[int], variables: list[str]):
        return [
            [partial(generateVariableNode, name=name) for name in variables] +
            [partial(generateLiteralNode, value=val) for val in literal],
            [generateInverseNode],
            [generateAdditionNode, generateSubtractionNode, generateMultiplicationNode, generateDivisionNode,
             generateModuloNode, generatePowerNode]
        ]

    @staticmethod
    def getStringOperations(literal: list[int], variables: list[str]):
        pass    # todo

    @staticmethod
    def getListOperations(literal: list[int], variables: list[str]):
        pass    # todo

    @staticmethod
    def readGrammarFromFile(filename: str):
        search_space = []
        with open(filename, 'r') as file:
            lines = file.readlines()
        literals = [partial(generateLiteralNode, value=eval(val.strip())) for val in lines[0].split(' ')]
        variables = [partial(generateVariableNode, name=name.strip()) for name in lines[1].split(' ')]
        search_space.append(variables + literals)
        for arity, line in zip(range(1, len(lines)), lines[2:]):
            operations = line.split(' ')
            funcs = []
            for operation in [operation.strip() for operation in operations if operation.strip()]:
                funcs.append(SearchSpace.OPERATION_DICT[arity][operation])
            search_space.append(funcs)
        return search_space
