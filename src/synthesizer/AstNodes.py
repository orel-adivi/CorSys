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
