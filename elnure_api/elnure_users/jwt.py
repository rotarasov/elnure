from rest_framework_simplejwt.tokens import AccessToken

from elnure_users.models import User


def generate_access_token_for_user(user: User) -> str:
    access = AccessToken.for_user(user)
    return str(access)
