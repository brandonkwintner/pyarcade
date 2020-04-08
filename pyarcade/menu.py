from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from pyarcade.menu_options import Options
from curses.textpad import rectangle, Textbox
from typing import List
import curses


class Menu:
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()

        self.stdscr.keypad(True)
        self.option_idx = 1
        self.height, self.width = self.stdscr.getmaxyx()
        self.rect_width = 13
        self.rect_length = 1
        self.x_start_position = self.width // 2 - self.width // 6
        self.testing = False
        self.testing_function = ""

        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def close_curse(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def display_options(self, opts: List[str], info: List[str]) -> List[str]:
        self.stdscr.clear()
        line_num = self.display_game_info(info) + 2

        for idx, text in enumerate(opts):
            if idx == self.option_idx:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(line_num, self.x_start_position, text)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(line_num, self.x_start_position, text)

            line_num += 2

        self.stdscr.refresh()

        return opts

    def display_game_info(self, info: List[str]) -> int:
        line_num = 3
        name = info[0]

        self.stdscr.addstr(line_num - 1, self.x_start_position, name)

        if name == "Mastermind":
            game_state = "Game #" + info[2]
            self.stdscr.addstr(0, 0, game_state)

            for row in info[1].split('\n'):
                line_num += 1
                self.stdscr.addstr(line_num, self.x_start_position, row)

        elif name == "Connect Four":
            game_state = "Game #" + info[2]
            self.stdscr.addstr(0, 0, game_state)

            game_turn = "Turn: " + info[3]
            self.stdscr.addstr(1, 0, game_turn)

            for row in info[1].split('\n'):
                line_num += 1
                self.stdscr.addstr(line_num, self.x_start_position, row)

        elif name == "Blackjack":
            game_state = "Games Won: " + info[2]
            self.stdscr.addstr(0, 0, game_state)

            line_num += 1
            self.stdscr.addstr(line_num, self.x_start_position,
                               "Player Hand: ")
            self.stdscr.addstr(line_num + 1, self.x_start_position, info[1][0])

            if info[3] == "Show":
                line_num += 3
                self.stdscr.addstr(line_num, self.x_start_position,
                                   "Dealer Hand: ")
                self.stdscr.addstr(line_num + 1, self.x_start_position,
                                   info[1][1])

            line_num += 2

        return line_num

    def scroll_options(self, opts: List[str], info: List[str]) -> int:
        while True:
            key = self.stdscr.getch()
            self.stdscr.clear()

            if key == curses.KEY_UP and self.option_idx > 1:
                self.option_idx -= 1
            elif key == curses.KEY_DOWN and self.option_idx < len(opts) - 1:
                self.option_idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return self.option_idx
            self.display_options(opts, info)
            self.stdscr.refresh()

            if self.testing:
                break

    def user_input_window(self, message: str, user_input: str) -> str:
        message_x_pos = self.width // 2 - len(message) // 2
        self.stdscr.addstr(0, message_x_pos, message)

        exit_message = "Press ENTER to submit"
        exit_x_pos = self.width // 2 - len(exit_message) // 2
        self.stdscr.addstr(2, exit_x_pos, exit_message)

        if user_input == "":
            edit_begin_y = self.height // 4
            edit_begin_x = self.width // 2 - self.rect_width // 2
            edit_window = curses.newwin(1, 13, edit_begin_y, edit_begin_x)

            rectangle(self.stdscr, edit_begin_y - 1, edit_begin_x - 2,
                      edit_begin_y + self.rect_length,
                      edit_begin_x + self.rect_width)

            self.stdscr.refresh()
            box = Textbox(edit_window)

            if self.testing:
                return "user"
            box.edit()
            user_input = box.gather()

        return user_input

    def main_menu(self) -> List[str]:
        menu_option = Options.MAIN_MENU_OPTIONS.value
        result = []

        while True:
            if not self.testing:
                self.display_options(menu_option, ["Pyarcade"])
                self.scroll_options(menu_option, ["Pyarcade"])

            if self.option_idx == 1:
                result = self.mastermind_menu()
            elif self.option_idx == 2:
                result = self.connect_four_menu()
            elif self.option_idx == 3:
                result = self.blackjack_menu()
            elif self.option_idx == len(menu_option) - 1:
                result = menu_option
                self.close_curse()
                break

            if self.testing:
                break

        return result

    def mastermind_menu(self) -> List[str]:
        input_system = InputSystem(Game.MASTERMIND)
        option_list = Options.MASTERMIND_OPTIONS.value

        while True:
            game = input_system.game_num
            status = input_system.get_last_guess()
            game_info = ["Mastermind", status, str(game)]

            if not self.testing:
                self.display_options(option_list, game_info)
                self.scroll_options(option_list, game_info)

            if option_list[self.option_idx] == "Take Guess":
                message = "Please enter 4 digits 0 to 9 inclusive"
                guess = self.user_input_window(message, "")

                if input_system.take_input(" ".join(guess))[0]:
                    option_list = Options.MASTERMIND_NEW_GAME.value
                self.testing_function = "guess"

            elif option_list[self.option_idx] == "Reset" or \
                    option_list[self.option_idx] == "New Game":
                option_list = Options.MASTERMIND_OPTIONS.value
                input_system.take_input("reset")
                self.testing_function = "reset"

            elif option_list[self.option_idx] == "Clear":
                option_list = Options.MASTERMIND_OPTIONS.value
                input_system.take_input("clear")
                self.testing_function = "clear"

            elif self.option_idx == len(option_list) - 1:
                self.option_idx = 1
                break

            if self.testing:
                break

        return option_list

    def connect_four_menu(self) -> List[str]:
        option_list = Options.CONNECT_FOUR_OPTIONS.value
        input_system = InputSystem(Game.CONNECT4)

        while True:
            status = input_system.get_last_guess()
            game = input_system.game_num
            game_info = ["Connect Four", status, str(game),
                         input_system.get_round_info()]

            if not self.testing:
                self.display_options(option_list, game_info)
                self.scroll_options(option_list, game_info)

            if option_list[self.option_idx] == "Enter Column":
                message = "Please enter a digits between 1 to 7"
                guess = self.user_input_window(message, "")

                if input_system.take_input(guess)[0]:
                    option_list = Options.CONNECT_FOUR_NEW_GAME.value
                    
                    if game_info[3] == 'Player X':
                        option_list[0] = 'Player X Wins!'
                    else:
                        option_list[0] = 'Player O Wins!'
                self.testing_function = "column"

            elif option_list[self.option_idx] == "Reset" or \
                    option_list[self.option_idx] == "New Game":
                input_system.take_input("reset")
                option_list = Options.CONNECT_FOUR_OPTIONS.value
                self.testing_function = "reset"

            elif option_list[self.option_idx] == "Clear":
                option_list = Options.CONNECT_FOUR_OPTIONS.value
                input_system.take_input("clear")
                self.testing_function = "clear"

            elif self.option_idx == len(option_list) - 1:
                self.option_idx = 1
                break

            if self.testing:
                break

        return option_list

    def blackjack_menu(self) -> List[str]:
        input_system = InputSystem(Game.BLACKJACK)
        games_won = 0
        option_list = Options.BLACKJACK_OPTIONS.value
        status = input_system.get_last_guess()
        game_info = ["Blackjack", status[0], str(games_won), ""]

        while True:
            status = input_system.get_last_guess()
            game_info[1] = status[0]
            game_info[2] = str(games_won)

            if not self.testing:
                self.display_options(option_list, game_info)
                self.scroll_options(option_list, game_info)

            if option_list[self.option_idx] == "Hit":
                input_system.take_input("hit")
                self.testing_function = "hit"

            elif option_list[self.option_idx] == "Reset" or \
                    option_list[self.option_idx] == "New Game":
                input_system.take_input("reset")
                option_list = Options.BLACKJACK_OPTIONS.value
                game_info[3] = "Hidden"
                self.testing_function = "reset"

            elif option_list[self.option_idx] == "Clear":
                input_system.take_input("clear")
                option_list = Options.BLACKJACK_OPTIONS.value
                game_info[3] = "Hidden"
                games_won = 0
                self.testing_function = "clear"

            elif option_list[self.option_idx] == "Stand":
                input_system.take_input("stand")
                option_list = Options.BLACKJACK_NEW_GAME.value
                game_info[3] = "Show"

                if input_system.get_last_guess()[1]:
                    option_list[0] = "Player Wins!"
                    games_won += 1
                else:
                    option_list[0] = "Dealer Wins!"
                self.testing_function = "stand"

            elif self.option_idx == len(option_list) - 1:
                self.option_idx = 1
                break

            if self.testing:
                break

        return option_list

    @staticmethod
    def run():
        menu_list = Menu()
        menu_list.main_menu()


if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()
