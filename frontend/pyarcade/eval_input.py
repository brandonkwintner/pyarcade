from enum import Enum


class Evaluation(Enum):
    """ Represents the evaluation of each digit for sequence guessing.

        INCORRECT - Nowhere in 4 the hidden sequence at all

        SOMEWHERE - Somewhere in the hidden sequence, but not in the location
        it was submitted

        CORRECT - Is in the hidden sequence at the location it was submitted.
    """

    INCORRECT = "Incorrect"
    SOMEWHERE = "Somewhere"
    CORRECT = "Correct"
