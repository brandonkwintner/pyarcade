from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from game_ui.menu_options import Options
from game_ui.display_ui import Display
from pyarcade.difficulties import Difficulty
from pyarcade.connection import Connections
from typing import List


class MastermindUI:
    """
    UI for Mastermind.
    """

    def __init__(self, window, scroll_idx, user):
        self.window = window
        self.scroll_idx = scroll_idx
        self.user = user
        self.display = Display(self.window, self.scroll_idx, user)

    def mastermind_menu(self) -> List[str]:
        """
        Mastermind menu screen.
        Returns:
            List containing game information.
        """
        menu = Options.GAME_STARTUP_DIFFICULT.value
        result = []

        while True:
            self.display.display_options(menu, ["Mastermind Menu"])
            self.scroll_idx = self.display.scroll_options(menu,
                                                          ["Mastermind Menu"])

            if menu[self.scroll_idx] == "Normal Mode":
                result = self.play_mastermind(4)

            elif menu[self.scroll_idx] == "Easy Mode":
                result = self.play_mastermind(2, Difficulty.EASY)

            elif menu[self.scroll_idx] == "Hard Mode":
                result = self.play_mastermind(6, Difficulty.HARD)

            elif menu[self.scroll_idx] == "Leaderboard":
                self.mastermind_leaderboard()

            elif menu[self.scroll_idx] == "Instructions":
                self.mastermind_instruction()

            elif self.scroll_idx == len(menu) - 1:
                break

            self.display.scroll_idx = 1

        return result

    def play_mastermind(self, width, mode=Difficulty.NORMAL) -> List[str]:
        """
        Mastermind game screen.
        Args:
            width: Length of hidden sequence.
            mode: Game difficulty.

        Returns:
            List containing information about game played.
        """
        input_system = InputSystem(Game.MASTERMIND, mode)
        option_list = Options.MASTERMIND_OPTIONS.value
        game_info = ["Mastermind", "", 0, ""]

        game_num = Connections.get_num_played("mastermind",
                                              self.user["token"])["played"]

        if mode == Difficulty.EASY:
            message = "Please enter 2 digits: 0 to 9 inclusive"
        elif mode == Difficulty.HARD:
            message = "Please enter 6 digits: 0 to 9 inclusive"
        else:
            message = "Please enter 4 digits: 0 to 9 inclusive"

        while True:
            game_info[1] = input_system.get_last_guess()
            game_info[2] = str(game_num)

            self.display.display_options(option_list, game_info)
            self.scroll_idx = self.display.scroll_options(option_list,
                                                          game_info)

            if option_list[self.scroll_idx] == "Take Guess":
                guess = " ".join(self.display.user_input_window(message, ""))
                result = input_system.take_input(guess)

                if result[1]:
                    if not len(guess.replace(" ", "")) == width:
                        game_info[3] = "Incorrect Input: Try Again"
                        continue

                    game_info[3] = ""

                    if result[0]:
                        option_list = Options.MASTERMIND_NEW_GAME.value
                        game_num += 1
                        Connections.update_num_wins("mastermind", True,
                                                    self.user["token"])

                else:
                    game_info[3] = "Incorrect Input: Try Again"

            elif option_list[self.scroll_idx] == "Reset" or \
                    option_list[self.scroll_idx] == "New Game":
                option_list = Options.MASTERMIND_OPTIONS.value
                game_info[3] = ""
                input_system.take_input("reset")

            elif option_list[self.scroll_idx] == "Clear":
                option_list = Options.MASTERMIND_OPTIONS.value
                game_info[3] = ""
                input_system.take_input("clear")
                Connections.reset_game_stat("mastermind", self.user["token"])
                game_num = 0

            elif self.scroll_idx == len(option_list) - 1:
                self.scroll_idx = 1
                break

        return option_list

    def mastermind_instruction(self):
        """Instructions to play Mastermind
        """

        goal = "Try to guess the mystery sequence"

        rules = "There are 3 modes: Easy (2 number)," \
                " Normal (4 number), and Hard (6 number) \n" \
                "The player enters a guess sequence. \n" \
                "The sequence is evaluated: \n" \
                "Correct (In the right position) \n" \
                "Somewhere (In sequence, but in wrong location) \n" \
                "Incorrect (Not in sequence)"

        instruct = "Take Guess: Enter the guess sequence" \
                   "New Game: Play another round \n" \
                   "Reset: Restart the round \n" \
                   "Clear: Clear all game history \n" \
                   "Back: Goes back to game start menu"

        self.display.display_instruction(goal, rules, instruct)

    def mastermind_leaderboard(self):
        board = Connections.get_leaderboard("mastermind", self.user["token"])
        self.display.display_leaderboard("Mastermind", board)
