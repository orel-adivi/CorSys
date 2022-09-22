#
#   @file : Synthesizer.py
#   @date : 22 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast
import time

from src.synthesizer.SearchSpace import SearchSpace
from src.synthesizer.ProgramGenerator import ProgramGenerator


if __name__ == '__main__':
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


"""
slice
"""