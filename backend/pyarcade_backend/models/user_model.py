from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class UserModel(models.Model):
    MIN_PASSWORD_LEN = 4
    MIN_USERNAME_LEN = 3
    MAX_USERNAME_LEN = 30
    MAX_STATUS_MSG_LEN = 30
    USERNAME_REGEX = f"^[a-zA-Z0-9]{{{MIN_USERNAME_LEN},}}$"
    PASSWORD_REGEX = f".{{{MIN_PASSWORD_LEN},}}"

    username = models.CharField(max_length=MAX_USERNAME_LEN,
                                unique=True,
                                validators=[
                                    RegexValidator(USERNAME_REGEX),
                                ])
    password = models.TextField(validators=[
        RegexValidator(PASSWORD_REGEX),
    ])
    status_message = models.CharField(max_length=MAX_STATUS_MSG_LEN,
                                      default="",
                                      blank=True)
    mastermind_wins = models.IntegerField(default=0)
    blackjack_wins = models.IntegerField(default=0)
    war_wins = models.IntegerField(default=0)
    go_fish_wins = models.IntegerField(default=0)
    connect_wins = models.IntegerField(default=0)
