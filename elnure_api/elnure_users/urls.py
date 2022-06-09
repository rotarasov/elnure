from django.urls import path
from elnure_users.views import GoogleLoginAPIView, LogoutAPIView

urlpatterns = [
    path(
        "authenticate/google-oauth2",
        GoogleLoginAPIView.as_view(),
        name="authenticate-google-oauth2",
    ),
    path("logoout", LogoutAPIView.as_view(), name="logout"),
]
