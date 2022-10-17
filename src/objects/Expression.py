#
#   @file : Expression.py
#   @date : 18 October 2022
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

    def __init__(self, node_function: Callable, value_function: Callable) -> None:
        """
        Initialize an Expression object.

        :param node_function: the function for evaluation of the node.
        :param value_function: the function for evaluation of the value.
        """
        self.__value = value_function()
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
