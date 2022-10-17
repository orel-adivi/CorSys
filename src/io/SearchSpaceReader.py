#
#   @file : SearchSpaceReader.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
import csv
from pathlib import Path

from src.objects.SearchSpace import SearchSpace


class SearchSpaceReader(object):
    """
    A class which allows conversion of a search space for the synthesizer (variables, literals and functions allowed in
    the program) from a CSV file to a SearchSpace object.

    Public method:
        - readCSV - Convert a csv containing symbols to a SearchSpace object.
    """

    @staticmethod
    def readCSV(root: Path) -> SearchSpace:
        """
        Read a csv containing variables, literals and functions and converts it to a SearchSpace object.

        :param root: Path of the csv file to read.
        :return: SearchSpace object containing the information from the CSV file.
        """
        with root.open() as file:
            file_content = list(csv.reader(file))
        literals = [eval(literal) for literal in file_content[0] if literal]
        variables = [variable for variable in file_content[1] if variable]
        result = SearchSpace()
        result.addLiterals(literals=literals)
        result.addVariables(variables=variables)
        for arity, functions in zip(range(1, len(file_content) - 1), file_content[2:]):
            for func in [func for func in functions if func]:
                result.addFunction(identifier=func, arity=arity)
        return result

    # todo - ready to use


# --------------------
#
#
#
# @staticmethod
# def getIntegerOperations(literal: list[int], variables: list[str]):
#     return [
#         [partial(generateVariableNode, name=name) for name in variables] +
#         [partial(generateLiteralNode, value=val) for val in literal],
#         [generateInverseNode],
#         [generateAdditionNode, generateSubtractionNode, generateMultiplicationNode, generateDivisionNode,
#          generateModuloNode, generatePowerNode]
#     ]
#
#
# @staticmethod
# def getStringOperations(literal: list[int], variables: list[str]):
#     pass  # todo
#
#
# @staticmethod
# def getListOperations(literal: list[int], variables: list[str]):
#     pass  # todo
#
#
# @staticmethod
# def readGrammarFromFile(filename: str):
#     search_space = []
#     with open(filename, 'r') as file:
#         lines = file.readlines()
#     literals = [partial(generateLiteralNode, value=eval(val.strip())) for val in lines[0].split(' ')]
#     variables = [partial(generateVariableNode, name=name.strip()) for name in lines[1].split(' ')]
#     search_space.append(variables + literals)
#     for arity, line in zip(range(1, len(lines)), lines[2:]):
#         operations = line.split(' ')
#         funcs = []
#         for operation in [operation.strip() for operation in operations if operation.strip()]:
#             funcs.append(SearchSpace.OPERATION_DICT[arity][operation])
#         search_space.append(funcs)
#     return search_space
#
