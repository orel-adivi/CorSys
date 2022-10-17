#
#   @file : ExpressionGenerator.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast
from typing import Callable
from itertools import chain

from src.objects.Expression import Expression


class ExpressionGenerator(object):
    """
    This class generate Expression objects representing the AST of a program (later, the actual AST is lazily evaluated
    using these Expressions).

    Public subclasses:
            - class Terminal - This class is used to generate Expressions for literals and variables.
            - class UnaryOperations - This class is used to generate Expressions for unary operations.
            - class BinaryOperations - This class is used to generate Expressions for binary operations.
            - class BooleanOperations - This class is used to generate Expressions for boolean operations.
            - class Subscripting - This class is used to generate Expressions for subscripting-related operations.
            - class Functions - This class is used to generate Expressions for calls to certain known functions.
            - class Generic - This class is used to generate Expressions representing the AST of a program, which will
              be lazily evaluated using python's "eval" function.
    """

    class Terminal(object):
        """
        This class is used to generate Expressions for literals and variables.

        Public methods:
            - generateLiteralNode - Generate an Expression for a literal.
            - generateVariableNode - Generate an Expression for a variable.
        """

        @staticmethod
        def generateLiteralNode(value: object, children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a literal.

            :param value: Value of the literal.
            :param children: The Expression's children in the AST (should be empty here).
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return Expression(
                node_function=lambda: ast.Constant(value=value),
                value_function=lambda: list(map(lambda inp: value, assignments))
            )

        @staticmethod
        def generateVariableNode(name: str, children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a variable.

            :param name: Name of the variable.
            :param children: The Expression's children in the AST (should be empty here).
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return Expression(
                node_function=lambda: ast.Name(id=name, ctx=ast.Load()),
                value_function=lambda: list(map(lambda inp: inp[name], assignments))
            )

    class UnaryOperations(object):
        """
        This class is used to generate Expressions for unary operations.

        Public methods:
            - generatePlusNode - Generate an Expression for an unary plus operation.
            - generateInverseNode - Generate an Expression for an unary minus operation.
            - generateLogicalNotNode - Generate an Expression for a logical not operation.
            - generateBitwiseNotNode - Generate an Expression for a bitwise not operation.
        """

        @staticmethod
        def __generateUnaryOperationNode(children: list[Expression], operation: ast, value_function: Callable) -> \
                Expression:
            """
            Create an Expression for a given unary operation.

            :param children: The Expression's children in the AST.
            :param operation: The chosen unary operation.
            :param value_function: The function to be used for computing the Expression's value.
            :return: The new Expression.
            """
            return Expression(
                node_function=lambda: ast.UnaryOp(operation, children[0].node),
                value_function=value_function
            )

        @staticmethod
        def generatePlusNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for an unary plus operation (+).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.UnaryOperations.__generateUnaryOperationNode(
                children=children,
                operation=ast.UAdd(),
                value_function=lambda: list(map(lambda inp: +inp, children[0].value))
            )

        @staticmethod
        def generateInverseNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for an unary minus operation (-).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.UnaryOperations.__generateUnaryOperationNode(
                children=children,
                operation=ast.USub(),
                value_function=lambda: list(map(lambda inp: -inp, children[0].value))
            )

        @staticmethod
        def generateLogicalNotNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a logical not operation (not).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.UnaryOperations.__generateUnaryOperationNode(
                children=children,
                operation=ast.Not(),
                value_function=lambda: list(map(lambda inp: not inp, children[0].value))
            )

        @staticmethod
        def generateBitwiseNotNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a bitwise not operation (~).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.UnaryOperations.__generateUnaryOperationNode(
                children=children,
                operation=ast.Invert(),
                value_function=lambda: list(map(lambda inp: ~inp, children[0].value))
            )

    class BinaryOperations(object):
        """
        This class is used to generate Expressions for binary operations.

        Public methods:
            - generateAdditionNode - Generate an Expression for a binary plus operation.
            - generateSubtractionNode - Generate an Expression for a binary minus operation.
            - generateMultiplicationNode - Generate an Expression for a multiplication operation.
            - generateDivisionNode - Generate an Expression for a float division operation.
            - generateFloorDivisionNode - Generate an Expression for an integer division operation.
            - generateModuloNode - Generate an Expression for a modulo operation.
            - generatePowerNode - Generate an Expression for a power operation.
            - generateLeftShiftNode - Generate an Expression for a left shift operation.
            - generateRightShiftNode - Generate an Expression for a left shift operation.
            - generateBitwiseOrNode - Generate an Expression for a bitwise or operation.
            - generateBitwiseXorNode - Generate an Expression for a bitwise xor operation.
            - generateBitwiseAndNode - Generate an Expression for a bitwise and operation.
            - generateMatrixMultiplicationNode - Generate an Expression for a matrix multiplication operation.
        """

        @staticmethod
        def __generateBinaryOperationNode(children: list[Expression], operation: ast, value_function: Callable) -> \
                Expression:
            """
            Create an Expression for a given binary operation.

            :param children: The Expression's children in the AST.
            :param operation: The chosen binary operation.
            :param value_function: The function to be used for computing the Expression's value.
            :return: The new Expression.
            """
            return Expression(
                node_function=lambda: ast.BinOp(children[0].node, operation, children[1].node),
                value_function=value_function
            )

        @staticmethod
        def generateAdditionNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a binary plus operation (+).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.Add(),
                value_function=lambda: list(map(lambda inp: inp[0] + inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateSubtractionNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a binary minus operation (-).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.Sub(),
                value_function=lambda: list(map(lambda inp: inp[0] - inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateMultiplicationNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a multiplication operation (*).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.Mult(),
                value_function=lambda: list(map(lambda inp: inp[0] * inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateDivisionNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a float division operation (/).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.Div(),
                value_function=lambda: list(map(lambda inp: inp[0] / inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateFloorDivisionNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for an integer division operation (//).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.FloorDiv(),
                value_function=lambda: list(map(lambda inp: inp[0] // inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateModuloNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a modulo operation (%).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.Mod(),
                value_function=lambda: list(map(lambda inp: inp[0] % inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generatePowerNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a power operation (**).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.Pow(),
                value_function=lambda: list(map(lambda inp: inp[0] ** inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateLeftShiftNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a left shift operation (<<).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.LShift(),
                value_function=lambda: list(map(lambda inp: inp[0] << inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateRightShiftNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a right shift operation (>>).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.RShift(),
                value_function=lambda: list(map(lambda inp: inp[0] >> inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateBitwiseOrNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a bitwise or operation (|).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.BitOr(),
                value_function=lambda: list(map(lambda inp: inp[0] | inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateBitwiseXorNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a bitwise xor operation (^).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.BitXor(),
                value_function=lambda: list(map(lambda inp: inp[0] ^ inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateBitwiseAndNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a bitwise and operation (&).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.BitAnd(),
                value_function=lambda: list(map(lambda inp: inp[0] & inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateMatrixMultiplicationNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a matrix multiplication operation (@).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BinaryOperations.__generateBinaryOperationNode(
                children=children,
                operation=ast.MatMult(),
                value_function=lambda: list(map(lambda inp: inp[0] @ inp[1],
                                                zip(children[0].value, children[1].value)))
            )

    class BooleanOperations(object):
        """
        This class is used to generate Expressions for boolean operations.

        Public methods:
            - generateLogicalAndNode - Generate an Expression for a logical and operation.
            - generateLogicalOrNode - Generate an Expression for a logical or operation.
        """

        @staticmethod
        def __generateBooleanOperationNode(children: list[Expression], operation: ast, value_function: Callable) -> \
                Expression:
            """
            Create an Expression for a given boolean operation.

            :param children: The Expression's children in the AST.
            :param operation: The chosen boolean operation.
            :param value_function: The function to be used for computing the Expression value.
            :return: The new Expression
            """
            return Expression(
                node_function=lambda: ast.BoolOp(operation, [children[0].node, children[1].node]),
                value_function=value_function
            )

        @staticmethod
        def generateLogicalAndNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a logical and operation (and).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BooleanOperations.__generateBooleanOperationNode(
                children=children,
                operation=ast.And(),
                value_function=lambda: list(map(lambda inp: inp[0] and inp[1],
                                                zip(children[0].value, children[1].value)))
            )

        @staticmethod
        def generateLogicalOrNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a logical or operation (or).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.BooleanOperations.__generateBooleanOperationNode(
                children=children,
                operation=ast.Or(),
                value_function=lambda: list(map(lambda inp: inp[0] or inp[1],
                                                zip(children[0].value, children[1].value)))
            )

    class Subscripting(object):
        """
        This class is used to generate Expressions for subscripting-related operations.

        Public methods:
            - generateListNode - Generate an Expression for a list-creation operation (wrapping value in []).
            - generateSubscriptListNode - Generate an Expression for a list-item access operation.
            - generateSliceListNode - Generate an Expression for a list slice operation.
        """

        @staticmethod
        def generateListNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a list-creation operation (wrapping value in []).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return Expression(
                node_function=lambda: ast.List(elts=[child.node for child in children], ctx=ast.Load()),
                value_function=lambda: [[child.value[i] for child in children] for i in range(len(assignments))]
            )

        @staticmethod
        def generateSubscriptListNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a list-item access operation (l[]).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return Expression(
                node_function=lambda: ast.Subscript(value=children[0].node, slice=children[1].node, ctx=ast.Load()),
                value_function=lambda: [(children[0].value[i])[children[1].value[i]] for i in range(len(assignments))]
            )

        @staticmethod
        def generateSliceListNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a list slice operation (l[::]).

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
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
        """
        This class is used to generate Expressions for calls to certain known functions.

        Public methods:
            - generateLenCallNode - Generate an Expression for a call to the "len" function.
            - generateIndexCallNode - Generate an Expression for a call to the "index" function.
            - generateSortedListNode - Generate an Expression for a call to the "sorted" function.
            - generateReversedListNode - Generate an Expression for a call to the "reversed" function.
            - generateCountCallNode - Generate an Expression for a call to the "count" function.
            - generateJoinCallNode - Generate an Expression for a call to the "join" function.
            - generateCapitalizeCallNode - Generate an Expression for a call to the "capitalize" function.
            - generateCasefoldCallNode - Generate an Expression for a call to the "casefold" function.
            - generateLowerCallNode - Generate an Expression for a call to the "lower" function.
            - generateTitleCallNode - Generate an Expression for a call to the "title" function.
            - generateUpperCallNode - Generate an Expression for a call to the "upper" function.
            - generateAbsCallNode - Generate an Expression for a call to the "abs" function.
        """

        @staticmethod
        def __generateFunctionCallNode(func: Callable, args: Callable, keywords: Callable, value_function: Callable) ->\
                Expression:
            """
            Create an Expression for a function call.

            :param func: The chosen function.
            :param args: The arguments used in the call.
            :param keywords: The keyword arguments used in the call.
            :param value_function: The function to be used for computing the Expression value.
            :return: The new Expression.
            """
            return Expression(
                node_function=lambda: ast.Call(func=func(), args=args(), keywords=keywords()),
                value_function=value_function
            )

        @staticmethod
        def generateLenCallNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a call to the "len" function.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Name(id='len', ctx=ast.Load()),
                args=lambda: [child.node for child in children],
                keywords=lambda: [],
                value_function=lambda: [len(children[0].value[i]) for i in range(len(assignments))]
            )

        @staticmethod
        def generateIndexCallNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a call to the "index" function.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Attribute(value=children[0].node, attr='index', ctx=ast.Load()),
                args=lambda: [children[1].node],
                keywords=lambda: [],
                value_function=lambda: [children[0].value[i].index(children[1].value[i])
                                        for i in range(len(assignments))]
            )

        @staticmethod
        def generateSortedListNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a call to the "sorted" function.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Name(id='sorted', ctx=ast.Load()),
                args=lambda: [child.node for child in children],
                keywords=lambda: [],
                value_function=lambda: [sorted(children[0].value[i]) for i in range(len(assignments))]
            )

        @staticmethod
        def generateReversedListNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a call to the "reversed" function.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
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

        @staticmethod
        def generateCountCallNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a call to the "count" function.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Attribute(value=children[0].node, attr='count', ctx=ast.Load()),
                args=lambda: [children[1].node],
                keywords=lambda: [],
                value_function=lambda: [children[0].value[i].count(children[1].value[i])
                                        for i in range(len(assignments))]
            )

        @staticmethod
        def generateJoinCallNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a call to the "join" function.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Attribute(value=children[0].node, attr='join', ctx=ast.Load()),
                args=lambda: [children[1].node],
                keywords=lambda: [],
                value_function=lambda: [children[0].value[i].join(children[1].value[i])
                                        for i in range(len(assignments))]
            )

        @staticmethod
        def generateCapitalizeCallNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a call to the "capitalize" function.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Attribute(value=children[0].node, attr='capitalize', ctx=ast.Load()),
                args=lambda: [],
                keywords=lambda: [],
                value_function=lambda: [children[0].value[i].capitalize()
                                        for i in range(len(assignments))]
            )

        @staticmethod
        def generateCasefoldCallNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a call to the "casefold" function.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Attribute(value=children[0].node, attr='casefold', ctx=ast.Load()),
                args=lambda: [],
                keywords=lambda: [],
                value_function=lambda: [children[0].value[i].casefold()
                                        for i in range(len(assignments))]
            )

        @staticmethod
        def generateLowerCallNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a call to the "lower" function.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Attribute(value=children[0].node, attr='lower', ctx=ast.Load()),
                args=lambda: [],
                keywords=lambda: [],
                value_function=lambda: [children[0].value[i].lower()
                                        for i in range(len(assignments))]
            )

        @staticmethod
        def generateTitleCallNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a call to the "title" function.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Attribute(value=children[0].node, attr='title', ctx=ast.Load()),
                args=lambda: [],
                keywords=lambda: [],
                value_function=lambda: [children[0].value[i].title()
                                        for i in range(len(assignments))]
            )

        @staticmethod
        def generateUpperCallNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a call to the "upper" function.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Attribute(value=children[0].node, attr='upper', ctx=ast.Load()),
                args=lambda: [],
                keywords=lambda: [],
                value_function=lambda: [children[0].value[i].upper()
                                        for i in range(len(assignments))]
            )

        @staticmethod
        def generateAbsCallNode(children: list[Expression], assignments: list[dict]) -> Expression:
            """
            Generate an Expression for a call to the "abs" function.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :return: The new Expression.
            """
            return ExpressionGenerator.Functions.__generateFunctionCallNode(
                func=lambda: ast.Name(id='abs', ctx=ast.Load()),
                args=lambda: [child.node for child in children],
                keywords=lambda: [],
                value_function=lambda: [abs(children[0].value[i]) for i in range(len(assignments))]
            )

    class Generic(object):
        """
        This class is used to generate Expressions representing the AST of a program, which will be lazily evaluated
        using python's "eval" function.

        Public methods:
            - generateGenericNode - Create an AST from a list of children and a root.
        """

        @staticmethod
        def __generateAstForGenericNode(children: list[Expression], expr: str) -> ast:
            """
            Create an AST from a list of children and a root.

            :param children: List of Expressions representing the AST children.
            :param expr: The AST's root in string form.
            :return: The new AST.
            """
            for i in range(len(children)):
                expr = expr.replace(f'EXP{i + 1}', f'({ast.unparse(children[i].node)})')
            return ast.parse(expr)

        @staticmethod
        def generateGenericNode(children: list[Expression], assignments: list[dict], expr: str) -> Expression:
            """
            Generate an Expression representing the root of an AST.

            :param children: The Expression's children in the AST.
            :param assignments: Input examples (variables and their assigned values).
            :param expr: The AST root in string form.
            :return: The new Expression.
            """
            return Expression(
                node_function=lambda: ExpressionGenerator.Generic.__generateAstForGenericNode(children, expr),
                value_function=lambda:
                    [eval(expr, dict(chain.from_iterable(
                        d.items() for d in (assignments[i],
                                            {f'EXP{j + 1}': children[j].value[i] for j in range(len(children))}))))
                     for i in range(len(assignments))]
            )
