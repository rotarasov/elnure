from django.urls import path
from elnure_users.views import GoogleLoginView

urlpatterns = [
    path(
        "authenticate/google-oauth2",
        GoogleLoginView.as_view(),
        name="authenticate-google-oauth2",
    )
]
