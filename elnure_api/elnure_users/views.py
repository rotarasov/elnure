from urllib.parse import urlencode

from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.exceptions import NotFound, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from elnure_users.services import GoogleOAuth2Client
from elnure_users.storage import Storage
from elnure_users.serializers import (
    RequestSerializer,
    UserSerializer,
    LoginResponseSerializer,
)
from elnure_users.jwt import generate_access_token_for_user


class GoogleLoginView(APIView):
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"

    FRONTEND_LOGIN_URL = f"{settings.BASE_FRONTEND_URL}/login"
    BACKEND_DOMAIN = f"{settings.BASE_BACKEND_URL}"

    permission_classes = []

    def get(self, request, *args, **kwargs):
        if not request.query_params:
            # Absence of query params implies effort to authenticate from DRF in browser
            # TODO: Make correct behavior for DRF in browser
            redirect(self.GOOGLE_AUTH_URL)

        request_serializer = RequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)

        validated_data = request_serializer.validated_data
        code = validated_data.get("code")
        error = validated_data.get("error")

        if error or not code:
            params = urlencode({"error": error})
            return redirect(f"{self.FRONTEND_LOGIN_URL}?{params}")

        google_client = GoogleOAuth2Client()

        google_access_token = self.obtain_google_access_token(google_client, code)

        profile_data = self.obtain_google_user_info(google_client, google_access_token)

        user, _ = Storage.get_or_create_user(profile_data)

        if not user.active:
            raise NotFound("No active user with this data")

        if settings.DEBUG:
            # Login in to skip adding auth header every time on browsable API
            auth.login(request, user)

        jwt_access_token = generate_access_token_for_user(user)

        user_serializer = UserSerializer(user)
        response_serializer = LoginResponseSerializer(
            data={
                "user": user_serializer.data,
                "access_token": jwt_access_token,
            }
        )

        return Response(response_serializer.initial_data, status=200)

    def obtain_google_access_token(self, client, code):
        auth_endpoint = reverse("authenticate-google-oauth2")
        redirect_uri = f"{self.BACKEND_DOMAIN}{auth_endpoint}"

        access_token = client.get_access_token(code=code, redirect_uri=redirect_uri)

        return access_token

    def obtain_google_user_info(self, client, access_token):
        user_data = client.get_user_info(access_token=access_token)

        if not (
            user_data.get("given_name", None) and user_data.get("family_name", None)
        ):
            raise AuthenticationFailed(
                "Profile data should contain given_name and family_name.", code=500
            )

        return {
            "email": user_data["email"],
            "first_name": user_data.get("given_name", None),
            "last_name": user_data.get("family_name", None),
        }
