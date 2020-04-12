import requests
from enum import Enum


class ConnectRequest(Enum):
    _server_address = "http://pyarcade_proxy"
    SIGNUP = _server_address + "/users/signup/"


class Connections:
    @staticmethod
    def sign_up_account(username: str, password: str) -> dict:
        post_body = {
            "username": username,
            "password": password,
        }

        try:
            response = requests.post(ConnectRequest.SIGNUP.value, data=post_body)
            status_code = response.status_code
            response_body = response.json()
        except requests.exceptions.ConnectionError:
            status_code = 400
            response_body = {"message": ""}

        return {
            "code": status_code,
            "message": response_body["message"]
        }

