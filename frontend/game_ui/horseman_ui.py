from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from game_ui.menu_options import Options
from game_ui.display_ui import Display
from pyarcade.difficulties import Difficulty
from typing import List


class HorsemanUI:
    """
    UI for Horseman.
    """
    def __init__(self, window, scroll_idx, user):
        self.window = window
        # self.scroll_idx = scroll_idx
        self.scroll_idx = 1
        self.display = Display(self.window, self.scroll_idx, user)

    def horseman_menu(self) -> List[str]:
        """
        Horseman menu screen.
        Returns:
            List containing information about the game played.
        """
        menu = Options.GAME_STARTUP_DIFFICULT.value
        result = []

        while True:
            self.display.display_options(menu, ["Horseman Menu"])
            self.scroll_idx = self.display.scroll_options(menu,
                                                          ["Horseman Menu"])

            if menu[self.scroll_idx] == "Normal Mode":
                result = self.play_horseman()

            elif menu[self.scroll_idx] == "Easy Mode":
                result = self.play_horseman(Difficulty.EASY)

            elif menu[self.scroll_idx] == "Hard Mode":
                result = self.play_horseman(Difficulty.HARD)

            elif self.scroll_idx == len(menu) - 1:
                break

            self.display.scroll_idx = 1

        return result

    def play_horseman(self, mode=Difficulty.NORMAL) -> List[str]:
        """
        Horseman game screen.
        Args:
            mode: Game difficulty.

        Returns:
            List containing information about the game played.
        """
        input_system = InputSystem(Game.HORSEMAN, mode)
        games_won = 0
        option_list = Options.HORSEMAN_OPTIONS.value
        game_info = ["Horseman", "", 0, "", "", ""]

        while True:
            game_info[1] = input_system.get_last_guess()[0]
            game_info[2] = str(games_won)

            self.display.display_options(option_list, game_info)
            self.scroll_idx = self.display.scroll_options(option_list,
                                                          game_info)

            if option_list[self.scroll_idx] == "Take Guess":
                message = "Please enter a letter"
                guess = self.display.user_input_window(message, "").strip()
                result = input_system.take_input(guess)

                if result[1]:
                    game_info[4] = ""
                    status = input_system.get_last_guess()

                    horse = "HORSE!"
                    game_info[3] = horse[:6 - status[1]]
                    game_info[5] += guess

                    if result[0]:
                        option_list = Options.HORSEMAN_NEW_GAME.value

                        if status[1] == 0:
                            game_info[4] = "You Lose! The word was "\
                                           + status[2]
                        else:
                            game_info[4] = "You Win!"
                            games_won += 1
                else:
                    game_info[4] = "Incorrect Input: Try Again"

            elif option_list[self.scroll_idx] == "Reset" or \
                    option_list[self.scroll_idx] == "New Game":
                input_system.take_input("reset")
                game_info = ["Horseman", "", 0, "", "", ""]
                option_list = Options.HORSEMAN_OPTIONS.value

            elif option_list[self.scroll_idx] == "Clear":
                option_list = Options.HORSEMAN_OPTIONS.value
                input_system.take_input("clear")
                game_info = ["Horseman", "", 0, "", "", ""]
                games_won = 0

            elif self.scroll_idx == len(option_list) - 1:
                self.scroll_idx = 1
                break

        return option_list
