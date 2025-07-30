from django.urls import path
from api.v1.auth.views import RegisterView, LoginView, UserDetailsView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("user-details/", UserDetailsView.as_view(), name="user-details"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
