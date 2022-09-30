#
#   @file : RunAllTests.py
#   @date : 30 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import unittest

from tests.synthesizer.AstNodesTests import AstNodesTests


class MyTestCase(AstNodesTests, unittest.TestCase):

    def testSanityUnittests(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
