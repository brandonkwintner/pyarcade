from pyarcade.input_system import InputSystem
from pyarcade.game_option import Game
from game_ui.menu_options import Options
from game_ui.display_ui import Display
from pyarcade.connection import Connections


class GoFishUI:
    """
    UI for Go Fish.
    """
    def __init__(self, window, user):
        self.window = window
        self.scroll_idx = 1
        self.display = Display(self.window, self.scroll_idx, user)
        self.user = user

    def go_fish_menu(self):
        """
        Go Fish menu screen.
        """
        menu = Options.GAME_STARTUP.value

        while True:
            self.display.display_options(menu, ["Go Fish Menu"])
            self.scroll_idx = self.display.scroll_options(menu,
                                                          ["Go Fish Menu"])

            if menu[self.scroll_idx] == "New Game":
                self.play_go_fish()

            elif menu[self.scroll_idx] == "Leaderboard":
                self.go_fish_leaderboard()

            elif menu[self.scroll_idx] == "Instructions":
                self.go_fish_instruction()

            elif self.scroll_idx == len(menu) - 1:
                break

            self.display.scroll_idx = 1

    def play_go_fish(self):
        """
        Go Fish game screen.
        """
        input_system = InputSystem(Game.GO_FISH)
        wins = Connections.get_num_wins("go fish",
                                        self.user["token"])["wins"]
        played = Connections.get_num_played("go fish",
                                            self.user["token"])["played"]
        option_list = Options.GO_FISH_OPTIONS.value
        status = input_system.get_last_guess()
        game_info = ["Go Fish", status, str(wins), "", str(played)]

        while True:
            status = input_system.get_last_guess()
            game_info[1] = status
            game_info[2] = str(wins)
            game_info[4] = str(played)

            self.display.display_options(option_list, game_info)
            self.scroll_idx = self.display.scroll_options(option_list,
                                                          game_info)

            if option_list[self.scroll_idx] == "Take Guess":
                message = "Please enter Card Rank (Full Name or Number)"
                guess = self.display.user_input_window(message, "")

                if not guess == "":
                    input_result = input_system.take_input(guess.strip())

                    if not input_result[1]:
                        game_info[3] = "Invalid input: Try Again"
                    else:
                        info = input_system.get_last_guess()

                        if input_result[0]:
                            option_list = Options.GO_FISH_NEW_GAME.value
                            game_info[3] = ""
                            played += 1

                            if info[2] == 1:
                                option_list[0] = "You Win!"
                                Connections.update_num_wins("go fish", True,
                                                            self.user["token"])
                                wins += 1
                            else:
                                option_list[0] = "You Lose!"
                                Connections.update_num_wins("go fish", False,
                                                            self.user["token"])
                        else:
                            if info[1]:
                                game_info[3] = "Go Fish"
                            else:
                                game_info[3] = "Correct Guess"

            elif option_list[self.scroll_idx] == "Reset" or \
                    option_list[self.scroll_idx] == "New Game":
                input_system.take_input("reset")
                option_list = Options.GO_FISH_OPTIONS.value

            elif option_list[self.scroll_idx] == "Clear":
                option_list = Options.GO_FISH_OPTIONS.value
                input_system.take_input("clear")
                Connections.reset_game_stat("go fish", self.user["token"])
                wins = 0
                played = 0

            elif self.scroll_idx == len(option_list) - 1:
                break

            self.display.scroll_idx = 1

    def go_fish_instruction(self):
        """Instructions to play Go Fish
        """

        goal = "Try to get 4 cards of the same rank"

        rules = "Enter any card rank, even if the card is not in your " \
                "hand.\nIf the NPC has any card of the declared" \
                " rank it will all be added to your hand.\n" \
                "Else a new card will be drawn to your hand."

        instruct = "Take Guess: Declare the desired card, either by " \
                   "'2, 3,..., 10' or 'Ace, Two,..., King'\n" \
                   "New Game: Play another round \n" \
                   "Reset: Restart the round \n" \
                   "Clear: Clear all game history \n" \
                   "Back: Goes back to game start menu"

        self.display.display_instruction(goal, rules, instruct)

    def go_fish_leaderboard(self):
        board = Connections.get_leaderboard("go fish", self.user["token"])
        self.display.display_leaderboard("Go Fish", board)
