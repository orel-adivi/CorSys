#
#   @file : BenchmarkTests.py
#   @date : 28 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import os
import unittest


class BenchmarkTests(unittest.TestCase):

    def testSumExamples(self):
        os.system("python ..\\..\\Synthesizer.py -io ..\\..\\utils\\examples\\SumExamples.csv "
                  "-s ..\\..\\utils\\grammars\\SumGrammar.csv -m DefaultMetric -t height -mh 3 > .\\temp_out.txt")
        with open('.\\temp_out.txt', 'r') as file:
            content = file.read()
        os.remove('.\\temp_out.txt')
        self.assertEqual("x + y + z", content.strip())

    def testNoisyExamples(self):
        os.system("python ..\\..\\Synthesizer.py -io ..\\..\\utils\\examples\\NoisyExamples.csv "
                  "-s ..\\..\\utils\\grammars\\NoisyGrammar.csv -m NormalMetric -t interrupt -mh 3 > .\\temp_out.txt")
        with open('.\\temp_out.txt', 'r') as file:
            content = file.read()
        os.remove('.\\temp_out.txt')
        self.assertEqual("x * y + z", content.strip())

    def testListExamples(self):
        os.system("python ..\\..\\Synthesizer.py -io ..\\..\\utils\\examples\\ListExamples.csv "
                  "-s ..\\..\\utils\\grammars\\ListGrammar.csv -m DefaultMetric -t height -mh 3 > .\\temp_out.txt")
        with open('.\\temp_out.txt', 'r') as file:
            content = file.read()
        os.remove('.\\temp_out.txt')
        self.assertEqual("sorted(x)[0:None:2]", content.strip())

    def testStringExamples(self):
        os.system("python ..\\..\\Synthesizer.py -io ..\\..\\utils\\examples\\StringExamples.csv "
                  "-s ..\\..\\utils\\grammars\\StringGrammar.csv -m LevenshteinMetric -mp False "
                  "-t interrupt -mh 3 > .\\temp_out.txt")
        with open('.\\temp_out.txt', 'r') as file:
            content = file.read()
        os.remove('.\\temp_out.txt')
        self.assertEqual("y[None:None:-1] + x[None:None:-1]", content.strip())


if __name__ == '__main__':
    unittest.main()
