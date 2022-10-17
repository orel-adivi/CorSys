#
#   @file : InputOutputPairs.py
#   @date : 18 October 2022
#   @authors : Orel Adivi and Daniel Noor
#


class InputOutputPairs(object):
    """
    This class implements objects containing input-output examples for the synthesizer.

    Public methods:
        - __init__ - Create a new InputOutputPairs object.
        - inputs - Return the input examples contained within the object.
        - outputs - Add input-output examples to the object.
        - addPair - Add input-output examples to the object.
    """

    def __init__(self) -> None:
        """
        Create a new InputOutputPairs object.
        """
        self._inputs = []
        self._outputs = []

    @property
    def inputs(self) -> list[dict]:
        """
        Return the input examples contained within the object.

        :return: List of input examples (assignments to variables).
        """
        return self._inputs

    @property
    def outputs(self) -> list[object]:
        """
        Return the output examples contained within the object.

        :return: List of output examples (values).
        """
        return self._outputs

    def addPair(self, inputs: dict, output: object) -> None:
        """
        Add input-output examples to the object.

        :param inputs: Input example to add.
        :param output: Output example to add.
        :return: None.
        """
        self._inputs.append(inputs)
        self._outputs.append(output)
