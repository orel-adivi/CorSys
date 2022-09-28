#
#   @file : InputOutputPairs.py
#   @date : 28 September 2022
#   @authors : Orel Adivi and Daniel Noor
#


class InputOutputPairs(object):

    def __init__(self):
        self._inputs = []
        self._outputs = []

    @property
    def inputs(self) -> list[dict]:
        return self._inputs

    @property
    def outputs(self) -> list[object]:
        return self._outputs

    def addPair(self, inputs: dict, output: object) -> None:
        self._inputs.append(inputs)
        self._outputs.append(output)
