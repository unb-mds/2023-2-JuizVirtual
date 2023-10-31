from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User


class CreateUserForm(UserCreationForm[User]):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
