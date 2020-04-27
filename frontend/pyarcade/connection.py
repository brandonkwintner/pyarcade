import requests
from enum import Enum


class ConnectRequest(Enum):
    _server_address = "http://pyarcade_proxy/api"
    SIGNUP = _server_address + "/users/signup/"
    LOGIN = _server_address + "/users/login/"


class Connections:
    @staticmethod
    def sign_up_account(username: str, password: str) -> dict:
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

