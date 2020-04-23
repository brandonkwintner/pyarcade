from django.urls import path

from .views.users_views import SignUpView
from .views.users_views import LogInView
from .views.stats_views import UserStatsView
from .views.games_played_views import GamesPlayedView

urlpatterns = [
    path("users/signup/", SignUpView.as_view(), name="signup"),
    path("users/login/", LogInView.as_view(), name="login"),
    path("stats/", UserStatsView.as_view(), name="userstats"),
    path("games_played/", GamesPlayedView.as_view(),
         name="gamesplayedall")
    # path("games_played?game={game}/", GamesPlayedView.as_view(),
    #     name="gamesplayed"),
]
