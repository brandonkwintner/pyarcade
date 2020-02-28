# PyArcade

## Assignment 4 Approximate Work Distribution

1. Andy Zhang: 50%
    1. Made main menu and game-specific menus.
    2. Assisted with game integration.
    3. Made and refactored existing tests for UI and other games.
    
2. Nam Quach: 50%
    1. Applied use of abstract factory design pattern.
    2. Integration with Andy's blackjack game.
    3. Assisted with game design.

## Design Pattern
The **Abstract Factory** design pattern was chosen because it felt like a natural extension of pyarcade.
To elaborate, our idea for pyarcade is that it is essentially made up of general "games".
Of course each game will have its own functionality but most pyarcade games definitely share common functionality.
For instance, starting a new game, resetting and clearing history, taking a user's input, getting the state of the game, etc.
Using this fact, making the specific games (i.e., mastermind, connect4, blackjack) conform/follow the abstract game class made it much easier to use the game code elsewhere.
For example, in the input system, after creating a desired game, since the methods were the same, there was no need to differentiate calling conventions (e.g., method names).
In our opinion, this made the code more merge-able, maintainable, and manageable.
Firstly, since we both had similar ideas of how the games worked (e.g., taking input), all we needed to do was made sure the game to be merged inherited from the abstract class and then refactored and rename its method to match the abstract base class' method name.
If there were any bugs to fix, it would likely happen at the specific game level rather than the caller of the method (i.e., input system) as we are only using the abstract methods rather than calling specific methods relating to the game in almost all cases.
Also, if we were to add another game, all that the new game needs to do is to adhere to the abstract class and along with very minor changes to the input system, it would be up and running in our pyarcade within a few lines of extra code.

You can see the definition of the class in **pyarcade/abstract_game.py**

Minified example for future game implementation:

```Python
class AbstractGame(metaclass=ABCMeta):
     @abstractmethod
    def enter_user_turn(self, guess) -> bool:
        pass

class OurGame(AbstractGame):
    def enter_user_turn(self, col: int) -> bool:
        # ... code omitted
        return win_move

class SomeNewGame(AbstractGame):
    def custom_input_stuff(self, in: str, misc_opts: List[str]) -> bool:
        # ... code omitted
        return win_move

    def enter_user_turn(self, in: str) -> bool:
        # quick conformance by wrapping needed method with custom one
        return self.custom_input_stuff(in, ["a", "b", "c"])
```
