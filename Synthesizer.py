#
#   @file : Synthesizer.py
#   @date : 22 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast
import pathlib
import time
import argparse

from src.io.SearchSpace import SearchSpace
from src.synthesizer.ProgramGenerator import ProgramGenerator


if __name__ == '__main__':
    cl_parser = argparse.ArgumentParser(description='CorSys - Synthesizing best-effort python expressions while'
                                                    'weighting the chance for mistakes in given user outputs.',
                                        epilog='For help with the synthesizer please read SUPPORT.md .',
                                        allow_abbrev=False)
    cl_parser.add_argument('-io', '--input-output', action='store', type=pathlib.Path, required=True,
                           help='the root for the input-output file', dest='input_output_file')
    cl_parser.add_argument('-s', '--search-space', action='store', type=pathlib.Path, required=True,
                           help='the root for the search space file', dest='search_space_file')
    cl_parser.add_argument('-m', '--metric', action='store', type=str, default='DefaultMetric',
                           help='the metric for the synthesizer', dest='metric')
    cl_parser.add_argument('-t', '--tactic', action='store', type=str, default='height',
                           choices=['height', 'time', 'best_by_height', 'top'],
                           help='the tactic for the synthesizer', dest='tactic')
    cl_parser.add_argument('-mh', '--max-height', action='store', type=int, default=5,
                           help='the max height for the synthesizer to search', dest='max_height')
    cl_parser.add_argument('-mt', '--max-time', action='store', type=int, default=60,
                           help='the time limit for the synthesizer to search', dest='max_time')
    cl_parser.add_argument('-r', '--result-number', action='store', type=int, default=5,
                           help='the number of results for the synthesizer to show', dest='result_number')
    arguments = cl_parser.parse_args()
    print(arguments)
    pass




    inputs = [{'x': 6, 'y': 1, 'z': 9}, {'x': 2, 'y': 3, 'z': 4}]
    outputs = list(map(lambda env: env['x'] + env['y'] + env['z'], inputs))
    search_space = SearchSpace.readGrammarFromFile('utils/grammars/IntegerGrammar.txt')
    generator = ProgramGenerator(search_space, 10)
    result = generator.findProgram(inputs, outputs)
    time.sleep(1)
    print(ast.unparse(result))
    print('')

    outputs = list(map(lambda env: [4, 3], inputs))
    search_space = SearchSpace.readGrammarFromFile('utils/grammars/ListGrammar.txt')
    generator = ProgramGenerator(search_space, 10)
    result = generator.findProgram(inputs, outputs)
    time.sleep(0.1)
    print(ast.unparse(result))
    print('')

