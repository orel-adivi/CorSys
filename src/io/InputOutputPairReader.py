#
#   @file : InputOutputPairReader.py
#   @date : 28 September 2022
#   @authors : Orel Adivi and Daniel Noor
#
import csv
from pathlib import Path

from src.io.InputOutputPairs import InputOutputPairs


class InputOutputPairReader(object):

    @staticmethod
    def readCSV(root: Path):
        with root.open() as file:
            file_content = list(csv.reader(file))
        variable_names = file_content[0]
        result = InputOutputPairs()
        for pair in file_content[1:]:
            inputs = {variable_names[i]: eval(value) for i, value in enumerate(pair[:-1])}
            output = eval(pair[-1])
            result.addPair(inputs=inputs, output=output)
        return result

    # todo - ready to use


if __name__ == "__main__":
    file1 = Path('..\\..\\utils\\examples\\SumExamples.csv')
    res = InputOutputPairReader.readCSV(file1)
    print(res.inputs)
    print(res.outputs)
