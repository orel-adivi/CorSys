#
#   @file : AstNodesTests.py
#   @date : 19 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import random
import string
import unittest
from src.synthesizer.AstNodes import *


class MyTestCase(unittest.TestCase):

    def testGenerateIntLiteralNode(self):
        for num in [0, 1, -1] + [random.randint(-(10 ** 100), 10 ** 100) for _ in range(100000)]:
            node = generateLiteralNode(num, [], [{'x': 0}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, num)

    def testGenerateVariableNode(self):
        names = [''.join(random.choice(string.ascii_letters) for _ in range(random.randint(1, 100)))
                 for _ in range(10000)]
        values = [0, 1, -1] + [random.randint(-(10 ** 100), 10 ** 100) for _ in range(len(names) - 3)]
        for name, value in zip(names, values):
            node = generateVariableNode(name, [], [{'x': 0, name: value}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, value)

    def testGenerateInverseNode(self):
        for num in [0, 1, -1] + [random.randint(-(10 ** 100), 10 ** 100) for _ in range(100000)]:
            node = generateInverseNode([generateLiteralNode(num, [], [{'x': 0}])], [{'x': 0}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, -num)

    def testGenerateAdditionNode(self):
        for left, right in [(0, 1), (1, 1), (-1, 1), (1, 2), (1, -2)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(-(10 ** 100), 10 ** 100))
                            for _ in range(100000)]:
            left_node = generateLiteralNode(left, [], [{'x': 0}])
            right_node = generateLiteralNode(right, [], [{'x': 0}])
            node = generateAdditionNode([left_node, right_node], [{'x': 0}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, left + right)

    def testGenerateSubtractionNode(self):
        for left, right in [(0, 1), (1, 1), (-1, 1), (1, 2), (1, -2)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(-(10 ** 100), 10 ** 100))
                            for _ in range(100000)]:
            left_node = generateLiteralNode(left, [], [{'x': 0}])
            right_node = generateLiteralNode(right, [], [{'x': 0}])
            node = generateSubtractionNode([left_node, right_node], [{'x': 0}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, left - right)

    def testGenerateMultiplicationNode(self):
        for left, right in [(0, 1), (1, 1), (-1, 1), (1, 2), (1, -2)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(-(10 ** 100), 10 ** 100))
                            for _ in range(100000)]:
            left_node = generateLiteralNode(left, [], [{'x': 0}])
            right_node = generateLiteralNode(right, [], [{'x': 0}])
            node = generateMultiplicationNode([left_node, right_node], [{'x': 0}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, left * right)

    def testGenerateDivisionNode(self):
        for left, right in [(0, 1), (1, 1), (-1, 1), (1, 2), (1, -2)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(1, 10 ** 100))
                            for _ in range(50000)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(-(10 ** 100), -1))
                            for _ in range(50000)]:
            left_node = generateLiteralNode(left, [], [{'x': 0}])
            right_name = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(1, 100)))
            right_node = generateVariableNode(right_name, [], [{'x': 0, right_name: right}])
            node = generateDivisionNode([left_node, right_node], [{'x': 0, right_name: right}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, left // right)

    def testGenerateModuloNode(self):
        for left, right in [(0, 1), (1, 1), (-1, 1), (1, 2), (1, -2)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(1, 10 ** 100))
                            for _ in range(50000)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(-(10 ** 100), -1))
                            for _ in range(50000)]:
            left_node = generateLiteralNode(left, [], [{'x': 0}])
            right_name = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(1, 100)))
            right_node = generateVariableNode(right_name, [], [{'x': 0, right_name: right}])
            node = generateModuloNode([left_node, right_node], [{'x': 0, right_name: right}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, left % right)

    def testGeneratePowerNode(self):
        for left, right in [(0, 1), (1, 1), (-1, 1), (1, 2), (1, -2)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(1, 250))
                            for _ in range(10000)]:
            left_node = generateLiteralNode(left, [], [{'x': 0}])
            right_node = generateLiteralNode(right, [], [{'x': 0}])
            node = generatePowerNode([left_node, right_node], [{'x': 0}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, left ** right)

    def testGenerateLeftShiftNode(self):
        for left, right in [(0, 1), (1, 1), (-1, 1), (1, 2), (-1, 2)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(0, 150))
                            for _ in range(100000)]:
            left_node = generateLiteralNode(left, [], [{'x': 0}])
            right_node = generateLiteralNode(right, [], [{'x': 0}])
            node = generateLeftShiftNode([left_node, right_node], [{'x': 0}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, left << right)

    def testGenerateRightShiftNode(self):
        for left, right in [(0, 1), (1, 1), (-1, 1), (1, 2), (-1, 2)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(0, 150))
                            for _ in range(100000)]:
            left_node = generateLiteralNode(left, [], [{'x': 0}])
            right_node = generateLiteralNode(right, [], [{'x': 0}])
            node = generateRightShiftNode([left_node, right_node], [{'x': 0}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, left >> right)

    def testGenerateBitwiseOrNode(self):
        for left, right in [(0, 1), (1, 1), (-1, 1), (1, 2), (-1, -2)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(-(10 ** 100), 10 ** 100))
                            for _ in range(100000)]:
            left_node = generateLiteralNode(left, [], [{'x': 0}])
            right_node = generateLiteralNode(right, [], [{'x': 0}])
            node = generateBitwiseOrNode([left_node, right_node], [{'x': 0}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, left | right)

    def testGenerateBitwiseXorNode(self):
        for left, right in [(0, 1), (1, 1), (-1, 1), (1, 2), (-1, -2)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(-(10 ** 100), 10 ** 100))
                            for _ in range(100000)]:
            left_node = generateLiteralNode(left, [], [{'x': 0}])
            right_node = generateLiteralNode(right, [], [{'x': 0}])
            node = generateBitwiseXorNode([left_node, right_node], [{'x': 0}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, left ^ right)

    def testGenerateBitwiseAndNode(self):
        for left, right in [(0, 1), (1, 1), (-1, 1), (1, 2), (-1, -2)] + \
                           [(random.randint(-(10 ** 100), 10 ** 100), random.randint(-(10 ** 100), 10 ** 100))
                            for _ in range(100000)]:
            left_node = generateLiteralNode(left, [], [{'x': 0}])
            right_node = generateLiteralNode(right, [], [{'x': 0}])
            node = generateBitwiseAndNode([left_node, right_node], [{'x': 0}])
            evaluated = node.results[0]
            self.assertEqual(evaluated, left & right)


if __name__ == '__main__':
    unittest.main()
