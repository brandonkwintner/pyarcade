from django.urls import path

from .views.users_views import SignUpView

urlpatterns = [
    path('users/signup/', SignUpView.as_view(), name='signup'),
]