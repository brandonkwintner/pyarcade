from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class UserModel(models.Model):
    username = models.CharField(max_length=30, unique=True,
                                validators=[
                                    RegexValidator(r'^[a-zA-Z0-9]{3,}$'),
                                ])
    password = models.TextField(validators=[
        RegexValidator(r'.{4,}'),
    ])
    status_message = models.CharField(max_length=30, default="")
    mastermind_wins = models.IntegerField(default=0)
    blackjack_wins = models.IntegerField(default=0)
    war_wins = models.IntegerField(default=0)
    go_fish_wins = models.IntegerField(default=0)
    connect_wins = models.IntegerField(default=0)
