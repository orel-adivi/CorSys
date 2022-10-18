# CorSys

[![Sanity Check - Build](https://github.com/orel-adivi/CorSys/actions/workflows/build.yml/badge.svg)](https://github.com/orel-adivi/CorSys/actions/workflows/build.yml)
[![Run all Benchmarks - Testing](https://github.com/orel-adivi/CorSys/actions/workflows/benchmarks.yml/badge.svg)](https://github.com/orel-adivi/CorSys/actions/workflows/benchmarks.yml)
[![Check Style (Flake8) - Style](https://github.com/orel-adivi/CorSys/actions/workflows/style.yml/badge.svg)](https://github.com/orel-adivi/CorSys/actions/workflows/style.yml)
[![Vulnerabilities Check (CodeQL) - Security](https://github.com/orel-adivi/CorSys/actions/workflows/vulnerabilities.yml/badge.svg)](https://github.com/orel-adivi/CorSys/actions/workflows/vulnerabilities.yml)
[![GitHub](https://img.shields.io/github/license/orel-adivi/CorSYs)](https://github.com/orel-adivi/CorSys/blob/main/LICENSE)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/orel-adivi/CorSys)](https://github.com/orel-adivi/CorSys/releases)
[![GitHub all releases](https://img.shields.io/github/downloads/orel-adivi/CorSys/total)](https://github.com/orel-adivi/CorSys/releases)
[![GitHub repo size](https://img.shields.io/github/repo-size/orel-adivi/CorSys)](https://github.com/orel-adivi/CorSys)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Forel-adivi.github.io%2FCorSys%2F)](https://orel-adivi.github.io/CorSys/)

![logo](/docs/logo.jpg)

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
independent, and was tested on Windows, MacOS, and Linux).

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

The `--help` flag shows this message with the list of the parameters, the `--max-height` sets the maximal syntax-tree
height to generate expressions, and `--statistics` shows statistics about the synthesizer. The other flags are covered
in the following sections.

### Inputs and Outputs

mention utils
todo

### Search Space

mention utils
todo

### Metrics

todo

### Tactics

todo

## Benchmarks

todo

(1) sanity, default + - * //
(2) floats, default
(4) strings, default
(3) lists, default (+ optionally list comprehension)
(5) floats, NormalMetric - numerical errors
(6) integers, CalculationMetric - calculation mistakes
(7) strings, LevenshteinMetric - typos
(8) strings, KeyboardMetric - typos
(9) strings, HomophoneMetric - typos
(10) lists, WeightedMetric(VectorMetric - correlation? + HammingMetric) - mistakes in lists

## Project Engineering

### Design and Development

website & support files
security
design

### Continuous Integration
ci

### Suggestions for Future Research

next
small utils: program minimizer (counter example ?), game man vs. synthesizer
unittests
pypy
weighted metric
constant diff keyboard
combined metric
