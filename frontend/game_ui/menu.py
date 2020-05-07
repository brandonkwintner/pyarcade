from game_ui.menu_options import Options
from pyarcade.connection import Connections
from game_ui.mastermind_ui import MastermindUI
from game_ui.connect4_ui import Connect4UI
from game_ui.blackjack_ui import BlackjackUI
from game_ui.war_ui import WarUI
from game_ui.go_fish_ui import GoFishUI
from game_ui.horseman_ui import HorsemanUI
from game_ui.display_ui import Display
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
        self.user = {"username": "", "token": ""}

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

    def main_menu(self):
        """
        UI for main menu.
        """
        display = ["Pyarcade", ""]

        while True:
            if self.is_login:
                menu_option = Options.MAIN_MENU_START.value
            else:
                menu_option = Options.MAIN_MENU_OPTIONS.value

            self.display.display_options(menu_option, display)
            self.scroll_idx = self.display.scroll_options(menu_option,
                                                          display)

            if menu_option[self.scroll_idx] == "Play Games":
                self.game_menu()

            elif menu_option[self.scroll_idx] == "Signup":
                username, password = self.display.account_login_signup(True)
                status = Connections.sign_up_account(username.strip(),
                                                     password.strip())
                if status["code"] == 200:
                    self.user["username"] = "Hello " + username
                    self.user["token"] = status["access"]
                    self.display.user = self.user
                    self.is_login = True
                    display[1] = ""

                else:
                    display[1] = status["message"]

            elif menu_option[self.scroll_idx] == "Login":
                username, password = self.display.account_login_signup(False)
                status = Connections.login_account(username.strip(),
                                                   password.strip())
                if status["code"] == 200:
                    self.user["username"] = "Hello, " + username
                    self.user["token"] = status["access"]
                    self.display.user = self.user
                    self.is_login = True
                    display[1] = ""

                else:
                    display[1] = status["message"]

            elif menu_option[self.scroll_idx] == "Logout":
                self.user = {"username": "", "token": ""}
                self.display.user = {"username": "", "token": ""}
                self.is_login = False

            elif menu_option[self.scroll_idx] == "About":
                self.display.about_screen()

            elif menu_option[self.scroll_idx] == "Friends":
                self.friend_menu()

            elif self.scroll_idx == len(menu_option) - 1:
                self.close_curse()
                break

            self.display.scroll_idx = 1

    def game_menu(self):
        """
        UI for game menu.
        """
        games = Options.GAME_OPTIONS.value

        while True:
            self.display.display_options(games, ["Game List"])
            self.scroll_idx = self.display.scroll_options(games, ["Game List"])

            if games[self.scroll_idx] == "Play Mastermind":
                MastermindUI(self.window, self.user).mastermind_menu()

            elif games[self.scroll_idx] == "Play Connect Four":
                Connect4UI(self.window, self.user).connect_four_menu()

            elif games[self.scroll_idx] == "Play Blackjack":
                BlackjackUI(self.window, self.user).blackjack_menu()

            elif games[self.scroll_idx] == "Play War":
                WarUI(self.window, self.user).war_menu()

            elif games[self.scroll_idx] == "Play Go Fish":
                GoFishUI(self.window, self.user).go_fish_menu()

            elif games[self.scroll_idx] == "Play Horseman":
                HorsemanUI(self.window, self.user).horseman_menu()

            elif self.scroll_idx == len(games) - 1:
                break

            self.display.scroll_idx = 1

    def friend_menu(self):
        """UI for friend menu.
        """

        menu_option = Options.FRIEND_OPTION.value
        info = ["Friend List", ""]

        while True:
            self.display.display_options(menu_option, info)
            self.scroll_idx = self.display.scroll_options(menu_option,
                                                          info)

            if menu_option[self.scroll_idx] == "Friend List":
                friends = Connections.get_friends(self.user["token"])
                self.display.display_friend_list(friends["friends"])

            elif menu_option[self.scroll_idx] == "Add Friend":
                username = self.display.friend_username().strip()
                status = Connections.add_friend(username, self.user["token"])

                if status["code"] != 200:
                    info[1] = status["message"]
                else:
                    info[1] = "Friend Added"

            elif self.scroll_idx == len(menu_option) - 1:
                break

            self.display.scroll_idx = 1

    @staticmethod
    def run():
        menu_list = Menu()
        menu_list.main_menu()


if __name__ == "__main__":
    option = Menu()
    option.main_menu()
