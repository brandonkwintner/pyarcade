from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from game_ui.menu_options import Options
from game_ui.display_ui import Display
from typing import List


class BlackjackUI:
    """
    UI for Black Jack.
    """
    def __init__(self, window, scroll_idx, user):
        self.window = window
        # self.scroll_idx = scroll_idx
        self.scroll_idx = 1
        self.display = Display(self.window, self.scroll_idx, user)

    def blackjack_menu(self) -> List[str]:
        """
        Black Jack menu screen.
        Returns:
            List containing result of Black Jack game.
        """
        menu = Options.GAME_STARTUP.value
        result = []

        while True:
            self.display.display_options(menu, ["Blackjack Menu"])
            self.scroll_idx = self.display.scroll_options(menu,
                                                          ["Blackjack Menu"])

            if menu[self.scroll_idx] == "New Game":
                result = self.play_blackjack()

            elif self.scroll_idx == len(menu) - 1:
                break

            self.display.scroll_idx = 1

        return result

    def play_blackjack(self) -> List[str]:
        """
        Black Jack game screen.
        Returns:
            List containing information about the game played.
        """
        input_system = InputSystem(Game.BLACKJACK)
        games_won = 0
        option_list = Options.BLACKJACK_OPTIONS.value
        status = input_system.get_last_guess()
        game_info = ["Blackjack", status[0], str(games_won), ""]

        while True:
            status = input_system.get_last_guess()
            game_info[1] = status[0]
            game_info[2] = str(games_won)

            self.display.display_options(option_list, game_info)
            self.scroll_idx = self.display.scroll_options(option_list,
                                                          game_info)

            if option_list[self.scroll_idx] == "Hit":
                input_system.take_input("hit")

            elif option_list[self.scroll_idx] == "Reset" or \
                    option_list[self.scroll_idx] == "New Game":
                input_system.take_input("reset")
                option_list = Options.BLACKJACK_OPTIONS.value
                game_info[3] = "Hidden"

            elif option_list[self.scroll_idx] == "Clear":
                input_system.take_input("clear")
                option_list = Options.BLACKJACK_OPTIONS.value
                game_info[3] = "Hidden"
                games_won = 0

            elif option_list[self.scroll_idx] == "Stand":
                input_system.take_input("stand")
                option_list = Options.BLACKJACK_NEW_GAME.value
                game_info[3] = "Show"

                if input_system.get_last_guess()[1]:
                    option_list[0] = "Player Wins!"
                    games_won += 1
                else:
                    option_list[0] = "Dealer Wins!"

            elif self.scroll_idx == len(option_list) - 1:
                self.scroll_idx = 1
                break

        return option_list
