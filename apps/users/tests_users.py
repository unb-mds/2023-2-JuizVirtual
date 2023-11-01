from django.test import TestCase

from .models import User


class UserModelTestCase(TestCase):
    def test_user_fields(self) -> None:
        self.user_data = {
            "email": "test@example.com",
            "username": "user_test",
            "password": "passwordtest",
        }
        self.user = User.objects.create(**self.user_data)

    def test_username_field_is_email(self) -> None:
        self.assertEqual(User().USERNAME_FIELD, "email")

    def test_required_fields_include_username(self) -> None:
        self.assertIn("username", User().REQUIRED_FIELDS)


class UserManagerTastCase(TestCase):
    pass


class UserAdminTestCase(TestCase):
    pass
