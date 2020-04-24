from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from game_ui.menu_options import Options
from game_ui.display_ui import Display
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
            self.scroll_idx = self.display.scroll_options(menu, ["Mastermind Menu"])

            if menu[self.scroll_idx] == "Easy Mode":
                result = self.play_mastermind()

            elif menu[self.scroll_idx] == "Instructions":
                result = []

            elif self.scroll_idx == len(menu) - 1:
                break

            self.display.scroll_idx = 1

        return result

    def play_mastermind(self) -> List[str]:
        input_system = InputSystem(Game.MASTERMIND)
        option_list = Options.MASTERMIND_OPTIONS.value

        while True:
            game = input_system.game_num
            status = input_system.get_last_guess()
            game_info = ["Mastermind", status, str(game)]

            self.display.display_options(option_list, game_info)
            self.scroll_idx = self.display.scroll_options(option_list, game_info)

            if option_list[self.scroll_idx] == "Take Guess":
                message = "Please enter 4 digits 0 to 9 inclusive"
                guess = self.display.user_input_window(message, "")

                if input_system.take_input(" ".join(guess))[0]:
                    option_list = Options.MASTERMIND_NEW_GAME.value

            elif option_list[self.scroll_idx] == "Reset" or \
                    option_list[self.scroll_idx] == "New Game":
                option_list = Options.MASTERMIND_OPTIONS.value
                input_system.take_input("reset")

            elif option_list[self.scroll_idx] == "Clear":
                option_list = Options.MASTERMIND_OPTIONS.value
                input_system.take_input("clear")

            elif self.scroll_idx == len(option_list) - 1:
                self.scroll_idx = 1
                break

        return option_list
