from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import EmailField, CharField, BooleanField

from core.models import TimestampedModel
from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    """Represents an user."""

    email = EmailField(db_index=True, max_length=256, unique=True)
    username = CharField(db_index=True, max_length=128, unique=True)

    # When a user no longer wishes to use our platform, they may try to
    # delete there account. That's a problem for us because the data we
    # collect is valuable to us and we don't want to delete it. To solve
    # this problem, we will simply offer users a way to deactivate their
    # account instead of letting them delete it. That way they won't
    # show up on the site anymore, but we can still analyze the data.
    is_active = BooleanField(default=True)

    # Designates whether the user can log into the admin site.
    is_staff = BooleanField(default=False)

    # Telling Django that the email field should be used for
    # authentication instead of the username field.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        db_table = "users"
