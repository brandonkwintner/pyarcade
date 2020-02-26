from pyarcade.input_system import InputSystem
from pyarcade.mastermind import Mastermind
from pyarcade.game_option import Game
from pyarcade.connect4 import Connect4
from pyarcade.blackjack import Blackjack
from curses.textpad import rectangle, Textbox
from typing import List, Tuple, Union
import curses

MAIN_MENU_OPTIONS = ['', 'Play Mastermind', 'Play Connect Four', 'Play Blackjack', 'Exit']
MASTERMIND_OPTIONS = ['', 'Take Guess', 'Reset', 'Clear', 'Back']
MASTERMIND_RESULT = ['You Win!', 'New Game', 'Clear', 'Back']
CONNECT_FOUR_OPTIONS = ['', 'Enter Column', 'Reset', 'Clear', 'Back']
CONNECT_FOUR_RESULT = ['', 'New Game', 'Clear', 'Back']
BLACKJACK_OPTIONS = ['', 'Hit', 'Stand', 'Reset', 'Clear', 'Back']
BLACKJACK_RESULT = ['', 'New Game', 'Clear', 'Back']


class Menu:
    @staticmethod
    def print_menu(stdscr, options: List[str], current_row: int, game_info: List[str]):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        line = Menu.display_game_info(stdscr, game_info) + 2

        for idx, text in enumerate(options):
            x_position = width // 2 - width // 6

            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(line, x_position, text)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(line, x_position, text)

            line += 2

        stdscr.refresh()

    @staticmethod
    def display_game_info(stdscr, game_info: List[str]) -> int:
        line = 3
        name = game_info[0]
        width = stdscr.getmaxyx()[1]
        x_position = width // 2 - width // 6
        stdscr.addstr(2, x_position, name)

        if name == "Mastermind":
            game_state = "Game #" + game_info[2]
            stdscr.addstr(0, 0, game_state)

            for row in game_info[1].split('\n'):
                stdscr.addstr(line, x_position, row)
                line += 1

        elif name == "Connect Four":
            game_state = "Game #" + game_info[2]
            stdscr.addstr(0, 0, game_state)
            game_turn = "Turn: " + game_info[3]
            stdscr.addstr(1, 0, game_turn)

            for row in game_info[1].split('\n'):
                line += 1
                stdscr.addstr(line, x_position, row)

        elif name == "Blackjack":
            game_state = "Games Won: " + game_info[2]
            stdscr.addstr(0, 0, game_state)

            line += 1
            stdscr.addstr(line, x_position, "Player Hand: ")
            stdscr.addstr(line + 1, x_position, game_info[1][0])

            if game_info[3] == "Show":
                line += 3
                stdscr.addstr(line, x_position, "Dealer Hand: ")
                stdscr.addstr(line + 1, x_position, game_info[1][1])
            line += 2

        return line

    @staticmethod
    def scroll_options(stdscr, options: List[str], current_row: int, game_info: List[str]) -> int:
        while True:
            key = stdscr.getch()
            stdscr.clear()

            if key == curses.KEY_UP and current_row > 1:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(options) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return current_row

            Menu.print_menu(stdscr, options, current_row, game_info)
            stdscr.refresh()

    @staticmethod
    def user_input_window(stdscr, message: str, rect_length: int, rect_width: int) -> str:
        height, width = stdscr.getmaxyx()
        stdscr.addstr(0, width//2 - len(message)//2, message)
        exit_message = "Press ENTER to submit"
        stdscr.addstr(2, width // 2 - len(exit_message) // 2, exit_message)

        edit_begin_y = height // 4
        edit_begin_x = width // 2 - rect_width // 2
        edit_window = curses.newwin(1, 13, edit_begin_y, edit_begin_x)

        rectangle(stdscr, edit_begin_y - 1, edit_begin_x - 2,
                  edit_begin_y + rect_length, edit_begin_x + rect_width)
        stdscr.refresh()
        box = Textbox(edit_window)
        box.edit()

        return box.gather()

    @staticmethod
    def main_menu(stdscr):
        idx = 1

        while True:
            Menu.print_menu(stdscr, MAIN_MENU_OPTIONS, idx, ["Pyarcade"])
            idx = Menu.scroll_options(stdscr, MAIN_MENU_OPTIONS, idx, ["Pyarcade"])

            if idx == 1:
                Menu.mastermind_menu(stdscr)
            elif idx == 2:
                Menu.connect_four_menu(stdscr)
            elif idx == 3:
                Menu.blackjack_menu(stdscr)
            elif idx == len(MAIN_MENU_OPTIONS) - 1:
                break

        return stdscr

    @staticmethod
    def mastermind_menu(stdscr):
        idx = 1
        game = 1
        input_system = InputSystem(Game.MASTERMIND)
        options = MASTERMIND_OPTIONS

        while True:
            status = input_system.get_last_guess()
            game_info = ["Mastermind", status, str(game)]

            Menu.print_menu(stdscr, options, idx, game_info)
            idx = Menu.scroll_options(stdscr, options, idx, game_info)

            if options[idx] == "Take Guess":
                message = "Please enter 4 digits 0 to 9 inclusive"
                guess = Menu.user_input_window(stdscr, message, 1, 13)
                if input_system.take_input(" ".join(guess))[0]:
                    options = MASTERMIND_RESULT
                    game += 1
            elif options[idx] == "Reset" or options[idx] == "New Game":
                options = MASTERMIND_OPTIONS
                input_system.take_input("reset")
            elif options[idx] == "clear":
                game = 1
                options = MASTERMIND_OPTIONS
                input_system.take_input("clear")
            elif idx == len(options) - 1:
                break

    @staticmethod
    def connect_four_menu(stdscr):
        idx = 1
        game = 1
        options = CONNECT_FOUR_OPTIONS
        input_system = InputSystem(Game.CONNECT4)

        while True:
            status = input_system.get_last_guess()
            game_info = ["Connect Four", status, str(game), input_system.get_round_info()]

            Menu.print_menu(stdscr, options, idx, game_info)
            idx = Menu.scroll_options(stdscr, options, idx, game_info)

            if options[idx] == "Enter Column":
                message = "Please enter a digits between 1 to 7"
                guess = Menu.user_input_window(stdscr, message, 1, 13)

                if input_system.take_input(guess)[0]:
                    options = CONNECT_FOUR_RESULT
                    if game_info[3] == 'Player X':
                        options[0] = 'Player X Wins!'
                    else:
                        options[0] = 'Player O Wins!'
                    game += 1
            elif options[idx] == "Reset" or options[idx] == "New Game":
                input_system.take_input("reset")
                options = CONNECT_FOUR_OPTIONS
            elif options[idx] == "Clear":
                game = 1
                options = CONNECT_FOUR_OPTIONS
                input_system.take_input("clear")
            elif idx == len(options) - 1:
                break

    @staticmethod
    def blackjack_menu(stdscr):
        input_system = InputSystem(Game.BLACKJACK)
        options = BLACKJACK_OPTIONS
        idx = 1
        games_won = 0
        status = input_system.get_last_guess()
        game_info = ["Blackjack", status[0], str(games_won), ""]

        while True:
            status = input_system.get_last_guess()
            game_info[1] = status[0]
            game_info[2] = str(games_won)

            Menu.print_menu(stdscr, options, idx, game_info)
            idx = Menu.scroll_options(stdscr, options, idx, game_info)

            if options[idx] == "Hit":
                input_system.take_input("hit")
            elif options[idx] == "Stand":
                input_system.take_input("stand")
                options = BLACKJACK_RESULT
                game_info[3] = "Show"

                if input_system.get_last_guess()[1]:
                    BLACKJACK_RESULT[0] = "Player Wins!"
                    games_won += 1
                else:
                    BLACKJACK_RESULT[0] = "Dealer Wins!"

            elif options[idx] == "Reset" or options[idx] == "New Game":
                input_system.take_input("reset")
                options = BLACKJACK_OPTIONS
                game_info[3] = "Hidden"
            elif options[idx] == "Clear":
                input_system.take_input("clear")
                options = BLACKJACK_OPTIONS
                game_info[3] = "Hidden"
                games_won = 0
            elif idx == len(options) - 1:
                break


if __name__ == "__main__":
    menu = Menu()
    curses.wrapper(menu.main_menu)





