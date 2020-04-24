from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from game_ui.menu_options import Options
from game_ui.display_ui import Display
from typing import List


class WarUI:
    def __init__(self, window, scroll_idx, user):
        self.window = window
        # self.scroll_idx = scroll_idx
        self.scroll_idx = 1
        self.display = Display(self.window, self.scroll_idx, user)

    def war_menu(self) -> List[str]:
        menu = Options.GAME_STARTUP.value
        result = []

        while True:
            self.display.display_options(menu, ["War Menu"])
            self.scroll_idx = self.display.scroll_options(menu,
                                                          ["War Menu"])

            if menu[self.scroll_idx] == "New Game":
                result = self.play_war()

            elif self.scroll_idx == len(menu) - 1:
                break

            self.display.scroll_idx = 1

        return result

    def play_war(self) -> List[str]:
        input_system = InputSystem(Game.WAR)
        games_won = 0
        option_list = Options.WAR_OPTIONS.value
        status = input_system.get_last_guess()
        game_info = ["War", status, str(games_won)]

        while True:
            status = input_system.get_last_guess()
            game_info[1] = status
            game_info[2] = str(games_won)

            self.display.display_options(option_list, game_info)
            self.scroll_idx = self.display.scroll_options(option_list,
                                                          game_info)

            if option_list[self.scroll_idx] == "Flip Card":
                input_system.take_input("flip card")
                info = input_system.get_last_guess()

                if info[4]:
                    option_list = Options.WAR_NEW_GAME.value

                    if info[5] == 2:
                        option_list[0] = "You Lose!"
                    else:
                        option_list[0] = "You Win!"
                        games_won += 1

            elif option_list[self.scroll_idx] == "Reset" or \
                    option_list[self.scroll_idx] == "New Game":
                input_system.take_input("reset")
                option_list = Options.WAR_OPTIONS.value

            elif option_list[self.scroll_idx] == "Clear":
                option_list = Options.WAR_OPTIONS.value
                input_system.take_input("clear")
                games_won = 0

            elif self.scroll_idx == len(option_list) - 1:
                self.scroll_idx = 1
                break

        return option_list
