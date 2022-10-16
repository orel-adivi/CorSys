#
#   @file : Expression.py
#   @date : 16 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast
from typing import Callable


class Expression(object):
    """
    This class implements objects representing Python expressions. The evaluation of AST nodes is done lazily.

    Public methods:
        - __init__ - Initialize an Expression object.
        - node - Return the ast describing the node.
        - value - Return the values of the expression.

    """

    class InvalidExpressionError(Exception):
        """
        This class is used for indicating invalid expression object generation.
        """
        pass

    __VALUE_ERROR = InvalidExpressionError("The Expression object value is not valid")

    def __init__(self, node_function: Callable, value_function: Callable) -> None:
        """
        Initialize an Expression object. In case of invalid value, an InvalidExpressionError is raised.

        :param node_function: the function for evaluation of the node.
        :param value_function: the function for evaluation of the value.
        """
        try:
            self.__value = value_function()
        except ArithmeticError:
            raise
        except BufferError:
            raise Expression.__VALUE_ERROR
        except LookupError:
            raise Expression.__VALUE_ERROR
        except TypeError:
            raise Expression.__VALUE_ERROR
        except ValueError:
            raise Expression.__VALUE_ERROR
        self.__node_function = node_function
        self.__node = None
        self.__node_evaluated = False

    @property
    def node(self) -> ast:
        """
        Return the ast describing the node.

        :return: the ast describing the node.
        """
        if not self.__node_evaluated:
            self.__node = self.__node_function()
            self.__node_evaluated = True
        return self.__node

    @property
    def value(self) -> list:
        """
        Return the values of the expression.

        :return: the values of the expression.
        """
        return self.__value
