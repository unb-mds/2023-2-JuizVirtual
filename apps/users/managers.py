from typing import TYPE_CHECKING, Any

from django.contrib.auth.models import BaseUserManager

if TYPE_CHECKING:
    from apps.users.models import User
else:
    User = Any


class UserManager(BaseUserManager[User]):
    def _create_user(
        self,
        username: str,
        email: str,
        password: str,
        **fields: bool,
    ) -> User:
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **fields)

        user.set_password(password)
        user.save()

        return user

    def create_user(
        self, username: str, email: str, password: str, **fields: bool
    ) -> User:
        fields.setdefault("is_staff", False)
        fields.setdefault("is_superuser", False)

        return self._create_user(username, email, password, **fields)

    def create_superuser(
        self, username: str, email: str, password: str, **fields: bool
    ) -> User:
        fields["is_staff"] = True
        fields["is_superuser"] = True

        return self._create_user(username, email, password, **fields)
