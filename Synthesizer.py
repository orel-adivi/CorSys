#
#   @file : Synthesizer.py
#   @date : 19 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast
import time

from src.synthesizer.SearchSpace import SearchSpace
from src.synthesizer.ProgramGenerator import ProgramGenerator


if __name__ == '__main__':
    inputs = [{'x': 6, 'y': 4, 'z': 5}, {'x': 2, 'y': 3, 'z': 4}]
    outputs = list(map(lambda env: env['x'] + env['y'] + env['z'], inputs))
    search_space = SearchSpace.readGrammarFromFile('utils/grammars/IntegerGrammar.txt')
    generator = ProgramGenerator(search_space, 10)
    result = generator.findProgram(inputs, outputs)
    time.sleep(1)
    print(ast.unparse(result))
    print('')

    outputs = list(map(lambda env: [7, 66, 101], inputs))
    search_space = SearchSpace.readGrammarFromFile('utils/grammars/ListGrammar.txt')
    generator = ProgramGenerator(search_space, 10)
    result = generator.findProgram(inputs, outputs)
    time.sleep(0.1)
    print(ast.unparse(result))
    print('')


"""
slice
"""