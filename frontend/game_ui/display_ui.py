from curses.textpad import rectangle
from typing import List
import curses
import curses.textpad as textpad


class Display:
    """
    Display utility for UI.
    """
    def __init__(self, window, scroll_idx, user):
        self.window = window
        self.user = user
        self.height, self.width = self.window.getmaxyx()
        self.x_start_position = self.width // 2 - self.width // 5
        self.scroll_idx = scroll_idx

    def display_options(self, opts: List[str], info: List[str]) -> List[str]:
        """
        Displays options list for screen.
        Args:
            opts: List of options.
            info: Game information.

        Returns:
            List of options.
        """
        self.window.clear()
        self.window.addstr(0, self.x_start_position, self.user["username"])
        line_num = self.display_game_info(info) + 2

        for idx, text in enumerate(opts):
            if idx == self.scroll_idx:
                self.window.attron(curses.color_pair(1))
                self.window.addstr(line_num, self.x_start_position, text)
                self.window.attroff(curses.color_pair(1))
            else:
                self.window.addstr(line_num, self.x_start_position, text)

            line_num += 2

        self.window.refresh()

        return opts

    def display_game_info(self, info: List[str]) -> int:
        """
        Display game information.
        Args:
            info: Game information

        Returns:
            Line number.
        """
        line_num = 3
        name = info[0]

        self.window.addstr(line_num - 1, self.x_start_position, name)

        if name == "Mastermind":
            game_state = "Games Played: " + info[2]
            self.window.addstr(0, 0, game_state)

            for row in info[1].split('\n'):
                line_num += 1
                self.window.addstr(line_num, self.x_start_position, row)

            line_num += 1
            self.window.addstr(line_num, self.x_start_position, info[3])

        elif name == "Connect Four":
            game_state = "Games Played: " + info[3]
            self.window.addstr(0, 0, game_state)
            game_state = "Games Won: " + info[2]
            self.window.addstr(1, 0, game_state)

            for row in info[1][0].split('\n'):
                line_num += 1
                self.window.addstr(line_num, self.x_start_position, row)

        elif name == "Blackjack":
            game_state = "Games Played: " + info[4]
            self.window.addstr(0, 0, game_state)
            game_state = "Games Won: " + info[2]
            self.window.addstr(1, 0, game_state)

            line_num += 1
            player_hand = info[1][0].split(":")

            self.window.addstr(line_num, self.x_start_position,
                               "Player Hand: " + player_hand[1])
            self.window.addstr(line_num + 1, self.x_start_position,
                               player_hand[0])

            if info[3] == "Show":
                line_num += 3
                dealer_hand = info[1][1].split(":")

                self.window.addstr(line_num, self.x_start_position,
                                   "Dealer Hand: " + dealer_hand[1])
                self.window.addstr(line_num + 1, self.x_start_position,
                                   dealer_hand[0])

            line_num += 2

        elif name == "War":
            game_state = "Games Played: " + info[3]
            self.window.addstr(0, 0, game_state)
            game_state = "Games Won: " + info[2]
            self.window.addstr(1, 0, game_state)

            line_num += 1
            self.window.addstr(line_num, self.x_start_position,
                               "Player 1 Card Count: " + str(info[1][2]))
            self.window.addstr(line_num + 1, self.x_start_position, info[1][0])

            line_num += 3
            self.window.addstr(line_num, self.x_start_position,
                               "Player 2 Card Count: " + str(info[1][3]))
            self.window.addstr(line_num + 1, self.x_start_position,
                               info[1][1])

            line_num += 2

        elif name == "Go Fish":
            game_state = "Games Played: " + info[4]
            self.window.addstr(0, 0, game_state)
            game_state = "Games Won: " + info[2]
            self.window.addstr(1, 0, game_state)

            line_num += 1
            self.window.addstr(line_num, self.x_start_position,
                               "Player hand: ")
            self.window.addstr(line_num + 1, self.x_start_position, info[1][0])

            line_num += 3

            self.window.addstr(line_num + 2, self.x_start_position, info[3])

            line_num += 2

        elif name == "Horseman":
            game_state = "Games Played: " + info[6]
            self.window.addstr(0, 0, game_state)
            game_state = "Games Won: " + info[2]
            self.window.addstr(1, 0, game_state)

            line_num += 1
            self.window.addstr(line_num, self.x_start_position, info[3])

            line_num += 2
            self.window.addstr(line_num, self.x_start_position,
                               "Word: ")
            self.window.addstr(line_num, self.x_start_position + 7,
                               " ".join(info[1]), curses.A_BOLD)
            line_num += 2
            self.window.addstr(line_num, self.x_start_position,
                               "Letters used: " + info[5])
            line_num += 3
            self.window.addstr(line_num, self.x_start_position, info[4])

        elif name == "Pyarcade":
            line_num += 2
            self.window.addstr(line_num, self.x_start_position, info[1])

        return line_num

    def scroll_options(self, opts: List[str], info: List[str]) -> int:
        """
        Scroll Options for screen.
        Args:
            opts: List of options.
            info: Game information.

        Returns:
            Current scroll index (What option is being highlighted).
        """
        while True:
            key = self.window.getch()
            self.window.clear()

            if key == curses.KEY_UP and self.scroll_idx > 1:
                self.scroll_idx -= 1
            elif key == curses.KEY_DOWN and self.scroll_idx < len(opts) - 1:
                self.scroll_idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return self.scroll_idx
            self.display_options(opts, info)
            self.window.refresh()

    def user_input_window(self, message: str, user_input: str) -> str:
        """
        User input window.
        Args:
            message: Message to be initially displayed.
            user_input: User's input.

        Returns:
            User's input.
        """
        rect = 13
        self.window.clear()
        self.window.addstr(0, self.x_start_position, message)

        exit_message = "Press ENTER to submit"
        self.window.addstr(14, self.x_start_position, exit_message)

        if user_input == "":
            user_win = curses.newwin(1, rect, 10,
                                     self.x_start_position + 1)

            rectangle(self.window, 9, self.x_start_position,
                      11, self.x_start_position + rect + 1)

            self.window.refresh()

            user_input = textpad.Textbox(user_win, insert_mode=True).edit()

        return user_input

    def account_login_signup(self, is_sign_up) -> (str, str):
        """
        Account login signup / login.
        Args:
            is_sign_up: Determines if the user wants to sign up or login.

        Returns:
            Tuple containing username and password of user.
        """
        self.window.clear()

        if is_sign_up:
            self.window.addstr(2, self.x_start_position, "Account Signup")
            message = "Length 3 or more (Alphanumeric)"
            self.window.addstr(8, self.x_start_position, message)
            message = "Length 4 or more"
            self.window.addstr(15, self.x_start_position, message)
        else:
            self.window.addstr(2, self.x_start_position, "Account Login")

        self.window.addstr(4, self.x_start_position, "Username")
        rectangle(self.window, 5, self.x_start_position, 7,
                  self.x_start_position + 27)

        self.window.addstr(11, self.x_start_position, "Password")
        rectangle(self.window, 12, self.x_start_position, 14,
                  self.x_start_position + 27)

        message = "Press the 'ENTER KEY' to confirm input"
        self.window.addstr(21, self.x_start_position, message)

        self.window.refresh()

        user_win = curses.newwin(1, 26, 6, self.x_start_position + 1)
        username = textpad.Textbox(user_win, insert_mode=True).edit()

        pass_win = curses.newwin(1, 26, 13, self.x_start_position + 1)
        password = textpad.Textbox(pass_win, insert_mode=True).edit()

        return username, password

    def about_screen(self):
        """
        About Screen.
        """
        self.window.clear()

        self.window.addstr(2, self.x_start_position, "Created by:")
        self.window.addstr(6, self.x_start_position, "Brandon Kwintner",
                           curses.color_pair(2) | curses.A_BOLD)
        self.window.addstr(8, self.x_start_position, "Ryan Ziemski",
                           curses.color_pair(3) | curses.A_BOLD)
        self.window.addstr(10, self.x_start_position, "Nam Quach",
                           curses.color_pair(4) | curses.A_BOLD)
        self.window.addstr(12, self.x_start_position, "Andy Zhang",
                           curses.color_pair(5) | curses.A_BOLD)
        self.window.getch()

        self.window.refresh()

    def display_instruction(self, goal: str, rules: str, instruction: str):
        """ Display instructions for the game

        Args:
            goal (): Goal of the game
            rules (): Special conditions for the game
            instruction (): Description of the purpose of each command

        """
        self.window.clear()

        self.window.addstr(2, self.x_start_position, "Goal:")
        self.window.addstr(3, self.x_start_position, goal)

        self.window.addstr(5, self.x_start_position, "Rules:")

        num_line = 6
        for line in rules.split("\n"):
            self.window.addstr(num_line, self.x_start_position, line)
            num_line += 1

        num_line += 1
        self.window.addstr(num_line, self.x_start_position, "Instructions:")
        num_line += 1

        for line in instruction.split("\n"):
            self.window.addstr(num_line, self.x_start_position, line)
            num_line += 1

        self.window.getch()
        self.window.refresh()

    def display_leaderboard(self, game: str, board: [dict]):
        """ Display the stats of the players with the most wins for the
            desired game (top 25 players at most)

        Args:
            game (): Name of the desired game
            board (): Leaderboard for the desired game

        """
        self.window.clear()

        self.window.addstr(5, self.x_start_position, "Username")
        self.window.addstr(5, self.x_start_position + 30, "Games Won")
        self.window.addstr(5, self.x_start_position + 50, "Games Played")

        num = 1
        line = 6
        for user in board["board"]:
            if num > 25:
                break

            self.window.addstr(line, self.x_start_position - 3, str(num) +
                               ") " + user["user"])
            self.window.addstr(line, self.x_start_position + 30,
                               str(user["wins"]))
            self.window.addstr(line, self.x_start_position + 50,
                               str(user["total"]))
            line += 1
            num += 1

        if num == 1:
            self.window.addstr(2, self.x_start_position,
                               game + " Leaderboard")
        else:
            if num < 25:
                num -= 1

            self.window.addstr(2, self.x_start_position, game + " Leaderboard:"
                               + " Top " + str(num) + " Users")

        self.window.getch()
        self.window.refresh()




