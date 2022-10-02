#
#   @file : RunAllBenchmarks.py
#   @date : 30 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import csv
import os
import subprocess
import time
from pathlib import Path

SYNTHESIZER = Path('Synthesizer.py')
BENCHMARKS = Path('benchmarks')


def run_test(grammar_path: Path, examples_path: Path, settings: dict[str, str]):
    cmd = ["python", str(SYNTHESIZER)]
    cmd += ["-io", str(examples_path)]
    cmd += ["-s", str(grammar_path)]
    if 'metric' in settings:
        cmd += ["-m", settings['metric']]
    if 'metric-parameter' in settings:
        cmd += ["-mp", settings['metric-parameter']]
    if 'tactic' in settings:
        cmd += ["-t", settings['tactic']]
    if 'tactic-parameter' in settings:
        cmd += ["-tp", settings['tactic-parameter']]
    if 'max-height' in settings:
        cmd += ["-mh", settings['max-height']]
    full_cmd = ' '.join(cmd)
    call = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    output, error = [output.decode().strip() for output in call.communicate()]
    return output, error


def main():
    run_counter, success_counter = 0, 0
    print('RUNNING ALL BENCHMARKS OF CorSys:')
    for benchmark in sorted([benchmark for benchmark
                             in next(os.walk(str(BENCHMARKS)))[1]
                             if 'benchmark' in benchmark],
                            key=lambda dirname: int(dirname.split('benchmark_')[1])):
        settings = {}
        grammar_path = Path(str(BENCHMARKS) + '/' + benchmark + '/Grammar.csv')
        with Path(str(BENCHMARKS) + '/' + benchmark + '/Settings.csv').open() as file:
            for row in csv.reader(file):
                settings[row[0]] = row[1]
        print('\n======================================================================')
        print(f'BENCHMARK: {benchmark}')
        print(f'DESCRIPTION: {settings["description"]}\n')
        print('Running tests:')
        for examples in sorted([examples for examples
                                in next(os.walk(str(BENCHMARKS) + '/' + benchmark))[2]
                                if 'Examples' in examples],
                               key=lambda filename: int(filename.split('Examples')[1].split('.')[0])):
            print('----------------------------------------------------------------------')
            run_counter += 1
            examples_path = Path(str(BENCHMARKS) + '/' + benchmark + '/' + examples)
            start_time = time.time()
            output, error = run_test(grammar_path=grammar_path, examples_path=examples_path, settings=settings)
            end_time = time.time()
            if output == settings[examples_path.stem] and not error:
                print(f'Ran {examples_path.stem} successfully (in {end_time - start_time} s):')
                print(output)
                success_counter += 1
            elif error:
                print(f'[ERROR] Ran {examples_path.stem} and got an error (in {end_time - start_time} s):')
                print(error)
            elif output != settings[examples_path.stem]:
                print(f'[NOT MATCH] Ran {examples_path.stem} and got a different output'
                      f' (in {end_time - start_time} s):')
                print(output)
                print(f'[EXPECTED: {settings[examples_path.stem]} ]')
            else:
                assert False
    print('\n======================================================================')
    print(f'{success_counter} tests out of {run_counter} tests were successful.')
    if run_counter == success_counter:
        print('ALL TESTS RAN SUCCESSFULLY.')
    else:
        print(f'FAILED IN {run_counter - success_counter} TESTS.')
    assert run_counter == success_counter


if __name__ == '__main__':
    main()
