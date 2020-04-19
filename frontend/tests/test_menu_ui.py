from game_ui.menu import Menu
from game_ui.menu_options import Options
import curses
import unittest


class MenuUITestCase(unittest.TestCase):
    @staticmethod
    def _move_up(menu, options, game_info):
        curses.ungetch(curses.KEY_UP)
        menu.scroll_options(options, game_info)

    @staticmethod
    def _move_down(menu, options, game_info):
        curses.ungetch(curses.KEY_DOWN)
        menu.scroll_options(options, game_info)

    def test_user_key_press_enter(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 2
        options = Options.MAIN_MENU_OPTIONS.value

        curses.ungetch(curses.KEY_ENTER)
        result = menu.scroll_options(options, [""])

        self.assertEqual(result, 2)
        menu.close_curse()

    def test_user_key_press_down(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 1
        options = Options.MAIN_MENU_OPTIONS.value
        MenuUITestCase._move_down(menu, options, [""])
        self.assertEqual(menu.scroll_idx, 2)

        MenuUITestCase._move_up(menu, options, [""])
        self.assertEqual(menu.scroll_idx, 1)
        menu.close_curse()

    def test_user_key_press_down_limit(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 1
        options = ['', 'mastermind', 'exit']

        MenuUITestCase._move_down(menu, options, [""])
        self.assertEqual(menu.scroll_idx, 2)

        MenuUITestCase._move_down(menu, options, [""])
        self.assertEqual(menu.scroll_idx, 2)

        menu.close_curse()

    def test_user_key_press_up(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 3
        options = Options.MAIN_MENU_OPTIONS.value

        MenuUITestCase._move_up(menu, options, [""])
        self.assertEqual(menu.scroll_idx, 2)

        menu.close_curse()

    def test_user_key_press_up_limit(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 2
        options = ['', 'mastermind', 'exit']

        MenuUITestCase._move_up(menu, options, [""])
        self.assertEqual(menu.scroll_idx, 1)

        MenuUITestCase._move_up(menu, options, [""])
        self.assertEqual(menu.scroll_idx, 1)

        menu.close_curse()

    def test_user_window_input_simple(self):
        menu = Menu()
        menu.testing = True
        result = menu.user_input_window("Message", "1234")
        self.assertEqual(result, "1234")

        menu.close_curse()

    def test_user_window_input_empty(self):
        menu = Menu()
        menu.testing = True

        result = menu.user_input_window("Message", "")
        self.assertEqual(result, "user")

        menu.close_curse()

    def test_main_to_mastermind(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 1
        result = menu.main_menu()
        self.assertEqual(result, Options.MASTERMIND_OPTIONS.value)
        menu.close_curse()

    def test_main_to_connect_four(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 2
        result = menu.main_menu()
        self.assertEqual(result, Options.CONNECT_FOUR_OPTIONS.value)
        menu.close_curse()

    def test_main_to_blackjack(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 3
        result = menu.main_menu()
        self.assertEqual(result, Options.BLACKJACK_OPTIONS.value)
        menu.close_curse()

    def test_main_to_war(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 4
        result = menu.main_menu()
        self.assertEqual(result, Options.WAR_OPTIONS.value)
        menu.close_curse()

    def test_main_to_go_fish(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 5
        result = menu.main_menu()
        self.assertEqual(result, Options.GO_FISH_OPTIONS.value)
        menu.close_curse()

    def test_main_to_options(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 6
        result = menu.main_menu()
        self.assertEqual(result, Options.FEATURE_OPTIONS.value)
        menu.close_curse()

    def test_new_game_menu(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 1
        result = menu.blackjack_menu()
        self.assertEqual(result, Options.BLACKJACK_OPTIONS.value)

        menu.scroll_idx = 2
        result = menu.blackjack_menu()
        self.assertEqual(result, Options.BLACKJACK_NEW_GAME.value)
        menu.close_curse()

    def test_display_game_info_mastermind(self):
        menu = Menu()
        menu.testing = True
        guess = "!: correct\n 2:incorrect\n"
        game_info = ["Mastermind", guess, str(4)]

        line_num = menu.display_game_info(game_info)
        self.assertEquals(line_num, 6)
        menu.close_curse()

    def test_display_game_info_connect_four(self):
        menu = Menu()
        menu.testing = True
        board = "---\n ---\n ---\n"
        game_info = ["Connect Four", board, str(4), "player X"]

        line_num = menu.display_game_info(game_info)
        self.assertEquals(line_num, 7)
        menu.close_curse()

    def test_display_blackjack_hidden(self):
        menu = Menu()
        menu.testing = True
        hands = ["player", "dealer"]
        game_info = ["Blackjack", hands, str(3), ""]

        line_num = menu.display_game_info(game_info)
        self.assertEquals(line_num, 6)
        menu.close_curse()

    def test_display_blackjack_show(self):
        menu = Menu()
        menu.testing = True
        hands = ["player", "dealer"]
        game_info = ["Blackjack", hands, str(3), "Show"]

        line_num = menu.display_game_info(game_info)
        self.assertEquals(line_num, 9)
        menu.close_curse()

    def test_display_war(self):
        menu = Menu()
        menu.testing = True
        hands = ("player", "dealer", 1, 1, 1, 1)
        game_info = ["War", hands, str(3)]

        line_num = menu.display_game_info(game_info)
        self.assertEquals(line_num, 9)
        menu.close_curse()

    def test_display_go_fish(self):
        menu = Menu()
        menu.testing = True
        hands = ("player", 1)
        game_info = ["Go Fish", hands, str(3), "a"]

        line_num = menu.display_game_info(game_info)
        self.assertEquals(line_num, 9)
        menu.close_curse()

    def test_mastermind_guess(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 1
        menu.mastermind_menu()

        self.assertEqual(menu.testing_function, "guess")
        menu.close_curse()

    def test_mastermind_reset(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 2
        menu.mastermind_menu()

        self.assertEqual(menu.testing_function, "reset")
        menu.close_curse()

    def test_mastermind_clear(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 3
        menu.mastermind_menu()

        self.assertEqual(menu.testing_function, "clear")
        menu.close_curse()

    def test_mastermind_back(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 4
        menu.mastermind_menu()

        self.assertEqual(menu.scroll_idx, 1)
        menu.close_curse()

    def test_connect4_choose(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 1
        menu.connect_four_menu()

        self.assertEqual(menu.testing_function, "column")
        menu.close_curse()

    def test_connect4_reset(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 2
        menu.connect_four_menu()

        self.assertEqual(menu.testing_function, "reset")
        menu.close_curse()

    def test_connect4_clear(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 3
        menu.connect_four_menu()

        self.assertEqual(menu.testing_function, "clear")
        menu.close_curse()

    def test_connect4_back(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 4
        menu.connect_four_menu()

        self.assertEqual(menu.scroll_idx, 1)
        menu.close_curse()

    def test_blackjack_hit(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 1
        menu.blackjack_menu()

        self.assertEqual(menu.testing_function, "hit")
        menu.close_curse()

    def test_blackjack_stand(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 2
        menu.blackjack_menu()

        self.assertEqual(menu.testing_function, "stand")
        menu.close_curse()

    def test_blackjack_reset(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 3
        menu.blackjack_menu()

        self.assertEqual(menu.testing_function, "reset")
        menu.close_curse()

    def test_blackjack_clear(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 4
        menu.blackjack_menu()

        self.assertEqual(menu.testing_function, "clear")
        menu.close_curse()

    def test_blackjack_back(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 5
        menu.blackjack_menu()

        self.assertEqual(menu.scroll_idx, 1)
        menu.close_curse()

    def test_main_menu_exit(self):
        menu = Menu()
        menu.testing = True
        options = Options.MAIN_MENU_OPTIONS.value
        curses.ungetch(curses.KEY_ENTER)
        curses.ungetch(curses.KEY_ENTER)

        MenuUITestCase._move_down(menu, options, [""])
        MenuUITestCase._move_down(menu, options, [""])
        MenuUITestCase._move_down(menu, options, [""])
        MenuUITestCase._move_down(menu, options, [""])
        MenuUITestCase._move_down(menu, options, [""])
        MenuUITestCase._move_down(menu, options, [""])
        self.assertEqual(menu.scroll_idx, 7)

        result = menu.main_menu()
        self.assertEqual(menu.scroll_idx, 7)

        self.assertEquals(result, Options.MAIN_MENU_OPTIONS.value)
        menu.close_curse()

    def test_war_flip_card(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 1
        menu.war_menu()

        self.assertEqual(menu.testing_function, "flip card")
        menu.close_curse()

    def test_war_reset(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 2
        menu.war_menu()

        self.assertEqual(menu.testing_function, "reset")
        menu.close_curse()

    def test_war_clear(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 3
        menu.war_menu()

        self.assertEqual(menu.testing_function, "clear")
        menu.close_curse()

    def test_war_back(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 4
        menu.go_fish_menu()

        self.assertEqual(menu.scroll_idx, 1)
        menu.close_curse()

    def test_go_fish_guess(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 1
        menu.go_fish_menu()

        self.assertEqual(menu.testing_function, "guess")
        menu.close_curse()

    def test_go_fish_reset(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 2
        menu.go_fish_menu()

        self.assertEqual(menu.testing_function, "reset")
        menu.close_curse()

    def test_go_fish_clear(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 3
        menu.go_fish_menu()

        self.assertEqual(menu.testing_function, "clear")
        menu.close_curse()

    def test_go_fish_back(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 4
        menu.go_fish_menu()

        self.assertEqual(menu.scroll_idx, 1)
        menu.close_curse()

    def test_go_options_back(self):
        menu = Menu()
        menu.testing = True
        menu.scroll_idx = 2
        menu.options_menu()

        self.assertEqual(menu.scroll_idx, 1)
        menu.close_curse()
