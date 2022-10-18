#
#   @file : SearchSpaceReader.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from functools import partial
from pathlib import Path

from src.objects.SearchSpace import SearchSpace

from src.synthesizer.ExpressionGenerator import ExpressionGenerator


class SearchSpaceReader(object):
    """
    A class which allows conversion of a search space for the synthesizer (variables, literals and functions allowed in
    the program) from a TXT file to a SearchSpace object.

    Public method:
        - readTXT - Convert a TXT containing symbols to a SearchSpace object.
    """

    OPERATION_DICTIONARY = {
        '+ EXP1': (ExpressionGenerator.UnaryOperations.generatePlusNode, 1),
        '- EXP1': (ExpressionGenerator.UnaryOperations.generateInverseNode, 1),
        'not EXP1': (ExpressionGenerator.UnaryOperations.generateLogicalNotNode, 1),
        '~ EXP1': (ExpressionGenerator.UnaryOperations.generateBitwiseNotNode, 1),
        '[EXP1]': (ExpressionGenerator.Subscripting.generateListNode, 1),
        'len(EXP1)': (ExpressionGenerator.Functions.generateLenCallNode, 1),
        'sorted(EXP1)': (ExpressionGenerator.Functions.generateSortedListNode, 1),
        'list(reversed(EXP1))': (ExpressionGenerator.Functions.generateReversedListNode, 1),
        'EXP1.capitalize()': (ExpressionGenerator.Functions.generateCapitalizeCallNode, 1),
        'EXP1.casefold()': (ExpressionGenerator.Functions.generateCasefoldCallNode, 1),
        'EXP1.lower()': (ExpressionGenerator.Functions.generateLowerCallNode, 1),
        'EXP1.title()': (ExpressionGenerator.Functions.generateTitleCallNode, 1),
        'EXP1.upper()': (ExpressionGenerator.Functions.generateUpperCallNode, 1),
        'abs(EXP1)': (ExpressionGenerator.Functions.generateAbsCallNode, 1),
        'EXP1 + EXP2': (ExpressionGenerator.BinaryOperations.generateAdditionNode, 2),
        'EXP1 - EXP2': (ExpressionGenerator.BinaryOperations.generateSubtractionNode, 2),
        'EXP1 * EXP2': (ExpressionGenerator.BinaryOperations.generateMultiplicationNode, 2),
        'EXP1 / EXP2': (ExpressionGenerator.BinaryOperations.generateDivisionNode, 2),
        'EXP1 // EXP2': (ExpressionGenerator.BinaryOperations.generateFloorDivisionNode, 2),
        'EXP1 % EXP2': (ExpressionGenerator.BinaryOperations.generateModuloNode, 2),
        'EXP1 ** EXP2': (ExpressionGenerator.BinaryOperations.generatePowerNode, 2),
        'EXP1 << EXP2': (ExpressionGenerator.BinaryOperations.generateLeftShiftNode, 2),
        'EXP1 >> EXP2': (ExpressionGenerator.BinaryOperations.generateRightShiftNode, 2),
        'EXP1 | EXP2': (ExpressionGenerator.BinaryOperations.generateBitwiseOrNode, 2),
        'EXP1 ^ EXP2': (ExpressionGenerator.BinaryOperations.generateBitwiseXorNode, 2),
        'EXP1 & EXP2': (ExpressionGenerator.BinaryOperations.generateBitwiseAndNode, 2),
        'EXP1 @ EXP2': (ExpressionGenerator.BinaryOperations.generateMatrixMultiplicationNode, 2),
        'EXP1 and EXP2': (ExpressionGenerator.BooleanOperations.generateLogicalAndNode, 2),
        'EXP1 or EXP2': (ExpressionGenerator.BooleanOperations.generateLogicalOrNode, 2),
        '[EXP1, EXP2]': (ExpressionGenerator.Subscripting.generateListNode, 2),
        'EXP1[EXP2]': (ExpressionGenerator.Subscripting.generateSubscriptListNode, 2),
        'EXP1 .index(EXP2)': (ExpressionGenerator.Functions.generateIndexCallNode, 2),
        'EXP1.count(EXP2)': (ExpressionGenerator.Functions.generateCountCallNode, 2),
        'EXP1.join(EXP2)': (ExpressionGenerator.Functions.generateJoinCallNode, 2),
        'EXP1 and EXP2 and EXP3': (ExpressionGenerator.BooleanOperations.generateLogicalAndNode, 3),
        'EXP1 or EXP2 or EXP3': (ExpressionGenerator.BooleanOperations.generateLogicalOrNode, 3),
        '[EXP1, EXP2, EXP3]': (ExpressionGenerator.Subscripting.generateListNode, 3),
        'EXP1 and EXP2 and EXP3 and EXP4': (ExpressionGenerator.BooleanOperations.generateLogicalAndNode, 4),
        'EXP1 or EXP2 or EXP3 or EXP4': (ExpressionGenerator.BooleanOperations.generateLogicalOrNode, 4),
        '[EXP1, EXP2, EXP3, EXP4]': (ExpressionGenerator.Subscripting.generateListNode, 4),
        'EXP1[EXP2:EXP3:EXP4]': (ExpressionGenerator.Subscripting.generateSliceListNode, 4),
        'EXP1 and EXP2 and EXP3 and EXP4 and EXP5': (ExpressionGenerator.BooleanOperations.generateLogicalAndNode, 5),
        'EXP1 or EXP2 or EXP3 or EXP4 or EXP5': (ExpressionGenerator.BooleanOperations.generateLogicalOrNode, 5),
        '[EXP1, EXP2, EXP3, EXP4, EXP5]': (ExpressionGenerator.Subscripting.generateListNode, 5)
    }

    @staticmethod
    def readTXT(root: Path) -> SearchSpace:
        """
        Read a txt containing variables, literals and functions and converts it to a SearchSpace object.

        :param root: Path of the csv file to read.
        :return: SearchSpace object containing the information from the CSV file.
        """
        with root.open() as file:
            lines = file.readlines()
        result = SearchSpace()
        literals, variables = [], []
        for line in [line.split('EXP ::= ')[1].strip() for line in lines]:
            if 'EXP' not in line:
                try:
                    value = eval(line)
                    literals.append(value)
                except NameError:
                    variables.append(line)
            elif line in SearchSpaceReader.OPERATION_DICTIONARY:
                function, arity = SearchSpaceReader.OPERATION_DICTIONARY[line]
                print(f'{function}\t{arity}')
                result.addFunction(function=function, arity=arity)
            else:
                arity = 1
                for i in range(9, 0, -1):
                    if f'EXP{i}' in line:
                        arity = i
                        break
                function = partial(ExpressionGenerator.Generic.generateGenericNode, expr=line)
                print(arity)
                result.addFunction(function=function, arity=arity)
        result.addLiterals(literals=literals)
        result.addVariables(variables=variables)
        return result
