from django.urls import path

from .views.users_views import SignUpView
from .views.users_views import LogInView
from .views.stats_views import UserStatsView


urlpatterns = [
    path("users/signup/", SignUpView.as_view(), name="signup"),
    path("users/login/", LogInView.as_view(), name="login"),
    path("stats/", UserStatsView.as_view(), name="userstats"),
]