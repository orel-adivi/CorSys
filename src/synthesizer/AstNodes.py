#
#   @file : AstNodes.py
#   @date : 19 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast


def generateIntLiteralNode(value: int, children: list, assignments: list):
    node = ast.Constant(value=value)
    node.results = map(lambda inp: value, assignments)
    return node


def generateVariableNode(name: str, children: list, assignments: list):
    node = ast.Name(id=name, ctx=ast.Load())
    node.results = map(lambda inp: inp[name], assignments)
    return node


def generateInverseNode(children: list, assignments: list):
    node = ast.UnaryOp(ast.USub(), children[0])
    node.results = map(lambda inp: -inp, children[0].results)
    return node


def generateBinaryOperationNode(children: list, assignments: list, operation: object, results: list):
    node = ast.BinOp(children[0], operation, children[1])
    node.results = results
    return node


def generateAdditionNode(children: list, assignments: list):
    return generateBinaryOperationNode(children=children,
                                       assignments=assignments,
                                       operation=ast.Add(),
                                       results=map(lambda inp: inp[0] + inp[1],
                                                   zip(children[0].results, children[1].results)))


def generateSubtractionNode(children: list, assignments: list):
    return generateBinaryOperationNode(children=children,
                                       assignments=assignments,
                                       operation=ast.Sub(),
                                       results=map(lambda inp: inp[0] - inp[1],
                                                   zip(children[0].results, children[1].results)))


def generateMultiplicationNode(children: list, assignments: list):
    return generateBinaryOperationNode(children=children,
                                       assignments=assignments,
                                       operation=ast.Mult(),
                                       results=map(lambda inp: inp[0] * inp[1],
                                                   zip(children[0].results, children[1].results)))


def generateDivisionNode(children: list, assignments: list):
    return generateBinaryOperationNode(children=children,
                                       assignments=assignments,
                                       operation=ast.FloorDiv(),
                                       results=map(lambda inp: inp[0] // inp[1],
                                                   zip(children[0].results, children[1].results)))


def generateModuloNode(children: list, assignments: list):
    return generateBinaryOperationNode(children=children,
                                       assignments=assignments,
                                       operation=ast.Mod(),
                                       results=map(lambda inp: inp[0] % inp[1],
                                                   zip(children[0].results, children[1].results)))


def generatePowerNode(children: list, assignments: list):
    return generateBinaryOperationNode(children=children,
                                       assignments=assignments,
                                       operation=ast.Pow(),
                                       results=map(lambda inp: inp[0] ** inp[1],
                                                   zip(children[0].results, children[1].results)))


def generateLeftShiftNode(children: list, assignments: list):
    return generateBinaryOperationNode(children=children,
                                       assignments=assignments,
                                       operation=ast.LShift(),
                                       results=map(lambda inp: inp[0] << inp[1],
                                                   zip(children[0].results, children[1].results)))


def generateRightShiftNode(children: list, assignments: list):
    return generateBinaryOperationNode(children=children,
                                       assignments=assignments,
                                       operation=ast.RShift(),
                                       results=map(lambda inp: inp[0] >> inp[1],
                                                   zip(children[0].results, children[1].results)))


def generateBitwiseOrNode(children: list, assignments: list):
    return generateBinaryOperationNode(children=children,
                                       assignments=assignments,
                                       operation=ast.BitOr(),
                                       results=map(lambda inp: inp[0] | inp[1],
                                                   zip(children[0].results, children[1].results)))


def generateBitwiseXorNode(children: list, assignments: list):
    return generateBinaryOperationNode(children=children,
                                       assignments=assignments,
                                       operation=ast.BitXor(),
                                       results=map(lambda inp: inp[0] ^ inp[1],
                                                   zip(children[0].results, children[1].results)))


def generateBitwiseAndNode(children: list, assignments: list):
    return generateBinaryOperationNode(children=children,
                                       assignments=assignments,
                                       operation=ast.BitAnd(),
                                       results=map(lambda inp: inp[0] & inp[1],
                                                   zip(children[0].results, children[1].results)))
