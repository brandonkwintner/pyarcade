# PyArcade -- The Back End Test Suite

# Refactoring Explanation
1. Comments
    - I had some comments in some functions which were from the project description.
    Even though these comments describe the way the code is supposed to run, they were not needed as I believe that the code itself was readable enough.
    For instance, a chunk of comments I removed was describe the specifications for checking a Mastermind's guess list.
    I believe that the if conditionals are simple and self explanatory such that another programmer could easily figure out the structure without needing the specifications.
    In this case, this techinque of refactor was simply following the rule (from the comments part of the reading) of using comments to explain why or a complex algorithm instead of just documenting every step.

2. Inappropriate Intimacy
    - In the init for the InputSystem, I originally had it create an instance of Mastermind and also called Mastermind's generate_sequence function.
    I decided that generating the sequence should not be the responsibility of a class who uses the Mastermind game.
    So I moved the sequence generating responsibility to inside the init of the Mastermind class and subsequently removed it from the InputSystem's init.
    In this case, the closest refactoring technique was hide delegate.
    Since by moving the method inside the init, clients don't need to have the burden of generating sequences any time a new game session starts.

3. Long Method
    - In Mastermind's checking guess function, there was a chunk of code which evaluated the user's guess list.
    I felt that it would be more clear to move that chunk into it's own (check_guess) function.
    This way, the responsibility of the checking function would just be appending the history and checking if the guess was correct.
    In this case, the refactoring technique used was extract method.
    The main benefit of this would be more readable code since another programmer that was looking at the code would have little idea why that evaluation chunk would be there in just checking a guess was correct or not.

4. Duplicate Code
    - When writing the merging code for the two games (Connect4 and Mastermind), I had originally made two take input functions in the InputSystem.
    Those two functions would then call the respective class' guess parsing method.
    When looking to refactor, I noticed that the code for these two functions were essentially the same.
    The only difference in these two functions were about how they supplied the guess argument to their respective classes.
    To fix this, I combined the logic of the two which where similar and, where they differed, I modified and passed in the guess.
    The refactoring technique used here was consolidating duplicate conditional fragments with an aspect of extract method.
    For instance, since the difference was branching on an if statement, I did the necessary computations inside the branches and called the desired method afterward.

# Software Requirements
These are the following requirements for your implementation of PyArcade.

## Input System
NOTE: Requirements to STORE something does **not** mean it needs to be persistent across restarts of the system.

1. The *input_system* **MUST** ignore all inputs that do not have meaningful functionality for *Mastermind*.
2. The *input_system* **MUST** parse a string of integers of the appropriate size into an input that *Mastermind* can use.
3. The *input_system* **MUST** reset a game of *Mastermind* to the starting state if the string "reset" is provided.
4. The *input_system* **MUST** clear the game history of *Mastermind* if the string "clear" is provided.

## Mastermind (Cows and Bulls)
1. *Mastermind* **MUST** generate a random hidden sequence of 4 numbers from 0 to 9 (inclusive). 
2. *Mastermind* **MUST** accept as input from the user a guessed sequence, 4 numbers from 0 to 9 (inclusive).
3. *Mastermind* **MUST** output an *evaluation.* This includes for each digit in the guessed sequence, whether that digit is:
    1. Nowhere in the hidden sequence at all 
    2. Somewhere in the hidden sequence, but not in the location it was submitted
    3. Is in the hidden sequence at the location it was submitted. 

4. *Mastermind* **MUST** store history of all of the guessed sequences and the evaluation for the current session.
5. *Mastermind* **MUST** store the entire history once the current guessed sequence matches the hidden sequence exactly.

## Testing Requirements
For this project, you must have > 97% code-coverage using your test-suite. 
To test the coverage of your unit-tests, use [pytest-cov](https://pypi.org/project/pytest-cov/).
 
