#
#   @file : RunAllTests.py
#   @date : 16 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
import unittest

from tests.synthesizer.AstNodesTests import AstNodesTests


class MyTestCase(AstNodesTests, unittest.TestCase):
    """
    This class runs all the unittests of this project.
    """

    def testSanityUnittests(self) -> None:
        """
        This unittests ensures that unittest class works correctly.
        :return: None.
        """
        self.assertEqual(True, True)


if __name__ == '__main__':
    """
    If this file is run as the main file, all the tests are run.
    """
    unittest.main()
