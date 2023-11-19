from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.users.admin import UserAdmin
from apps.users.models import User


class UserModelTestCase(TestCase):
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
        list_display = UserAdmin.list_display
        expected = ("username", "email", "is_staff", "is_active")

        self.assertEqual(list_display, expected)

    def test_list_filter(self) -> None:
        list_filter = UserAdmin.list_filter
        expected = ("is_staff", "is_superuser", "is_active", "groups")

        self.assertEqual(list_filter, expected)

    def test_fieldsets(self) -> None:
        expected = [
            (
                _("Personal info"),
                {"fields": ("username", "email", "password")},
            ),
            (
                _("Permissions"),
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

        self.assertEqual(UserAdmin.fieldsets, expected)

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

    def test_email(self) -> None:
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        self.client.force_login(user)

        url = reverse("users:profile")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.email)
