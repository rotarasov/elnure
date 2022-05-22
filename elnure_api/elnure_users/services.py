"""
Reference: https://www.hacksoft.io/blog/google-oauth2-with-django-react-part-2
"""
import logging
import functools

from django.conf import settings
from rest_framework.exceptions import ValidationError, AuthenticationFailed

import requests

logger = logging.getLogger(__name__)


def wrap_request_errors(api_caller):
    @functools.wraps(api_caller)
    def inner(*args, **kwargs):
        try:
            return api_caller(*args, **kwargs)

        except requests.RequestException as exc:
            logger.error("Request exception: %s", str(exc))
            raise AuthenticationFailed(detail="Google API is unavailable", code=503)

    return inner


class GoogleOAuth2Client:
    ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    TOKEN_INFO_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def __init__(
        self,
        client_id=settings.GOOGLE_OAUTH2_CLIENT_ID,
        secret=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
    ) -> None:
        self.client_id = client_id
        self.secret = secret

    @wrap_request_errors
    def get_access_token(self, code: str, redirect_uri: str) -> str:
        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
        data = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        response = requests.post(self.ACCESS_TOKEN_OBTAIN_URL, data=data)

        if not response.ok:
            logger.error("Google OAuth2 error: %s", response.json())
            raise AuthenticationFailed(
                "Failed to obtain access token from Google.", code=500
            )

        access_token = response.json()["access_token"]

        return access_token

    @wrap_request_errors
    def get_user_info(self, access_token: str) -> dict:
        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server?hl=en#callinganapi
        response = requests.get(
            self.USER_INFO_URL, params={"access_token": access_token}
        )

        if not response.ok:
            logger.error("Error during fetching user info: %s", response.json)
            raise AuthenticationFailed(detail="Failed to fetch user info.", code=500)

        return response.json()
