import requests
from enum import Enum


class ConnectRequest(Enum):
    _server_address = "http://pyarcade_proxy/api"
    SIGNUP = _server_address + "/users/signup/"
    LOGIN = _server_address + "/users/login/"
    GAMES_WIN = _server_address + "/game_wins/"
    GAMES_PLAYED = _server_address + "/games_played/"
    RESET_STAT = _server_address + "/stats/reset/"
    LEADERBOARD = _server_address + "/stats/board/"
    FRIEND = _server_address + "/friends/"


class Connections:
    @staticmethod
    def sign_up_account(username: str, password: str) -> dict:
        """
        Sign up new account.
        Args:
            username: username for account.
            password: password for account.

        Returns:
            Status code and either token or a message.
        """
        post_body = {
            "username": username,
            "password": password,
        }

        response = requests.post(ConnectRequest.SIGNUP.value, data=post_body)
        status_code = response.status_code
        response_body = response.json()

        if status_code == 200:
            return {
                "code": status_code,
                "access": response_body["access"]
            }

        return {
            "code": status_code,
            "message": response_body["message"]
        }

    @staticmethod
    def login_account(username: str, password: str) -> dict:
        """
        Login to an existing account.
        Args:
            username: username for account.
            password: password for account.

        Returns:
            Status code and either token or a message.
        """
        post_body = {
            "username": username,
            "password": password,
        }

        response = requests.post(ConnectRequest.LOGIN.value, data=post_body)
        status_code = response.status_code
        response_body = response.json()

        if status_code == 200:
            return {
                "code": status_code,
                "access": response_body["access"]
            }

        return {
            "code": status_code,
            "message": response_body["message"]
        }

    @staticmethod
    def get_num_wins(game: str, token: str) -> dict:
        """ Get the number of wins for the desired game.

        Args:
            game (): The desired game
            token (): The user's token for validation
        Returns:
            Status code and either number of wins or a message.

        """
        header = {
            "authorization": token
        }

        param = {
            "game": game,
        }

        response = requests.get(ConnectRequest.GAMES_WIN.value,
                                headers=header, params=param)
        status_code = response.status_code
        response_body = response.json()

        if status_code == 200:
            return {
                "code": status_code,
                "wins": response_body["wins"]
            }

        return {
            "code": status_code,
            "message": response_body["message"]
        }

    @staticmethod
    def update_num_wins(game: str, did_win: bool, token: str) -> dict:
        """ Get the number of wins for the desired game.

        Args:
            game (): The desired game
            did_win (): Did player win the round
            token (): The user's token for validation
        Returns:
            Status code and a message in failed.
        """
        header = {
            "authorization": token
        }

        post_body = {
            "game": game,
            "won": did_win,
        }

        response = requests.post(ConnectRequest.GAMES_WIN.value,
                                 headers=header, data=post_body)
        status_code = response.status_code
        response_body = response.json()

        if status_code == 200:
            return {
                "code": status_code,
            }

        return {
            "code": status_code,
            "message": response_body["message"]
        }

    @staticmethod
    def get_num_played(game: str, token: str) -> dict:
        """ Get the number of games played for the desired game.

        Args:
            game (): The desired game
            token (): The user's token for validation
        Returns:
            Status code and either number of games played or a message.
        """
        header = {
            "authorization": token
        }

        param = {
            "game": game,
        }

        response = requests.get(ConnectRequest.GAMES_PLAYED.value,
                                headers=header, params=param)
        status_code = response.status_code
        response_body = response.json()

        if status_code == 200:
            return {
                "code": status_code,
                "played": response_body["games_played"]
            }

        return {
            "code": status_code,
            "message": response_body["message"]
        }

    @staticmethod
    def reset_game_stat(game: str, token: str) -> dict:
        """ Resets the number of wins and games played

        Args:
            game (): The desired game
            token (): The user's token for validation
        Returns:
            Status code and a message if failed.
        """
        header = {
            "authorization": token
        }

        post_body = {
            "game": game,
        }

        response = requests.post(ConnectRequest.RESET_STAT.value,
                                 headers=header, data=post_body)
        status_code = response.status_code
        response_body = response.json()

        if status_code == 200:
            return {
                "code": status_code,
            }

        return {
            "code": status_code,
            "message": response_body["message"]
        }

    @staticmethod
    def get_leaderboard(game: str, token: str) -> dict:
        """ Get the leader board for the desired game

        Args:
            game (): The desired game
            token (): The user's token for validation
        Returns:
            Status code and either leaderboard or a message.
        """
        header = {
            "authorization": token
        }

        param = {
            "game": game,
        }

        response = requests.get(ConnectRequest.LEADERBOARD.value,
                                headers=header, params=param)
        status_code = response.status_code
        response_body = response.json()

        if status_code == 200:
            return {
                "code": status_code,
                "board": response_body["board"]
            }

        return {
            "code": status_code,
            "message": response_body["message"]
        }

    @staticmethod
    def get_friends(token: str) -> dict:
        """ Get the friend list of the user

        Args:
            token (): The user's token for validation
        Returns:
            Status code and either friend list or a message.
        """
        header = {
            "authorization": token
        }

        response = requests.get(ConnectRequest.FRIEND.value, headers=header)
        status_code = response.status_code
        response_body = response.json()

        if status_code == 200:
            return {
                "code": status_code,
                "friends": response_body["friends"]
            }

        return {
            "code": status_code,
            "message": response_body["message"]
        }

    @staticmethod
    def add_friend(username: str, token: str) -> dict:
        """ Sends a friend request to user/ Accepts the friend invite

        Args:
            username (): The username of the friend
            token (): The user's token for validation
        Returns:
            Status code and a message if failed.
        """
        header = {
            "authorization": token
        }

        post_body = {
            "user2": username
        }

        response = requests.post(ConnectRequest.FRIEND.value,
                                 headers=header, data=post_body)
        status_code = response.status_code
        response_body = response.json()

        if status_code == 200:
            return {
                "code": status_code,
            }

        return {
            "code": status_code,
            "message": response_body["message"]
        }
