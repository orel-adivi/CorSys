#
#   @file : Synthesizer.py
#   @date : 19 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast

from src.synthesizer.SearchSpace import SearchSpace
from src.synthesizer.ProgramGenerator import ProgramGenerator


if __name__ == '__main__':
    inputs = [{'x': 9, 'y': 6, 'z': 3}, {'x': 2, 'y': 3, 'z': 4}]
    outputs = list(map(lambda env: 4, inputs))
    search_space = SearchSpace.readGrammarFromFile('test/grammars/IntegerGrammar.txt')
    generator = ProgramGenerator(search_space, 10)
    result = generator.findProgram(inputs, outputs)
    print(ast.unparse(result))
