from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from game_ui.menu_options import Options
from game_ui.display_ui import Display
from pyarcade.connection import Connections


class Connect4UI:
    """
    UI for Connect 4.
    """
    def __init__(self, window, user):
        self.window = window
        self.scroll_idx = 1
        self.display = Display(self.window, self.scroll_idx, user)
        self.user = user

    def connect_four_menu(self):
        """
        Connect 4 menu screen.
        """
        menu = Options.GAME_STARTUP.value

        while True:
            self.display.display_options(menu, ["Connect 4 Menu"])
            self.scroll_idx = self.display.scroll_options(menu,
                                                          ["Connect 4 Menu"])

            if menu[self.scroll_idx] == "New Game":
                self.play_connect_four()

            elif menu[self.scroll_idx] == "Leaderboard":
                self.connect4_leaderboard()

            elif menu[self.scroll_idx] == "Instructions":
                self.connect4_instruction()

            elif self.scroll_idx == len(menu) - 1:
                break

            self.display.scroll_idx = 1

    def play_connect_four(self):
        """
        Connect 4 game screen.
        """
        option_list = Options.CONNECT_FOUR_OPTIONS.value
        input_system = InputSystem(Game.CONNECT4)
        wins = Connections.get_num_wins("connect4",
                                        self.user["token"])["wins"]
        played = Connections.get_num_played("connect4",
                                            self.user["token"])["played"]

        game_info = ["Connect Four", input_system.get_last_guess(), str(wins),
                     str(played)]

        while True:
            game_info[1] = input_system.get_last_guess()
            game_info[2] = str(wins)
            game_info[3] = str(played)

            self.display.display_options(option_list, game_info)
            self.scroll_idx = self.display.scroll_options(option_list,
                                                          game_info)

            if option_list[self.scroll_idx] == "Enter Column":
                message = "Please enter a digits between 1 to 7"
                guess = self.display.user_input_window(message, "")

                if input_system.take_input(guess)[0]:
                    winner = input_system.get_last_guess()
                    option_list = Options.CONNECT_FOUR_NEW_GAME.value
                    played += 1

                    if winner[1] == 'Player':
                        option_list[0] = 'Player X Wins!'
                        wins += 1
                        Connections.update_num_wins("connect4", True,
                                                    self.user["token"])
                    elif winner[1] == 'NPC':
                        option_list[0] = 'Player O Wins!'
                        Connections.update_num_wins("connect4", False,
                                                    self.user["token"])

            elif option_list[self.scroll_idx] == "Reset" or \
                    option_list[self.scroll_idx] == "New Game":
                input_system.take_input("reset")
                option_list = Options.CONNECT_FOUR_OPTIONS.value

            elif option_list[self.scroll_idx] == "Clear":
                option_list = Options.CONNECT_FOUR_OPTIONS.value
                input_system.take_input("clear")
                Connections.reset_game_stat("connect4", self.user["token"])
                wins = 0
                played = 0

            elif self.scroll_idx == len(option_list) - 1:
                break

            self.display.scroll_idx = 1

    def connect4_instruction(self):
        """Instructions to play Connect 4
        """

        goal = "Try to get 4 X in a row"
        rules = "First to get 4 in a row wins\n" \
                "It can be connect horizontally XXXX, vertically X," \
                " or diagonally X\n                                         " \
                "       X               X\n                                 " \
                "               X              X\n                          " \
                "                      X             X"
        instruct = "Enter Column: Puts piece in the desired columns 1 to 7\n" \
                   "New Game: Play another round \n" \
                   "Reset: Restart the round \n" \
                   "Clear: Clear all game history \n" \
                   "Back: Goes back to game start menu"

        self.display.display_instruction(goal, rules, instruct)

    def connect4_leaderboard(self):
        board = Connections.get_leaderboard("connect4", self.user["token"])
        self.display.display_leaderboard("Connect 4", board)
