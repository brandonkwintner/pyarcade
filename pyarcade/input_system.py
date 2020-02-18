from typing import Tuple, List, Union
from pyarcade.mastermind import Mastermind
from pyarcade.game_option import Game
from pyarcade.connect4 import Connect4
import re


class InputSystem:
    """ Represents input system for validation and game usage.
        And executes commands on user input.

    """
    def __init__(self, game: Game = Game.MASTERMIND):
        """ Input System session.

            Args:
                game (Game enum): Which game to play

        """
        # other parameters starts mastermind game by default
        if game == Game.CONNECT4:
            self.game = Connect4()
        else:
            self.game = Mastermind()

        self.round = 1
        self.game_num = 1

    def take_input(self, cmd: str) -> Tuple[bool, bool]:
        """ Takes in a user's input and interacts with mastermind
        accordingly.

        Args:
            cmd (string): user's command.

        Returns:
            A 2-tuple boolean representing (win, valid_cmd).

            win (bool): True iff correct sequence was guessed.
            valid_cmd (bool): True iff a valid cmd was inputted.

        """

        valid_cmd = True
        win = False

        if cmd == "reset":
            self.reset()
        elif cmd == "clear":
            self.clear()
        elif self.is_valid_input_for_game(cmd):
            # turns the string guess into an int list
            guess = [int(num) for num in cmd.split()]

            '''
            if isinstance(self.game, Connect4):
                correct_guess = self.make_guess_for_connect4(guess)
            else:
                correct_guess = self.make_guess_for_mastermind(guess)
            '''
            correct_guess = self.make_guess_for_game(guess)

            if correct_guess:
                self.round = 1
                self.game_num += 1
            else:
                self.round += 1

            win = correct_guess
        else:
            valid_cmd = False

        return win, valid_cmd

    def make_guess_for_game(self, guess: List[int]) -> bool:
        """ Make a guess based on current game.

        Args:
            guess: (List[int]) user's guess list.

        Returns:
            True if correct according to the game, False otherwise.

        """

        if len(guess) < 1:
            return False

        if isinstance(self.game, Connect4):
            if not isinstance(guess[0], int):
                return False

            # board index from 0, but QOL for players start at 1
            proper_guess = guess[0] - 1
        else:
            proper_guess = guess

        return self.game.enter_user_turn(proper_guess)

    def reset(self):
        """ Resets the current game to starting state.
        """

        self.round = 1
        self.game.reset_game()

    def clear(self):
        """ Clear the all game history.
        """

        self.round = 1
        self.game_num = 1
        self.game.clear_game()

    def get_last_guess(self) -> Union[List[Tuple[int, str]], List[List[str]]]:
        """ Retrieves the player's last move/guess.

        Returns:
            List[Tuple[int, str]]: The evaluation of last guess (mastermind).
            List[List[str]]: Board state of last move (connect4).

        """

        return self.game.get_last_turn()

    def is_valid_input_for_game(self, cmd: str) -> bool:
        """ Determines if cmd is valid for the current game instance.

            Args:
                cmd (str): User's input.

            Returns:
                True if valid for current game.
        """

        if isinstance(self.game, Connect4):
            # matches only input with 1 number between [1-max cols] on board
            re_exp = r"^\s*[1-{}]\s*$".format(Connect4.MAX_COLS)
        else:
            # matches only input with 4 numbers separated by whitespace
            re_exp = r"^\s*[0-9]\s+[0-9]\s+[0-9]\s+[0-9]\s*$"

        return True if re.match(re_exp, cmd) else False

    def get_round_info(self) -> str:
        """ Gets the round information.
        If game is Mastermind, return round number
        If game is Connect4, return the current player's turn

            Returns:
                round_info (str)
        """

        if isinstance(self.game, Connect4):
            return f"Player {self.game.get_turn().value}:"
        else:
            return f"Round #{self.round}:"
