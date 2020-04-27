from django.urls import path

from .views.users_views import SignUpView
from .views.users_views import LogInView
from .views.stats_views import ResetUserStatsView
from .views.games_played_views import GamesPlayedView
from .views.game_wins_views import GameWinsView

urlpatterns = [
    path("users/signup/", SignUpView.as_view(), name="signup"),
    path("users/login/", LogInView.as_view(), name="login"),
    path("stats/reset/", ResetUserStatsView.as_view(), name="reset_stats"),
    path("games_played/", GamesPlayedView.as_view(),
         name="gamesplayed"),
    path("game_wins/", GameWinsView.as_view(), name="game_wins")
]
