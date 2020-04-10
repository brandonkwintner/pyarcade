from django.urls import path

from . import views

urlpatterns = [
    path('users/signup/', views.SignUpView.as_view(), name='signup'),
]