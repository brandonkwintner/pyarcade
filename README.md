# PyArcade

## Assignment 4 Approximate Work Distribution

1. John Doe: 60% effort
    1. Finished integration with John Doe 2's game.
    2. Made main menu and game-specific menus.
    
2. John Doe 2: 40%
    1. Applied use of Adapter pattern.
    2. Assisted with game design.

## Design Pattern
We chose to use the **Adapter pattern** because...

You can see where we used it in **pyarcade/input_system.py line 100.**

As a minified example: 

```Python
class TheirGame:

class MyGame:

class MyGameAdapter(MyGame):
    def __init__(self, their_game: TheirGame):
        pass

their_game = MyGameAdapter(TheirGame)
```