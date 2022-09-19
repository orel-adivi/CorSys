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
            node = generateIntLiteralNode(num, [], [{'x': 0}])
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







"""
testGenerateInverseNode
testGenerateAdditionNode
testGenerateSubtractionNode
testGenerateMultiplicationNode
testGenerateDivisionNode
testGenerateModuloNode
testGeneratePowerNode
testGenerateLeftShiftNode
testGenerateRightShiftNode
testGenerateBitwiseOrNode
testGenerateBitwiseXorNode
testGenerateBitwiseAndNode
"""

if __name__ == '__main__':
    unittest.main()
