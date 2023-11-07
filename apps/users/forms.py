from typing import TYPE_CHECKING

from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User

if TYPE_CHECKING:
    BaseUserCreationForm = UserCreationForm[User]
else:
    BaseUserCreationForm = UserCreationForm


class CreateUserForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
