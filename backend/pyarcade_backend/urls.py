from django.urls import path

from .views.users_views import SignUpView
from .views.users_views import LogInView
from .views.stats_views import ResetUserStatsView
from .views.stats_views import ScoreboardView
from .views.games_played_views import GamesPlayedView
from .views.game_wins_views import GameWinsView
from .views.status_views import StatusView
from .views.friendship_views import FriendshipView

urlpatterns = [
    path("users/signup/", SignUpView.as_view(), name="signup"),
    path("users/login/", LogInView.as_view(), name="login"),
    path("stats/reset/", ResetUserStatsView.as_view(), name="reset_stats"),
    path("stats/board/", ScoreboardView.as_view(), name="scoreboard"),
    path("games_played/", GamesPlayedView.as_view(),
         name="games_played"),
    path("game_wins/", GameWinsView.as_view(), name="game_wins"),
    path("status/", StatusView.as_view(), name="status"),
    path("friends/", FriendshipView.as_view(), name="friends")
]
