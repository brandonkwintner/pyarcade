from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from game_ui.menu_options import Options
from game_ui.display_ui import Display
from pyarcade.connection import Connections


class WarUI:
    """
    UI for War.
    """
    def __init__(self, window, user):
        self.window = window
        self.scroll_idx = 1
        self.display = Display(self.window, self.scroll_idx, user)
        self.user = user

    def war_menu(self):
        """
        War menu screen
        """
        menu = Options.GAME_STARTUP.value

        while True:
            self.display.display_options(menu, ["War Menu"])
            self.scroll_idx = self.display.scroll_options(menu,
                                                          ["War Menu"])

            if menu[self.scroll_idx] == "New Game":
                self.play_war()

            elif self.scroll_idx == len(menu) - 1:
                break

            elif menu[self.scroll_idx] == "Leaderboard":
                self.war_leaderboard()

            elif menu[self.scroll_idx] == "Instructions":
                self.war_instruction()

            self.display.scroll_idx = 1

    def play_war(self):
        """
        War game screen.
        """
        input_system = InputSystem(Game.WAR)

        wins = Connections.get_num_wins("war", self.user["token"])["wins"]
        played = Connections.get_num_played("war",
                                            self.user["token"])["played"]

        option_list = Options.WAR_OPTIONS.value
        status = input_system.get_last_guess()
        game_info = ["War", status, str(wins), str(played)]

        while True:
            status = input_system.get_last_guess()
            game_info[1] = status
            game_info[2] = str(wins)
            game_info[3] = str(played)

            self.display.display_options(option_list, game_info)
            self.scroll_idx = self.display.scroll_options(option_list,
                                                          game_info)

            if option_list[self.scroll_idx] == "Flip Card":
                input_system.take_input("flip card")
                info = input_system.get_last_guess()

                if info[4]:
                    option_list = Options.WAR_NEW_GAME.value
                    played += 1

                    if info[5] == 2:
                        option_list[0] = "You Lose!"
                        Connections.update_num_wins("war", False,
                                                    self.user["token"])
                    else:
                        option_list[0] = "You Win!"
                        Connections.update_num_wins("war", True,
                                                    self.user["token"])
                        wins += 1

            elif option_list[self.scroll_idx] == "Reset" or \
                    option_list[self.scroll_idx] == "New Game":
                input_system.take_input("reset")
                option_list = Options.WAR_OPTIONS.value

            elif option_list[self.scroll_idx] == "Clear":
                option_list = Options.WAR_OPTIONS.value
                input_system.take_input("clear")
                Connections.reset_game_stat("war", self.user["token"])
                wins = 0
                played = 0

            elif self.scroll_idx == len(option_list) - 1:
                break

            self.display.scroll_idx = 1

    def war_instruction(self):
        """Instructions to play War
        """

        goal = "Try to win over all of the opponents cards"

        rules = "The number of cards in each hand as well as the " \
                "cards played are displayed.\nBoth cards are added to the" \
                " side that has the higher Rank card.\n" \
                "If both cards have the same rank, 4 additional cards are " \
                "removed from each side. \nThe last card is used to " \
                "determine the winner and gets all 10 cards.\n" \
                "If both cards have the same rank, but a side has less " \
                "then 4 cards in their hand they lose"

        instruct = "Take Guess: Enter the guess sequence" \
                   "New Game: Play another round \n" \
                   "Reset: Restart the round \n" \
                   "Clear: Clear all game history \n" \
                   "Back: Goes back to game start menu"

        self.display.display_instruction(goal, rules, instruct)

    def war_leaderboard(self):
        board = Connections.get_leaderboard("war", self.user["token"])
        self.display.display_leaderboard("War", board)
