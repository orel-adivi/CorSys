#
#   @file : Synthesizer.py
#   @date : 28 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import ast
import pathlib
import argparse
from functools import partial

from src.io.InputOutputPairReader import InputOutputPairReader
from src.io.SearchSpaceReader import SearchSpaceReader

from src.metrics.Metric import Metric
from src.metrics.DefaultMetric import DefaultMetric
from src.metrics.NormalMetric import NormalMetric
from src.metrics.CalculationMetric import CalculationMetric
from src.metrics.VectorMetric import VectorMetric
from src.metrics.HammingMetric import HammingMetric
from src.metrics.LevenshteinMetric import LevenshteinMetric
from src.metrics.PermutationMetric import PermutationMetric
from src.metrics.KeyboardMetric import KeyboardMetric
from src.metrics.HomophoneMetric import HomophoneMetric
# from src.metrics.CombinedMetric import CombinedMetric
# from src.metrics.WeightedMetric import WeightedMetric

from src.synthesizer.BestEffortProgramGenerator import BestEffortProgramGenerator


def get_metric(metric_name: str, metric_parameter: str) -> Metric:
    metrics = {
        'DefaultMetric': lambda: DefaultMetric(),
        'NormalMetric': lambda: NormalMetric(),     # todo support change std
        'CalculationMetric': lambda: CalculationMetric(),
        'VectorMetric': lambda: VectorMetric(dist_func=metric_parameter),
        'HammingMetric': lambda: HammingMetric(),
        'LevenshteinMetric': lambda: LevenshteinMetric(solve_recursively=eval(metric_parameter)),
        'PermutationMetric': lambda: PermutationMetric(),
        'KeyboardMetric': lambda: KeyboardMetric(),
        'HomophoneMetric': lambda: HomophoneMetric()
        # 'CombinedMetric': lambda: CombinedMetric()
        # 'WeightedMetric': lambda: WeightedMetric()
    }
    return metrics[metric_name]()


def main() -> None:
    cl_parser = argparse.ArgumentParser(description='CorSys - Synthesizing best-effort python expressions while'
                                                    'weighting the chance for mistakes in given user outputs.',
                                        epilog='For help with the synthesizer please read SUPPORT.md .',
                                        allow_abbrev=False)
    cl_parser.add_argument('-io', '--input-output', action='store', type=pathlib.Path, required=True,
                           help='the root for the input-output file', dest='input_output_file')
    cl_parser.add_argument('-s', '--search-space', action='store', type=pathlib.Path, required=True,
                           help='the root for the search space file', dest='search_space_file')
    cl_parser.add_argument('-m', '--metric', action='store', type=str, default='DefaultMetric',
                           choices=['DefaultMetric', 'NormalMetric', 'CalculationMetric', 'VectorMetric',
                                    'HammingMetric', 'LevenshteinMetric', 'PermutationMetric', 'KeyboardMetric',
                                    'HomophoneMetric'],
                           # 'CombinedMetric', 'WeightedMetric'
                           help='the metric for the synthesizer (default = \'DefaultMetric\')', dest='metric')
    cl_parser.add_argument('-mp', '--metric-parameter', action='store', type=str, default='',
                           help='the parameter for the metric', dest='metric_parameter')
    cl_parser.add_argument('-t', '--tactic', action='store', type=str, default='height',
                           choices=['match', 'accuracy', 'height', 'top', 'best_by_height', 'penalized_height',
                                    'interrupt'],
                           help='the tactic for the synthesizer (default = \'height\')', dest='tactic')
    cl_parser.add_argument('-tp', '--tactic-parameter', action='store', type=str, default='',
                           help='the parameter for the tactic', dest='tactic_parameter')
    cl_parser.add_argument('-mh', '--max-height', action='store', type=int, default=5,
                           help='the max height for the synthesizer to search (default = 5)', dest='max_height')
    arguments = cl_parser.parse_args()

    input_output_pairs = InputOutputPairReader.readCSV(arguments.input_output_file)
    inputs = input_output_pairs.inputs
    outputs = input_output_pairs.outputs
    search_space = SearchSpaceReader.readCSV(arguments.search_space_file).symbols
    metric = get_metric(arguments.metric, arguments.metric_parameter)
    generator = BestEffortProgramGenerator(search_space, arguments.max_height)

    if arguments.tactic == 'match':
        generation_function = partial(generator.findBestEffortMatchProgram,
                                      error_sum=eval(arguments.tactic_parameter))
    elif arguments.tactic == 'accuracy':
        generation_function = partial(generator.findBestEffortAccuracyProgram,
                                      error_rate=eval(arguments.tactic_parameter))
    elif arguments.tactic == 'height':
        generation_function = partial(generator.findBestEffortByHeightProgram)
    elif arguments.tactic == 'top':
        generation_function = partial(generator.findBestEffortPrograms,
                                      programs=eval(arguments.tactic_parameter))
    elif arguments.tactic == 'best_by_height':
        generation_function = partial(generator.findBestEffortByHeightPrograms)
    elif arguments.tactic == 'penalized_height':
        generation_function = partial(generator.findBestEffortPrioritizingHeightProgram,
                                      penalty=eval(arguments.tactic_parameter))
    elif arguments.tactic == 'interrupt':
        generation_function = partial(generator.findBestEffortUntilInterruptProgram)
    else:
        return

    result = generation_function(inputs, outputs, metric=metric)
    if not isinstance(result, list):
        result = [result]
    for program in result:
        print(ast.unparse(program))


if __name__ == '__main__':
    main()
