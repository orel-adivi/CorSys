#
#   @file : AstNodes.py
#   @date : 19 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast


# -------------------- Null-ary operations: --------------------

def generateLiteralNode(value: object, children: list, assignments: list[dict]):
    node = ast.Constant(value=value)
    node.results = list(map(lambda inp: value, assignments))
    return node


def generateVariableNode(name: str, children: list, assignments: list[dict]):
    node = ast.Name(id=name, ctx=ast.Load())
    node.results = list(map(lambda inp: inp[name], assignments))
    return node


# -------------------- Unary operations: --------------------

def __generateUnaryOperationNode(children: list, operation: object, results: list):
    node = ast.UnaryOp(operation, children[0])
    node.results = results
    return node


def generateInverseNode(children: list, assignments: list[dict]):
    return __generateUnaryOperationNode(children=children,
                                        operation=ast.USub(),
                                        results=list(map(lambda inp: -inp, children[0].results)))


# -------------------- Binary operations: --------------------
"""
    +
    -
    *
    //
    %
    *
    <<
    >>
    |
    ^
    &
"""


def __generateBinaryOperationNode(children: list, operation: object, results: list):
    node = ast.BinOp(children[0], operation, children[1])
    node.results = results
    return node


def generateAdditionNode(children: list, assignments: list[dict]):
    return __generateBinaryOperationNode(children=children,
                                         operation=ast.Add(),
                                         results=list(map(lambda inp: inp[0] + inp[1],
                                                          zip(children[0].results, children[1].results))))


def generateSubtractionNode(children: list, assignments: list[dict]):
    return __generateBinaryOperationNode(children=children,
                                         operation=ast.Sub(),
                                         results=list(map(lambda inp: inp[0] - inp[1],
                                                          zip(children[0].results, children[1].results))))


def generateMultiplicationNode(children: list, assignments: list[dict]):
    return __generateBinaryOperationNode(children=children,
                                         operation=ast.Mult(),
                                         results=list(map(lambda inp: inp[0] * inp[1],
                                                          zip(children[0].results, children[1].results))))


def generateDivisionNode(children: list, assignments: list[dict]):
    return __generateBinaryOperationNode(children=children,
                                         operation=ast.FloorDiv(),
                                         results=list(map(lambda inp: inp[0] // inp[1],
                                                          zip(children[0].results, children[1].results))))


def generateModuloNode(children: list, assignments: list[dict]):
    return __generateBinaryOperationNode(children=children,
                                         operation=ast.Mod(),
                                         results=list(map(lambda inp: inp[0] % inp[1],
                                                          zip(children[0].results, children[1].results))))


def generatePowerNode(children: list, assignments: list[dict]):
    return __generateBinaryOperationNode(children=children,
                                         operation=ast.Pow(),
                                         results=list(map(lambda inp: inp[0] ** inp[1],
                                                          zip(children[0].results, children[1].results))))


def generateLeftShiftNode(children: list, assignments: list[dict]):
    return __generateBinaryOperationNode(children=children,
                                         operation=ast.LShift(),
                                         results=list(map(lambda inp: inp[0] << inp[1],
                                                          zip(children[0].results, children[1].results))))


def generateRightShiftNode(children: list, assignments: list[dict]):
    return __generateBinaryOperationNode(children=children,
                                         operation=ast.RShift(),
                                         results=list(map(lambda inp: inp[0] >> inp[1],
                                                          zip(children[0].results, children[1].results))))


def generateBitwiseOrNode(children: list, assignments: list[dict]):
    return __generateBinaryOperationNode(children=children,
                                         operation=ast.BitOr(),
                                         results=list(map(lambda inp: inp[0] | inp[1],
                                                          zip(children[0].results, children[1].results))))


def generateBitwiseXorNode(children: list, assignments: list[dict]):
    return __generateBinaryOperationNode(children=children,
                                         operation=ast.BitXor(),
                                         results=list(map(lambda inp: inp[0] ^ inp[1],
                                                          zip(children[0].results, children[1].results))))


def generateBitwiseAndNode(children: list, assignments: list[dict]):
    return __generateBinaryOperationNode(children=children,
                                         operation=ast.BitAnd(),
                                         results=list(map(lambda inp: inp[0] & inp[1],
                                                          zip(children[0].results, children[1].results))))


# -------------------- List operations: --------------------

def generateListNode(children: list, assignments: list[dict]):
    node = ast.List(elts=children, ctx=ast.Load())
    node.results = [[child.results[i] for child in children] for i in range(len(assignments))]
    return node


def generateSubscriptListNode(children: list, assignments: list[dict]):
    list_to_process, index = children
    node = ast.Subscript(value=list_to_process, slice=index, ctx=ast.Load())
    node.results = [(list_to_process.results[i])[index.results[i]] for i in range(len(assignments))]
    return node


def generateSliceListNode(children: list, assignments: list[dict]):
    list_to_process, lower, upper, step = children
    node = ast.Subscript(value=list_to_process, slice=ast.Slice(lower=lower, upper=upper, step=step), ctx=ast.Load())
    node.results = [(list_to_process.results[i])[(lower.results[i]):(upper.results[i]):(step.results[i])]
                    for i in range(len(assignments))]
    return node


def __generateFunctionCallNode(func: ast, args: list, keywords: list, results: list):
    node = ast.Call(func=func, args=args, keywords=keywords)
    node.results = results
    return node


def generateLenCallNode(children: list, assignments: list[dict]):
    return __generateFunctionCallNode(func=ast.Name(id='len', ctx=ast.Load()),
                                      args=children,
                                      keywords=[],
                                      results=[len(children[0].results[i]) for i in range(len(assignments))])


def generateIndexCallNode(children: list, assignments: list[dict]):
    return __generateFunctionCallNode(func=ast.Attribute(value=children[0], attr='index', ctx=ast.Load()),
                                      args=[children[1]],
                                      keywords=[],
                                      results=[children[0].results[i].index(children[1].results[i])
                                               for i in range(len(assignments))])


def generateSortedListNode(children: list, assignments: list[dict]):
    return __generateFunctionCallNode(func=ast.Name(id='sorted', ctx=ast.Load()),
                                      args=children,
                                      keywords=[],
                                      results=[sorted(children[0].results[i]) for i in range(len(assignments))])


def generateReversedListNode(children: list, assignments: list[dict]):
    iter_node = __generateFunctionCallNode(func=ast.Name(id='reversed', ctx=ast.Load()),
                                           args=children,
                                           keywords=[],
                                           results=[reversed(children[0].results[i]) for i in range(len(assignments))])
    return __generateFunctionCallNode(func=ast.Name(id='list', ctx=ast.Load()),
                                      args=[iter_node],
                                      keywords=[],
                                      results=[list(iter_node.results[i]) for i in range(len(assignments))])


if __name__ == '__main__':
    assignments0 = [{'X': 0}, {'X': 1}]
    lst = [generateLiteralNode(value=i, children=[], assignments=assignments0) for i in [1, 2, 3]]
    lst.append(generateVariableNode('X', [], assignments0))
    node0 = generateListNode(lst, assignments0)
    print(ast.unparse(node0))
    for i in range(len(assignments0)):
        print(node0.results[i])
    print('')

    node1 = generateSubscriptListNode([node0, generateLiteralNode(3, children=[], assignments=assignments0)], assignments0)
    print(ast.unparse(node1))
    for i in range(len(assignments0)):
        print(node1.results[i])
    print('')

    params = [node0,
              generateLiteralNode(1, children=[], assignments=assignments0),
              generateLiteralNode(4, children=[], assignments=assignments0),
              generateLiteralNode(2, children=[], assignments=assignments0)]
    node2 = generateSliceListNode(params, assignments0)
    print(ast.unparse(node2))
    for i in range(len(assignments0)):
        print(node2.results[i])
    print('')

    for i in range(5):
        print("--- Curr i is ", i, ":")
        curr_lst = [generateLiteralNode(value=j, children=[], assignments=assignments0) for j in range(i)]
        curr_node = generateListNode(curr_lst, assignments0)
        print(ast.unparse(curr_node))
        curr_len = generateLenCallNode([curr_node], assignments0)
        print(ast.unparse(curr_len))
        print(curr_len.results[0])
    print('')

    node3 = generateReversedListNode([node0], assignments0)
    print(ast.unparse(node3))
    for i in range(len(assignments0)):
        print(node3.results[i])
    print('')

    node4 = generateSortedListNode([node0], assignments0)
    print(ast.unparse(node4))
    for i in range(len(assignments0)):
        print(node4.results[i])
    print('')

    node5 = generateIndexCallNode([node0, generateLiteralNode(value=3, children=[], assignments=assignments0)],
                                  assignments0)
    print(ast.unparse(node5))
    for i in range(len(assignments0)):
        print(node5.results[i])
    print('')



