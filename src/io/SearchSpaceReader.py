#
#   @file : SearchSpaceReader.py
#   @date : 28 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import csv
from pathlib import Path

from src.io.SearchSpace import SearchSpace


class SearchSpaceReader(object):

    @staticmethod
    def readCSV(root: Path) -> SearchSpace:
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


if __name__ == "__main__":
    file1 = Path('..\\..\\utils\\grammars\\CsvGrammar.csv')
    res = SearchSpaceReader.readCSV(file1)
    print(res.symbols)

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
