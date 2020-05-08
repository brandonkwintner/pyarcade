from pyarcade.abstract_game import AbstractGame
from pyarcade.difficulties import Difficulty
from typing import Optional, List
import random


class Horseman(AbstractGame):
    """A class representing a Horseman game session
    """
    four_letter_words = ['four', 'beer', 'baby', 'ball', 'dark', 'data',
                         'deck', 'edge', 'firm', 'food', 'hear', 'hate',
                         'huge', 'idea', 'main', 'mass', 'moon', 'rice',
                         'rich', 'rule', 'said', 'sees', 'send', 'snow',
                         'shot', 'sick', 'tape', 'then', 'than', 'unit',
                         'user', 'view']
    six_letter_words = ['accept', 'access', 'across', 'button', 'buyers',
                        'butter', 'camera', 'charge', 'cheese', 'dining',
                        'direct', 'doctor', 'earned', 'eating', 'energy',
                        'fabric', 'failed', 'finger','health', 'handle',
                        'humans', 'laptop', 'leaves', 'layout', 'muscle',
                        'nation', 'normal']
    eight_letter_words = ['accident', 'accepted', 'assigned', 'bacteria',
                          'campaign', 'chemical', 'criminal', 'congress',
                          'fighting', 'findings', 'graphics', 'greatest',
                          'hardware', 'graduate', 'honestly', 'language',
                          'lifetime', 'millions', 'painting', 'personal',
                          'terrible', 'template']

    def __init__(self, difficulty: Optional[Difficulty] = Difficulty.NORMAL):
        """ A Horseman game session

            Game modes:
            Easy - 4 letter words
            Normal (default) - 6 letter words
            Hard - 8 letter words

            Args:
                difficulty: (Difficulty) The difficulty of the new game to be
                played

        """
        AbstractGame.__init__(self)

        self.num_guesses_left = 6
        self.difficulty = difficulty
        self.word = self.pick_word()
        self.current_word = ["_" for i in range(len(self.word))]
        self.game_over = False

    def pick_word(self) -> List[str]:
        """Chooses a word from the given list

        Returns: The chosen word

        """
        if self.difficulty == Difficulty.EASY:
            return list(random.choice(Horseman.four_letter_words))
        elif self.difficulty == Difficulty.NORMAL:
            return list(random.choice(Horseman.six_letter_words))
        else:
            return list(random.choice(Horseman.eight_letter_words))

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
            self.entire_history.append(("Player won", self.current_word))
            self.current_history.append(("Player won", self.current_word))
            return True
        elif self.game_over and not result:
            self.entire_history.append(("Player lost", self.word))
            self.current_history.append(("Player lost", self.word))
            return True
        else:
            return False

    def check_letter(self, guessed_letter: str) -> bool:
        """Checks if guess is in the word

        Args:
            guessed_letter (): User's guessed letter.

        Returns:
            True if guess is in word
        """
        letter_found = False

        for index in range(len(self.word)):
            if guessed_letter == self.word[index]:
                letter_found = True
                self.current_word[index] = self.word[index]

        if letter_found is False:
            self.num_guesses_left -= 1

            if self.num_guesses_left == 0:
                self.game_over = True

            return False

        if self.check_for_winner():
            self.game_over = True

        return True

    def check_for_winner(self) -> bool:
        """ Checks if word is filled out

        Returns: True if word is filled out

        """
        return "_" not in self.current_word

    def reset_game(self):
        """ Reset single game. (input reset)
        """
        super().reset_game()

        self.current_history = []
        self.num_guesses_left = 6
        self.word = self.pick_word()
        self.current_word = ["_" for i in range(len(self.word))]
        self.game_over = False

    def clear_game(self):
        """ Clears entire game. (input clear)
        """
        super().clear_game()
        self.reset_game()
        self.entire_history = []

    def get_last_turn(self):
        """ Gets the last turn/state of game (the amount of the word guessed).

        Returns:
            Meaningful state of the current game.
        """
        super().get_last_turn()

        return ''.join(self.current_word), self.num_guesses_left, ''.join(
            self.word)

    @staticmethod
    def get_regex_pattern() -> str:
        """ Gets validator for game.

        Returns:
            Regex string.
        """
        AbstractGame.get_regex_pattern()

        return r"^[a-zA-Zz]$"
