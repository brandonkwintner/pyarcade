from game_ui.menu_options import Options
from pyarcade.connection import Connections
from game_ui.mastermind_ui import MastermindUI
from game_ui.connect4_ui import Connect4UI
from game_ui.blackjack_ui import BlackjackUI
from game_ui.war_ui import WarUI
from game_ui.go_fish_ui import GoFishUI
from game_ui.horseman_ui import HorsemanUI
from game_ui.display_ui import Display
from typing import List
import curses


class Menu:
    """
    UI for menus.
    """
    def __init__(self):
        self.window = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.user = ""

        self.window.keypad(True)
        self.scroll_idx = 1
        self.is_login = False

        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)

        self.display = Display(self.window, self.scroll_idx, self.user)

    def close_curse(self):
        curses.nocbreak()
        self.window.keypad(False)
        curses.echo()
        curses.endwin()

    def main_menu(self) -> List[str]:
        """
        UI for main menu.
        Returns:
            Result of selected option.
        """
        menu_option = Options.MAIN_MENU_OPTIONS.value
        result = []

        while True:
            self.display.display_options(menu_option, ["Pyarcade"])
            self.scroll_idx = self.display.scroll_options(menu_option,
                                                          ["Pyarcade"])

            if menu_option[self.scroll_idx] == "Play Games":
                result = self.game_menu()

            elif menu_option[self.scroll_idx] == "Options":
                result = self.options_menu()

            elif self.scroll_idx == len(menu_option) - 1:
                # result = menu_option
                self.close_curse()
                break
            self.display.scroll_idx = 1
        return result

    def game_menu(self) -> List[str]:
        """
        UI for game menu.
        Returns:
            Result of selected option.
        """
        games = Options.GAME_OPTIONS.value
        result = []

        while True:
            self.display.display_options(games, ["Game List"])
            self.scroll_idx = self.display.scroll_options(games, ["Game List"])

            if games[self.scroll_idx] == "Play Mastermind":
                result = MastermindUI(self.window, self.scroll_idx, self.user) \
                    .mastermind_menu()

            elif games[self.scroll_idx] == "Play Connect Four":
                result = Connect4UI(self.window, self.scroll_idx, self.user) \
                    .connect_four_menu()

            elif games[self.scroll_idx] == "Play Blackjack":
                result = BlackjackUI(self.window, self.scroll_idx, self.user) \
                    .blackjack_menu()

            elif games[self.scroll_idx] == "Play War":
                result = WarUI(self.window, self.scroll_idx,
                               self.user).war_menu()

            elif games[self.scroll_idx] == "Play Go Fish":
                result = GoFishUI(self.window, self.scroll_idx,
                                  self.user).go_fish_menu()

            elif games[self.scroll_idx] == "Play Horseman":
                result = HorsemanUI(self.window, self.scroll_idx,
                                  self.user).horseman_menu()

            elif self.scroll_idx == len(games) - 1:
                result = games
                break

        return result

    def options_menu(self) -> List[str]:
        """
        UI for options menu.
        Returns:
            List containing all options.
        """
        if self.is_login:
            option_list = Options.FEATURE_LOGOUT_OPTIONS.value
        else:
            option_list = Options.FEATURE_OPTIONS.value
        display_list = ['Options', '']
        self.display.scroll_idx = 1

        while True:
            self.display.display_options(option_list, display_list)
            self.scroll_idx = self.display.scroll_options(option_list,
                                                          display_list)

            if option_list[self.scroll_idx] == "Signup":
                username, password = self.display.account_login_signup(True)
                status = Connections.sign_up_account(username.strip(),
                                                     password.strip())
                if status["code"] == 200:
                    self.user = "Hello " + username
                    self.display.user = self.user
                    self.is_login = True
                    break
                else:
                    display_list[1] = status["message"]

            elif option_list[self.scroll_idx] == "Login":
                username, password = self.display.account_login_signup(False)
                status = Connections.login_account(username.strip(),
                                                   password.strip())
                if status["code"] == 200:
                    self.user = "Hello " + username
                    self.display.user = self.user
                    self.is_login = True
                    break
                else:
                    display_list[1] = status["message"]

            elif option_list[self.scroll_idx] == "Logout":
                self.user = ""
                self.display.user = ""
                self.is_login = False
                option_list = Options.FEATURE_OPTIONS.value

            elif option_list[self.scroll_idx] == "About":
                self.display.about_screen()

            elif self.scroll_idx == len(option_list) - 1:
                self.scroll_idx = 1
                break

        return option_list

    @staticmethod
    def run():
        menu_list = Menu()
        menu_list.main_menu()


if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()
