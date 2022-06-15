from django.urls import path
from elnure_users.views import (
    GoogleLoginAPIView,
    PlainLoginAPIView,
    LogoutAPIView,
    MeAPIView,
)

urlpatterns = [
    path(
        "authenticate/google-oauth2",
        GoogleLoginAPIView.as_view(),
        name="authenticate-google-oauth2",
    ),
    path("authenticate", PlainLoginAPIView.as_view(), name="authenticate"),
    path("logout", LogoutAPIView.as_view(), name="logout"),
    path("me", MeAPIView.as_view(), name="me"),
]
