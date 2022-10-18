---
layout: default
---

[![Sanity Check - Build](https://github.com/orel-adivi/CorSys/actions/workflows/build.yml/badge.svg)](https://github.com/orel-adivi/CorSys/actions/workflows/build.yml)
[![Run all Benchmarks - Testing](https://github.com/orel-adivi/CorSys/actions/workflows/benchmarks.yml/badge.svg)](https://github.com/orel-adivi/CorSys/actions/workflows/benchmarks.yml)
[![Check Style (Flake8) - Style](https://github.com/orel-adivi/CorSys/actions/workflows/style.yml/badge.svg)](https://github.com/orel-adivi/CorSys/actions/workflows/style.yml)
[![Vulnerabilities Check (CodeQL) - Security](https://github.com/orel-adivi/CorSys/actions/workflows/vulnerabilities.yml/badge.svg)](https://github.com/orel-adivi/CorSys/actions/workflows/vulnerabilities.yml)
[![GitHub](https://img.shields.io/github/license/orel-adivi/CorSYs)](https://github.com/orel-adivi/CorSys/blob/main/LICENSE)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/orel-adivi/CorSys)](https://github.com/orel-adivi/CorSys/releases)
[![GitHub all releases](https://img.shields.io/github/downloads/orel-adivi/CorSys/total)](https://github.com/orel-adivi/CorSys/releases)
[![GitHub repo size](https://img.shields.io/github/repo-size/orel-adivi/CorSys)](https://github.com/orel-adivi/CorSys)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Forel-adivi.github.io%2FCorSys%2F)](https://orel-adivi.github.io/CorSys/)

## About the Project

"CorSys" is a demonstrative program synthesizer, which synthesizes best-effort Python expressions while
weighting the chance for mistakes in given user outputs, using various metrics for mistake probability
evaluation. CorSys enumerates all possible expressions using the given syntax, limited to a specified
syntax-tree height, using a bottom-up enumeration methodology and using Observational Equivalence for
pruning equivalent expressions under the given set of input-output examples. For each expression whose
outputs are not observationally equivalent to a previously seen expression, the specified metric grades
the distance between the actual outputs and the expected ones. Finally, the synthesizer is able to
return the best expression, under a criterion selected by the user. CorSys is using the Syntax-Guided
Synthesis (SyGuS) methodology, and is given small-step specifications to work with Programming by Examples (PBE).

This project is based on a [previous work](https://github.com/peleghila/bester) by Peleg and Polikarpova (2020).
This paper describes a technique for dealing efficiently with incorrect input-output specifications given by the
user. In the paper, it is suggested to use a distance metric for rewarding more-likely-to-be-correct programs,
specifically using Levenshtein distance. In this work, we generalize this concept of distance metric for various
kinds of user mistakes, focusing on arithmetical mistakes (for example, rounding values and off-by-one calculation
mistakes) and typing mistakes (for example, replacing similar-sounding letters and deleting a letter). Please read
the paper for more details about this technique:

> Peleg, Hila, and Polikarpova, Nadia. 2020. “<span class="nocase">Perfect
> Is the Enemy of Good: Best-Effort Program Synthesis</span>.” In *34th
> European Conference on Object-Oriented Programming (ECOOP 2020)*, edited
> by Robert Hirschfeld and Tobias Pape, 166:2:1–30. Leibniz International
> Proceedings in Informatics (LIPIcs). Dagstuhl, Germany: Schloss
> Dagstuhl–Leibniz-Zentrum für Informatik.
> <https://doi.org/10.4230/LIPIcs.ECOOP.2020.2>.

The work is submitted as the final project in the course "Software Synthesis and Automated Reasoning" (236347),
at Taub Faculty of Computer Science, Technion - Israel Institute of Technology. The project was written by
Orel Adivi `(orel.adivi [at] cs.technion.ac.il)` and Daniel Noor `(daniel.noor [at] cs.technion.ac.il)`,
and under the supervision of Matan Peled and assistant professor Shachar Itzhaky. The work was done in about
a month, from 19 September 2022 to 18 October 2022. The project is released under MIT licence.


## Usage

The synthesizer main file is [Synthesizer.py](https://github.com/orel-adivi/CorSys/blob/main/Synthesizer.py),
which uses code implemented in [src directory](https://github.com/orel-adivi/CorSys/tree/main/src). For running
the synthesizer, an installation of [CPython 3.9](https://www.python.org/downloads/release/python-3915/)
or [CPython 3.10](https://www.python.org/downloads/release/python-3108/) is required (the implementation is platform
independent, and was tested on Windows, macOS, and Linux).

The project uses NumPy, SciPy, and overrides Python libraries, which can be installed using Pip package installer: 

```bash
python -m pip install -r requirements.txt
```

Then, running the synthesizer with `--help` flag gives the list of the parameters to provide:

```bash
python Synthesizer.py --help
```

The following output is given:

```text
usage: Synthesizer.py [-h] -io INPUT_OUTPUT_FILE -s SEARCH_SPACE_FILE
                      [-m {DefaultMetric,NormalMetric,CalculationMetric,VectorMetric,HammingMetric,LevenshteinMetric,PermutationMetric,KeyboardMetric,HomophoneMetric}]
                      [-mp METRIC_PARAMETER]
                      [-t {match,accuracy,height,top,best_by_height,penalized_height,interrupt}]
                      [-tp TACTIC_PARAMETER] [-mh MAX_HEIGHT] [--statistics]

CorSys - Synthesizing best-effort python expressions while weighting the
chance for mistakes in given user outputs.

options:
  -h, --help            show this help message and exit
  -io INPUT_OUTPUT_FILE, --input-output INPUT_OUTPUT_FILE
                        the root for the input-output file
  -s SEARCH_SPACE_FILE, --search-space SEARCH_SPACE_FILE
                        the root for the search space file
  -m {DefaultMetric,NormalMetric,CalculationMetric,VectorMetric,HammingMetric,LevenshteinMetric,PermutationMetric,KeyboardMetric,HomophoneMetric}, --metric {DefaultMetric,NormalMetric,CalculationMetric,VectorMetric,HammingMetric,LevenshteinMetric,PermutationMetric,KeyboardMetric,HomophoneMetric}
                        the metric for the synthesizer (default =
                        'DefaultMetric')
  -mp METRIC_PARAMETER, --metric-parameter METRIC_PARAMETER
                        the parameter for the metric
  -t {match,accuracy,height,top,best_by_height,penalized_height,interrupt}, --tactic {match,accuracy,height,top,best_by_height,penalized_height,interrupt}
                        the tactic for the synthesizer (default = 'height')
  -tp TACTIC_PARAMETER, --tactic-parameter TACTIC_PARAMETER
                        the parameter for the tactic
  -mh MAX_HEIGHT, --max-height MAX_HEIGHT
                        the max height for the synthesizer to search (default
                        = 2)
  --statistics          whether to present statistics

For help with the synthesizer please read SUPPORT.md .
```

The `--help` flag (or `-h`) shows this message with the list of the parameters, the `--max-height` parameter (or `-mh`)
sets the maximal syntax-tree height to generate expressions, and `--statistics` flag shows statistics about the
synthesizer. The other flags are covered in the following sections.


### Inputs and Outputs

mention utils
todo

-io INPUT_OUTPUT_FILE, --input-output INPUT_OUTPUT_FILE
                        the root for the input-output file


### Search Space

mention utils
todo

-s SEARCH_SPACE_FILE, --search-space SEARCH_SPACE_FILE
                        the root for the search space file


### Metrics

todo

-m {DefaultMetric,NormalMetric,CalculationMetric,VectorMetric,HammingMetric,LevenshteinMetric,PermutationMetric,KeyboardMetric,HomophoneMetric}, --metric {DefaultMetric,NormalMetric,CalculationMetric,VectorMetric,HammingMetric,LevenshteinMetric,PermutationMetric,KeyboardMetric,HomophoneMetric}
                        the metric for the synthesizer (default =
                        'DefaultMetric')
  -mp METRIC_PARAMETER, --metric-parameter METRIC_PARAMETER
                        the parameter for the metric


### Tactics

The criterion of which expression to return is defined by the `--tactic` parameter (or `-t`). For several tactics,
an additional parameter, `--tactic-parameter` (or `-tp`), is also required. The following values are available for
the `--tactic` parameter:
- `match` - the first expression whose distance value is equal or less than the defined value is returned.
The `--tactic-parameter` defines the threshold distance for returning an expression, and should be between 0.0 to
the number of examples.
- `accuracy` - the first expression whose distance value, divided by the number of examples, is equal or less than the
defined value is returned. The `--tactic-parameter` defines the threshold distance, after normalization, for returning
an expression, and should be between 0.0 to 1.0.
- `height` - the best expression, among all possible expressions whose syntax-tree height is up the the defined, is
returned. Please note that the height threshold is defined by `--max-height` parameter, and  `--tactic-parameter` is
ignored.
- `top` - the best expressions, among all possible expressions whose syntax-tree height is up the the defined, are
returned, one in each line (in descending accuracy). The `--tactic-parameter` defines the number of expressions to
return.
- `best_by_height` - the best expressions, among all possible expressions whose syntax-tree height is up the the
defined, are returned, one in each line, so each line represent a different syntax-tree height limit. Please note
that the maximal syntax-tree height is defined by `--max-height` parameter, and  `--tactic-parameter` is ignored.
- `penalized_height` - the best expression, among all possible expressions whose syntax-tree height is up the the
defined, is returned. Each expression is penalized according to its syntax-tree height, so smaller expressions are
preferred. The `--tactic-parameter` defines the penalty for each addition of one for the syntax-tree height, and
should be between 0.0 to 1.0.
- `interrupt` - the best expression, till finishing searching all possible expressions whose syntax-tree height is
up the the defined or till keyboard interrupt `(ctrl + c)`, is returned. The `--tactic-parameter` is ignored.


## Benchmarks

In order to evaluate the performance of the synthesizer, we wrote a set of ten benchmarks, each having a single Grammar
file and five input-output pair files (total of 50 tests). Each of the benchmarks was built to demonstrate a different
ability of the synthesizer, focusing on its unique abilities of correcting incorrect input-output specifications. In
order to run the synthesizer with all the benchmarks, the following script can be executed:

```bash
python RunAllBenchmarks.py
```

It is also possible ro run specific benchmarks by mentioning them as command line arguments. The script runs the
synthesizer with each of the input-output pair files, with the relevant Grammar, and ensures the correctness of the
output the lack of other errors. The time that is required for each test is also printed. We ran the script and the
output we got is available in [results.txt](https://github.com/orel-adivi/CorSys/blob/main/benchmarks/results.txt).

The following benchmarks are available:
- **[benchmark_1](https://github.com/orel-adivi/CorSys/tree/main/benchmarks/benchmark_1)** -
this is a sanity benchmark, testing integer expression synthesis with DefaultMetric.
- **[benchmark_2](https://github.com/orel-adivi/CorSys/tree/main/benchmarks/benchmark_2)** -
this benchmark tests float expression synthesis with DefaultMetric.
- **[benchmark_3](https://github.com/orel-adivi/CorSys/tree/main/benchmarks/benchmark_3)** -
this benchmark tests string-related expression synthesis with DefaultMetric.
- **[benchmark_4](https://github.com/orel-adivi/CorSys/tree/main/benchmarks/benchmark_4)** -
this benchmark tests list-related expression synthesis with DefaultMetric.
- **[benchmark_5](https://github.com/orel-adivi/CorSys/tree/main/benchmarks/benchmark_5)** -
this is a numerical error benchmark, testing float expression synthesis with NormalMetric.
- **[benchmark_6](https://github.com/orel-adivi/CorSys/tree/main/benchmarks/benchmark_6)** -
this is a calculation error benchmark, testing integer expression synthesis with CalculationMetric.
- **[benchmark_7](https://github.com/orel-adivi/CorSys/tree/main/benchmarks/benchmark_7)** -
this is a typo benchmark, testing string expression synthesis with LevenshteinMetric.
- **[benchmark_8](https://github.com/orel-adivi/CorSys/tree/main/benchmarks/benchmark_8)** -
this is a typo benchmark, testing string expression synthesis with KeyboardMetric.
- **[benchmark_9](https://github.com/orel-adivi/CorSys/tree/main/benchmarks/benchmark_9)** -
this is a typo benchmark, testing string expression synthesis with HomophoneMetric.
- **[benchmark_10](https://github.com/orel-adivi/CorSys/tree/main/benchmarks/benchmark_10)** -
this is a list-element typo benchmark, testing list expression synthesis with HammingMetric.


## Project Engineering

### Design and Development

The project was designed with accordance to the object-oriented programming (OOP) principles. For security purposes,
later commits were signed cryptographically, security Github Actions were enabled, and a
[SECURITY.md](https://github.com/orel-adivi/CorSys/blob/main/SECURITY.md) file was written. For documentation, a
[website](https://orel-adivi.github.io/CorSys/) is available and a
[SUPPORT.md](https://github.com/orel-adivi/CorSys/blob/main/SUPPORT.md) file was written. The project was written using
PyCharm Professional and was managed using [GitHub](https://github.com/orel-adivi/CorSys).


### Continuous Integration

In order to ensure the correctness of commits sent to th GitHub server, a continuous integration pipeline was set.
These checks are run automatically for each pull request and each push. The following actions were set:
1) [Build](https://github.com/orel-adivi/CorSys/actions/workflows/build.yml) - basic tests are run with the updated
code, to ensure the lack of syntax errors.
2) [Benchmarks](https://github.com/orel-adivi/CorSys/actions/workflows/benchmarks.yml) - all the benchmarks are run
with the updated code, to ensure its correctness.
3) [Style check](https://github.com/orel-adivi/CorSys/actions/workflows/style.yml) - the coding style is automatically
checked using Flake8, to match the PEP8 coding standard.
4) [Vulnerabilities check](https://github.com/orel-adivi/CorSys/actions/workflows/vulnerabilities.yml) - the updated
code is check to ensure it does not contain any known vulnerability.
5) [Dependency review](https://github.com/orel-adivi/CorSys/actions/workflows/dependency-review.yml) - the dependencies
are reviewed to check for any security issue.
6) [Website](https://github.com/orel-adivi/CorSys/actions/workflows/website.yml) - the
[CorSys website](https://orel-adivi.github.io/CorSys/) is updated with the current information.
7) [Dependabot](https://github.com/orel-adivi/CorSys/blob/main/.github/dependabot.yml) - the dependency versions (in
[requirements.txt](https://github.com/orel-adivi/CorSys/blob/main/requirements.txt)) are updated regularly.

For the relevant actions, the checks were run in all the supported Python version (CPython 3.9 and CPython 3.10), and
on all supported operating systems - Windows (Windows Server 2022), macOS (macOS Big Sur 11), and Linux (Ubuntu 20.04).


### Suggestions for Future Research

next
small utils: program minimizer (counter example ?), game man vs. synthesizer
unittests
pypy
weighted metric
constant diff keyboard
combined metric
