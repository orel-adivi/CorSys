#
#   @file : BestEffortProgramGenerator.py
#   @date : 16 October 2022
#   @authors : Orel Adivi and Daniel Noor
#
from src.synthesizer.ProgramGenerator import ProgramGenerator
from src.objects.Metric import Metric
from src.metrics.DefaultMetric import DefaultMetric


class BestEffortProgramGenerator(ProgramGenerator):
    """
    This class implements the best effort program generator, which finds a program that is a "close enough" match to the
    input-output examples according to a chosen metric.

    Public methods:
        - current_height - Checks the current height of programs being generated
        - program_counter - Checks how many programs have been generated
        - enumerate - Generates programs contained in the generator's search space
        - findProgram - Finds a program precisely matching all the given input-output examples
        - findBestEffortMatchProgram - Finds a program matching the given input-output examples while allowing a limited
          number of mistakes
        - findBestEffortAccuracyProgram - Finds a program matching the given input-output examples while allowing a
          limited error rate
        - findBestEffortByHeightProgram - Finds a program best matching the given input-output examples up to the
          maximal program search height
        - findBestEffortPrograms - Finds a chosen number of programs best matching the given input-output examples
        - findBestEffortByHeightPrograms - For each search height finds the program best matching the given input-output
          examples
       -  findBestEffortPrioritizingHeightProgram - Finds a program best matching the given input-output examples while
          prioritizing smaller heights
        - findBestEffortUntilInterruptProgram - Searches a program best matching the given input-output examples until
          receiving a keyboard interrupt
    """

    def __init__(self, search_space: list[list], max_height: int) -> None:
        """
        Initialize a BestEffortProgramGenerator object.

        :param search_space: The search space to be used by the generator.
        :param max_height: Maximal height of generated programs.
        """
        super().__init__(search_space=search_space, max_height=max_height)

    @staticmethod
    def __get_distance(actual: list, expected: list, metric: Metric):
        """
        Compute the total distance between a program's results and the expected outputs, according to a given metric.

        :param actual: List of a program's results
        :param expected: List of expected outputs
        :param metric: Chosen metric
        :return: Sum of distances between each result to and the expected output
        """
        res = [metric.distance(actual=actual_example, expected=expected_example)
               for actual_example, expected_example in zip(actual, expected)]
        return sum(res)

    def findBestEffortMatchProgram(self, assignments: list[dict], evaluations: list, error_sum: int,
                                   metric: Metric = DefaultMetric()):
        """
        Find a program whose results given the input examples have a distance of at most error_sum to the output
        examples according to the chosen metric.

        :param assignments: Input examples (variables and their assigned values).
        :param evaluations: Output examples.
        :param error_sum: Maximal allowed distance between the program's results and the expected outputs.
        :param metric: Chosen metric.
        :return: The first matching program.
        """
        for program in self.enumerate(assignments=assignments):
            if BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                         expected=evaluations,
                                                         metric=metric) <= error_sum:
                return program

    def findBestEffortAccuracyProgram(self, assignments: list[dict], evaluations: list, error_rate: float,
                                      metric: Metric = DefaultMetric()):
        """
        Find a program which has an error rate of at most error_rate on the input-output examples, according to the
        chosen metric.

        :param assignments: Input examples (variables and their assigned values).
        :param evaluations: Output examples.
        :param error_rate: Maximal allowed error_rate of the program.
        :param metric: Chosen metric.
        :return: The first matching program.
        """
        for program in self.enumerate(assignments=assignments):
            if BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                         expected=evaluations,
                                                         metric=metric) <= error_rate * len(evaluations):
                return program

    def findBestEffortByHeightProgram(self, assignments: list[dict], evaluations: list,
                                      metric: Metric = DefaultMetric()):
        """
        Find the program which has the smallest distance between the results on the given input and the outputs. Only
        searches programs up to the maximal search height of the generator object.

        :param assignments: Input examples (variables and their assigned values).
        :param evaluations: Output examples.
        :param metric: Chosen metric.
        :return: The best program (the least distance between results and given outputs).
        """
        best_program = None
        best_score = len(evaluations) + 1
        for program in self.enumerate(assignments=assignments):
            curr_score = BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                                   expected=evaluations,
                                                                   metric=metric)
            if curr_score < best_score:
                best_program = program
                best_score = curr_score
        return best_program

    def findBestEffortPrograms(self, assignments: list[dict], evaluations: list, programs: int = 5,
                               metric: Metric = DefaultMetric()):
        """
        Find a chosen number of programs which have the smallest distances between the results on the given input and
        the outputs.

        :param assignments: Input examples (variables and their assigned values).
        :param evaluations: Output examples.
        :param programs: Maximal number of programs to return.
        :param metric: Chosen metric.
        :return: A list of the best programs (the least distance between results and given outputs).
        """
        best_programs = []
        for program in self.enumerate(assignments=assignments):
            curr_score = BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                                   expected=evaluations,
                                                                   metric=metric)
            if len(best_programs) < programs or best_programs[-1][1] > curr_score:
                best_programs.append((program, curr_score))
                best_programs = sorted(best_programs, key=lambda prog: prog[1])[:programs]
        return [program[0] for program in best_programs]

    def findBestEffortByHeightPrograms(self, assignments: list[dict], evaluations: list,
                                       metric: Metric = DefaultMetric()):
        """
        For each possible height in the search space, find the program of said height which has the smallest distance
        between the results on the given input and the outputs.

        :param assignments: Input examples (variables and their assigned values).
        :param evaluations: Output examples.
        :param metric: Chosen metric.
        :return: A list containing the best program for each height (the least distance between results and given
        outputs).
        """
        best_programs = [None]
        best_scores = [len(evaluations) + 1]
        for program in self.enumerate(assignments=assignments):
            if len(best_programs) < self._current_height + 1:
                best_programs += [None] * ((self._current_height + 1) - len(best_programs))
                best_scores = [len(evaluations) + 1] * ((self._current_height + 1) - len(best_scores))
            curr_score = BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                                   expected=evaluations,
                                                                   metric=metric)
            if curr_score < best_scores[-1]:
                best_programs[-1] = program
                best_scores[-1] = curr_score
        return best_programs

    def findBestEffortPrioritizingHeightProgram(self, assignments: list[dict], evaluations: list, penalty: float = 0.75,
                                                metric: Metric = DefaultMetric()):
        """
        Find the program which has the smallest distance between the results on the given input and the outputs, while
        taking height into account. A distance "penalty" is given to each program based on its height, meaning a program
        with a smaller height will be prioritized.

        :param assignments: Input examples (variables and their assigned values).
        :param evaluations: Output examples.
        :param penalty: height penalty.
        :param metric: Chosen metric.
        :return: The best program (the least distance between results and given outputs after penalty).
        """
        best_program = None
        best_score = (len(evaluations) + 1) * (penalty ** self._max_height)
        for program in self.enumerate(assignments=assignments):
            curr_score = BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                                   expected=evaluations,
                                                                   metric=metric)
            curr_score *= penalty ** self._current_height
            if curr_score < best_score:
                best_program = program
                best_score = curr_score
        return best_program

    def findBestEffortUntilInterruptProgram(self, assignments: list[dict], evaluations: list,
                                            metric: Metric = DefaultMetric()):
        """
        Search the program which has the smallest distance between the results on the given input and the outputs,
        upon a keyboard interrupt returns the best program found thus far.

        :param assignments: Input examples (variables and their assigned values).
        :param evaluations: Output examples.
        :param metric: Chosen metric.
        :return: The best program found until interrupt (least distance between results and given outputs).
        """
        best_program = None
        best_score = len(evaluations) + 1
        try:
            for program in self.enumerate(assignments=assignments):
                curr_score = BestEffortProgramGenerator.__get_distance(actual=program.results,
                                                                       expected=evaluations,
                                                                       metric=metric)
                if curr_score < best_score:
                    best_program = program
                    best_score = curr_score
        except KeyboardInterrupt:
            pass
        return best_program
