from pyarcade.abstract_game import AbstractGame
from pyarcade.difficulties import Difficulty
from typing import Optional, List


class Horseman(AbstractGame):
    def __init__(self, difficulty: Optional[Difficulty] = Difficulty.NORMAL):
        if difficulty == Difficulty.EASY:
            self.word_length = 4
        elif difficulty == Difficulty.NORMAL:
            self.word_length = 6
        else:
            self.word_length = 8

        self.num_guesses_left = 6
        self.difficulty = difficulty
        self.word = self.pick_word()
        self.current_word = ["_" for i in range(len(self.word))]
        self.game_over = False

    @staticmethod
    def pick_word() -> List[str]:
        return ""

    def enter_user_turn(self, guess) -> bool:
        """ Checks if letter is in the word.

        Args:
            guess: User's guessed letter.

        Returns:
            result (bool): True if game is over, false otherwise.

        """
        super().enter_user_turn(guess)

        result = self.check_letter(guess)

        if self.game_over and result:
            self.entire_history.append("Player won", self.current_word)
            self.current_history.append("Player won", self.current_word)
            return True
        elif self.game_over and not result:
            self.entire_history.append("Player lost", self.word)
            self.current_history.append("Player lost", self.word)
            return True
        else:
            return False

    def check_letter(self, guessed_letter: str) -> bool:
        letter_found = False

        for letter in self.word:
            if guessed_letter == letter:
                letter_found = True
                self.current_word[self.word.index(letter)] = letter

        if letter_found is False:
            self.num_guesses_left -= 1

            if self.num_guesses_left == 0:
                self.game_over = True

            return False

        if self.check_for_winner():
            self.game_over = True

        return True

    def check_for_winner(self) -> bool:
        for letter in self.current_word:
            if letter == "_":
                return False

        return True

    def reset_game(self):
        """ Reset single game. (input reset)
        """
        super.reset_game()

        self.current_history = []
        self.word = self.pick_word()

    def clear_game(self):
        """ Clears entire game. (input clear)
        """
        super.clear_game()

        self.current_history = []
        self.entire_history = []
        self.word = self.pick_word()

    def get_last_turn(self):
        """ Gets the last turn/state of game (the amount of the word guessed).

        Returns:
            Meaningful state of the current game.
        """
        super.get_last_turn()

        return ''.join(self.current_word), self.game_over

    @staticmethod
    def get_regex_pattern() -> str:
        """ Gets validator for game.

        Returns:
            Regex string.
        """
        AbstractGame.get_regex_pattern()

        return r"^[a-zA-Zz]$"
