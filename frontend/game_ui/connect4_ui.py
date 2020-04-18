from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from game_ui.menu_options import Options
from game_ui.display_ui import Display
from typing import List


class Connect4UI:
    def __init__(self, window, scroll_idx, user):
        self.window = window
        # self.scroll_idx = scroll_idx
        self.scroll_idx = 1
        self.display = Display(self.window, self.scroll_idx, user)

    def connect_four_menu(self) -> str:
        menu = Options.GAME_STARTUP.value
        result = []

        while True:
            self.display.display_options(menu, ["Connect 4 Menu"])
            self.scroll_idx = self.display.scroll_options(menu,
                                                          ["Connect 4 Menu"])

            if menu[self.scroll_idx] == "New Game":
                result = self.play_connect_four()

            elif menu[self.scroll_idx] == "Instructions":
                result = []

            elif self.scroll_idx == len(menu) - 1:
                break

            self.display.scroll_idx = 1

        return result

    def play_connect_four(self) -> List[str]:
        option_list = Options.CONNECT_FOUR_OPTIONS.value
        input_system = InputSystem(Game.CONNECT4)
        games_won = 0

        while True:
            status = input_system.get_last_guess()
            game_info = ["Connect Four", status, str(games_won), input_system.get_round_info()]

            self.display.display_options(option_list, game_info)
            self.scroll_idx = self.display.scroll_options(option_list,
                                                          game_info)

            if option_list[self.scroll_idx] == "Enter Column":
                message = "Please enter a digits between 1 to 7"
                guess = self.display.user_input_window(message, "")

                if input_system.take_input(guess)[0]:
                    winner = input_system.get_last_guess()
                    option_list = Options.CONNECT_FOUR_NEW_GAME.value

                    if winner[1] == 'Player':
                        option_list[0] = 'Player X Wins!'
                        games_won += 1
                    elif winner[1] == 'NPC':
                        option_list[0] = 'Player O Wins!'

            elif option_list[self.scroll_idx] == "Reset" or \
                    option_list[self.scroll_idx] == "New Game":
                input_system.take_input("reset")
                option_list = Options.CONNECT_FOUR_OPTIONS.value

            elif option_list[self.scroll_idx] == "Clear":
                option_list = Options.CONNECT_FOUR_OPTIONS.value
                input_system.take_input("clear")

            elif self.scroll_idx == len(option_list) - 1:
                self.scroll_idx = 1
                break

        return option_list
