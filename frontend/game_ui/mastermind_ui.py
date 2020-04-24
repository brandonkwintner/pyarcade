from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from game_ui.menu_options import Options
from game_ui.display_ui import Display
from pyarcade.difficulties import Difficulty
from typing import List


class MastermindUI:
    def __init__(self, window, scroll_idx, user):
        self.window = window
        self.scroll_idx = scroll_idx
        self.display = Display(self.window, self.scroll_idx, user)

    def mastermind_menu(self) -> List[str]:
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

            elif self.scroll_idx == len(menu) - 1:
                break

            self.display.scroll_idx = 1

        return result

    def play_mastermind(self,width, mode=Difficulty.NORMAL) -> List[str]:
        input_system = InputSystem(Game.MASTERMIND, mode)
        option_list = Options.MASTERMIND_OPTIONS.value
        game_info = ["Mastermind", "", 0, ""]

        if mode == Difficulty.EASY:
            message = "Please enter 2 digits: 0 to 9 inclusive"
        elif mode == Difficulty.HARD:
            message = "Please enter 6 digits: 0 to 9 inclusive"
        else:
            message = "Please enter 4 digits: 0 to 9 inclusive"

        while True:
            game_info[1] = input_system.get_last_guess()
            game_info[2] = str(input_system.game_num)

            self.display.display_options(option_list, game_info)
            self.scroll_idx = self.display.scroll_options(option_list, game_info)

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

            elif self.scroll_idx == len(option_list) - 1:
                self.scroll_idx = 1
                break

        return option_list
