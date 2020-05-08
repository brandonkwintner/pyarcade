from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from game_ui.menu_options import Options
from game_ui.display_ui import Display
from pyarcade.connection import Connections


class BlackjackUI:
    """
    UI for Black Jack.
    """

    def __init__(self, window, user):
        self.window = window
        self.scroll_idx = 1
        self.user = user
        self.display = Display(self.window, self.scroll_idx, user)

    def blackjack_menu(self):
        """
        Black Jack menu screen.
        """
        menu = Options.GAME_STARTUP.value

        while True:
            self.display.display_options(menu, ["Blackjack Menu"])
            self.scroll_idx = self.display.scroll_options(menu,
                                                          ["Blackjack Menu"])

            if menu[self.scroll_idx] == "New Game":
                self.play_blackjack()

            elif menu[self.scroll_idx] == "Leaderboard":
                self.blackjack_leaderboard()

            elif menu[self.scroll_idx] == "Instructions":
                self.blackjack_instruction()

            elif self.scroll_idx == len(menu) - 1:
                break

            self.display.scroll_idx = 1

    def play_blackjack(self):
        """
        Black Jack game screen.
        """
        input_system = InputSystem(Game.BLACKJACK)

        wins = Connections.get_num_wins("blackjack",
                                        self.user["token"])["wins"]
        played = Connections.get_num_played("blackjack",
                                            self.user["token"])["played"]

        option_list = Options.BLACKJACK_OPTIONS.value
        status = input_system.get_last_guess()
        game_info = ["Blackjack", status[0], str(wins), "", str(played)]

        while True:
            game_info[1] = input_system.get_last_guess()[0]
            game_info[2] = str(wins)
            game_info[4] = str(played)

            self.display.display_options(option_list, game_info)
            self.scroll_idx = self.display.scroll_options(option_list,
                                                          game_info)

            if option_list[self.scroll_idx] == "Hit":
                input_system.take_input("hit")

                total = input_system.get_last_guess()[0][0].split(":")[1]
                if int(total) > 21:
                    input_system.take_input("stand")
                    option_list = Options.BLACKJACK_NEW_GAME.value
                    game_info[3] = "Show"
                    played += 1
                    option_list[0] = "Dealer Wins!"
                    Connections.update_num_wins("blackjack", False,
                                                self.user["token"])

            elif option_list[self.scroll_idx] == "Reset" or \
                    option_list[self.scroll_idx] == "New Game":
                input_system.take_input("reset")
                option_list = Options.BLACKJACK_OPTIONS.value
                game_info[3] = "Hidden"

            elif option_list[self.scroll_idx] == "Clear":
                input_system.take_input("clear")
                option_list = Options.BLACKJACK_OPTIONS.value
                game_info[3] = "Hidden"
                Connections.reset_game_stat("blackjack", self.user["token"])
                wins = 0
                played = 0

            elif option_list[self.scroll_idx] == "Stand":
                input_system.take_input("stand")
                option_list = Options.BLACKJACK_NEW_GAME.value
                game_info[3] = "Show"
                played += 1

                if input_system.get_last_guess()[1]:
                    option_list[0] = "Player Wins!"
                    Connections.update_num_wins("blackjack", True,
                                                self.user["token"])
                    wins += 1
                else:
                    option_list[0] = "Dealer Wins!"
                    Connections.update_num_wins("blackjack", False,
                                                self.user["token"])

            elif self.scroll_idx == len(option_list) - 1:
                break

            self.display.scroll_idx = 1

    def blackjack_instruction(self):
        """Instructions to play Blackjack
        """

        goal = "Try to get Card Hand as close as possible to 21"

        rules = "If player's Card Hand has a value greater then 21 " \
                "player loses. \nDealer wins if they have a card hand " \
                "value equal or greater then player.\nNumber of cards in " \
                "hand does not matter"

        instruct = "Hit: Adds a card to the players hand\n" \
                   "Stand: Ends the turn and calculate winner \n" \
                   "New Game: Play another round \n" \
                   "Reset: Restart the round \n" \
                   "Clear: Clear all game history \n" \
                   "Back: Goes back to game start menu"

        self.display.display_instruction(goal, rules, instruct)

    def blackjack_leaderboard(self):
        board = Connections.get_leaderboard("blackjack", self.user["token"])
        self.display.display_leaderboard("Blackjack", board)
