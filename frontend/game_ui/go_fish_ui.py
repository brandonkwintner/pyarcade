from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from game_ui.menu_options import Options
from game_ui.display_ui import Display
from typing import List


class GoFishUI:
    def __init__(self, window, scroll_idx, user):
        self.window = window
        # self.scroll_idx = scroll_idx
        self.scroll_idx = 1
        self.display = Display(self.window, self.scroll_idx, user)

    def go_fish_menu(self) -> List[str]:
        menu = Options.GAME_STARTUP.value
        result = []

        while True:
            self.display.display_options(menu, ["Go Fish Menu"])
            self.scroll_idx = self.display.scroll_options(menu,
                                                          ["Go Fish Menu"])

            if menu[self.scroll_idx] == "New Game":
                result = self.play_go_fish()

            elif menu[self.scroll_idx] == "Instructions":
                result = []

            elif self.scroll_idx == len(menu) - 1:
                break

            self.display.scroll_idx = 1

        return result

    def play_go_fish(self) -> List[str]:
        input_system = InputSystem(Game.GO_FISH)
        games_won = 0
        option_list = Options.GO_FISH_OPTIONS.value
        status = input_system.get_last_guess()
        game_info = ["Go Fish", status, str(games_won), ""]

        while True:
            status = input_system.get_last_guess()
            game_info[1] = status
            game_info[2] = str(games_won)

            self.display.display_options(option_list, game_info)
            self.scroll_idx = self.display.scroll_options(option_list,
                                                          game_info)

            if self.scroll_idx > len(option_list) - 1:
                break

            if option_list[self.scroll_idx] == "Take Guess":
                message = "Please enter Card Rank (Full Name or Number)"
                guess = self.display.user_input_window(message, "")

                if not guess == "":
                    input_result = input_system.take_input(guess.strip())

                    if not input_result[1]:
                        game_info[3] = "Invalid input: Try Again"
                    else:
                        info = input_system.get_last_guess()

                        if input_result[0]:
                            option_list = Options.GO_FISH_NEW_GAME.value
                            game_info[3] = ""

                            if info[2] == 1:
                                option_list[0] = "You Win!"
                                games_won += 1
                            else:
                                option_list[0] = "You Lose!"
                        else:
                            if info[1]:
                                game_info[3] = "Go Fish"
                            else:
                                game_info[3] = "Correct Guess"

            elif option_list[self.scroll_idx] == "Reset" or \
                    option_list[self.scroll_idx] == "New Game":
                input_system.take_input("reset")
                option_list = Options.GO_FISH_OPTIONS.value

            elif option_list[self.scroll_idx] == "Clear":
                option_list = Options.GO_FISH_OPTIONS.value
                input_system.take_input("clear")
                games_won = 0

            elif self.scroll_idx == len(option_list) - 1:
                self.scroll_idx = 1
                break

        return option_list
