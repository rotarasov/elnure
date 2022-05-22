from elnure_users.models import User


class Storage:
    @staticmethod
    def get_or_create_user(profile: dict) -> tuple[User, bool]:
        created = False
        try:
            user = User.unfiltered.get(email=profile["email"])
        except User.DoesNotExist:
            created = True
            user = User.objects.create_user(**profile)

        assert user.first_name == profile.get("first_name")
        assert user.last_name == profile.get("last_name")

        return user, created
