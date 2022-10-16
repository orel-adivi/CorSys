#
#   @file : ExpressionGenerator.py
#   @date : 17 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast
from typing import Callable

from src.objects.Expression import Expression


class ExpressionGenerator(object):

    class Terminal(object):

        @staticmethod
        def generateLiteralNode(value: object, children: list[Expression], assignments: list[dict]) -> Expression:
            return Expression(
                node_function=lambda: ast.Constant(value=value),
                value_function=lambda: list(map(lambda inp: value, assignments))
            )

        @staticmethod
        def generateVariableNode(name: str, children: list[Expression], assignments: list[dict]) -> Expression:
            return Expression(
                node_function=lambda: ast.Name(id=name, ctx=ast.Load()),
                value_function=lambda: list(map(lambda inp: inp[name], assignments))
            )

    class UnaryOperations(object):

        @staticmethod
        def __generateUnaryOperationNode(children: list[Expression], operation: ast, value_function: Callable):
            return Expression(
                node_function=lambda: ast.UnaryOp(operation, children[0].node),
                value_function=value_function
            )

        @staticmethod
        def generatePlusNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.UnaryOperations.__generateUnaryOperationNode(
                children=children,
                operation=ast.UAdd(),
                value_function=lambda: list(map(lambda inp: +inp, children[0].value))
            )

        @staticmethod
        def generateInverseNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.UnaryOperations.__generateUnaryOperationNode(
                children=children,
                operation=ast.USub(),
                value_function=lambda: list(map(lambda inp: -inp, children[0].value))
            )

        @staticmethod
        def generateLogicalNotNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.UnaryOperations.__generateUnaryOperationNode(
                children=children,
                operation=ast.Not(),
                value_function=lambda: list(map(lambda inp: not inp, children[0].value))
            )

        @staticmethod
        def generateBitwiseNotNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.UnaryOperations.__generateUnaryOperationNode(
                children=children,
                operation=ast.Invert(),
                value_function=lambda: list(map(lambda inp: ~inp, children[0].value))
            )

    class BinaryOperations(object):

        @staticmethod
        def __generateBinaryOperationNode(children: list[Expression], operation: ast, value_function: Callable):
            return Expression(
                node_function=lambda: ast.BinOp(children[0].node, operation, children[1].node),
                value_function=value_function
            )

        @staticmethod
        def generateAdditionNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.Add(),
                value_function=lambda: list(map(lambda inp: inp[0] + inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateSubtractionNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.Sub(),
                value_function=lambda: list(map(lambda inp: inp[0] - inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateMultiplicationNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.Mult(),
                value_function=lambda: list(map(lambda inp: inp[0] * inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateDivisionNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.Div(),
                value_function=lambda: list(map(lambda inp: inp[0] / inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateFloorDivisionNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.FloorDiv(),
                value_function=lambda: list(map(lambda inp: inp[0] // inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateModuloNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.Mod(),
                value_function=lambda: list(map(lambda inp: inp[0] % inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generatePowerNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.Pow(),
                value_function=lambda: list(map(lambda inp: inp[0] ** inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateLeftShiftNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.LShift(),
                value_function=lambda: list(map(lambda inp: inp[0] << inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateRightShiftNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.RShift(),
                value_function=lambda: list(map(lambda inp: inp[0] >> inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateBitwiseOrNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.BitOr(),
                value_function=lambda: list(map(lambda inp: inp[0] | inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateBitwiseXorNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.BitXor(),
                value_function=lambda: list(map(lambda inp: inp[0] ^ inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateBitwiseAndNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.BitAnd(),
                value_function=lambda: list(map(lambda inp: inp[0] & inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateMatrixMultiplicationNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.MatMult(),
                value_function=lambda: list(map(lambda inp: inp[0] @ inp[1],
                                                zip(children[0].value, children[1].value)))
            )

    class BooleanOperations(object):

        @staticmethod
        def __generateBooleanOperationNode(children: list[Expression], operation: ast, value_function: Callable):
            return Expression(
                node_function=lambda: ast.BoolOp(operation, [children[0].node, children[1].node]),
                value_function=value_function
            )

        @staticmethod
        def generateLogicalAndNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BooleanOperations.__generateBooleanOperationNode(
                children=children,
                operation=ast.And(),
                value_function=lambda: list(map(lambda inp: inp[0] and inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateLogicalOrNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.BooleanOperations.__generateBooleanOperationNode(
                children=children,
                operation=ast.Or(),
                value_function=lambda: list(map(lambda inp: inp[0] or inp[1],
                                                zip(children[0].value, children[1].value)))
            )

    class Subscripting(object):

        @staticmethod
        def generateListNode(children: list[Expression], assignments: list[dict]):
            return Expression(
                node_function=lambda: ast.List(elts=[child.node for child in children], ctx=ast.Load()),
                value_function=lambda: [[child.value[i] for child in children] for i in range(len(assignments))]
            )

        @staticmethod
        def generateSubscriptListNode(children: list[Expression], assignments: list[dict]):
            return Expression(
                node_function=lambda: ast.Subscript(value=children[0].node, slice=children[1].node, ctx=ast.Load()),
                value_function=lambda: [(children[0].value[i])[children[1].value[i]] for i in range(len(assignments))]
            )

        @staticmethod
        def generateSliceListNode(children: list[Expression], assignments: list[dict]):
            return Expression(
                node_function=lambda: ast.Subscript(value=children[0].node,
                                                    slice=ast.Slice(lower=children[1].node,
                                                                    upper=children[2].node,
                                                                    step=children[3].node),
                                                    ctx=ast.Load()),
                value_function=lambda:
                    [(children[0].value[i])[(children[1].value[i]):(children[2].value[i]):(children[3].value[i])]
                     for i in range(len(assignments))]
            )

    class Functions(object):

        @staticmethod
        def __generateFunctionCallNode(func: Callable, args: Callable, keywords: Callable, value_function: Callable):
            return Expression(
                node_function=lambda: ast.Call(func=func(), args=args(), keywords=keywords()),
                value_function=value_function
            )

        @staticmethod
        def generateLenCallNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Name(id='len', ctx=ast.Load()),
                args=lambda: [child.node for child in children],
                keywords=lambda: [],
                value_function=lambda: [len(children[0].value[i]) for i in range(len(assignments))]
            )

        @staticmethod
        def generateIndexCallNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Attribute(value=children[0], attr='index', ctx=ast.Load()),
                args=lambda: [children[1].node],
                keywords=lambda: [],
                value_function=lambda: [children[0].value[i].index(children[1].value[i])
                                        for i in range(len(assignments))]
            )

        @staticmethod
        def generateSortedListNode(children: list[Expression], assignments: list[dict]):
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Name(id='sorted', ctx=ast.Load()),
                args=lambda: [child.node for child in children],
                keywords=lambda: [],
                value_function=lambda: [sorted(children[0].value[i]) for i in range(len(assignments))]
            )

        @staticmethod
        def generateReversedListNode(children: list[Expression], assignments: list[dict]):
            iterable_node = ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Name(id='reversed', ctx=ast.Load()),
                args=lambda: [child.node for child in children],
                keywords=lambda: [],
                value_function=lambda: [reversed(children[0].value[i]) for i in range(len(assignments))]
            )
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Name(id='list', ctx=ast.Load()),
                args=lambda: [iterable_node.node],
                keywords=lambda: [],
                value_function=lambda: [list(iterable_node.value[i]) for i in range(len(assignments))]
            )

        # todo
        """
        count
        capitlize
        casefold
        join
        lower
        title
        upper
        abs
        """

    class General(object):
        pass


if __name__ == "__main__":
    exp = ExpressionGenerator.Terminal.generateLiteralNode(1, [], [{'x': 1}])
    exp1 = ExpressionGenerator.UnaryOperations.generateInverseNode([exp], [{'x': 1}])
    print(exp1)
