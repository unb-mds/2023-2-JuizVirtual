from django.test import TestCase

from .admin import UserAdmin
from .models import User


class UserModelTestCase(TestCase):
    def test_user_fields(self) -> None:
        self.user_data = {
            "email": "test@example.com",
            "username": "user_test",
            "password": "testpassword",
        }
        self.user = User.objects.create(**self.user_data)

    def test_username_field_is_email(self) -> None:
        self.assertEqual(User().USERNAME_FIELD, "email")

    def test_required_fields_include_username(self) -> None:
        self.assertIn("username", User().REQUIRED_FIELDS)


class UserManagerTestCase(TestCase):
    def test_create_user(self) -> None:
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self) -> None:
        superuser = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="adminpassword",
        )
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertEqual(superuser.username, "adminuser")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class UserAdminTestCase(TestCase):
    def test_list_display(self) -> None:
        self.assertEqual(
            UserAdmin.list_display,
            ("username", "email", "is_staff", "is_active"),
        )

    def test_fieldsets(self) -> None:
        expected_fieldsets = [
            (("Personal info"), {"fields": ("username", "email", "password")}),
            (
                ("Permissions"),
                {
                    "fields": (
                        "user_permissions",
                        "groups",
                        "is_active",
                        "is_staff",
                        "is_superuser",
                    )
                },
            ),
        ]
        self.assertEqual(UserAdmin.fieldsets, expected_fieldsets)

    def test_add_fieldsets(self) -> None:
        expected_add_fieldsets = (
            (
                None,
                {
                    "classes": ("wide",),
                    "fields": ("username", "email", "password1", "password2"),
                },
            ),
        )
        self.assertEqual(UserAdmin.add_fieldsets, expected_add_fieldsets)
