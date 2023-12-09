from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.users.admin import UserAdmin
from apps.users.forms import CreateUserForm
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
        expected = (
            "username",
            "email",
            "is_staff",
            "is_active",
            "score",
        )

        self.assertEqual(list_display, expected)

    def test_list_filter(self) -> None:
        list_filter = UserAdmin.list_filter
        expected = ("is_staff", "is_superuser", "is_active", "groups")

        self.assertEqual(list_filter, expected)

    def test_fieldsets(self) -> None:
        expected = [
            (
                _("Personal info"),
                {"fields": ("username", "email", "password", "score")},
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
                    "fields": (
                        "username",
                        "email",
                        "password1",
                        "password2",
                        "score",
                    ),
                },
            ),
        )

        self.assertEqual(UserAdmin.add_fieldsets, expected_add_fieldsets)


class RegisterViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse("users:register")
        self.valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
        }

    def test_register_view_get(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertIsInstance(response.context["form"], CreateUserForm)

    def test_register_view_post_invalid_data(self) -> None:
        response = self.client.post(self.url, data={}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertContains(response, "This field is required.")

    def test_post_valid_data(self) -> None:
        response = self.client.post(
            self.url, data=self.valid_data, follow=True
        )

        user = User.objects.get(username=self.valid_data["username"])

        self.assertRedirects(response, reverse("home"))
        self.assertIsNotNone(user)
        self.client.force_login(user)
        self.assertTrue(self.client.session["_auth_user_id"])

    def test_email(self) -> None:
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        self.client.force_login(user)

        url = reverse("users:profile", args=[user.username])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.email)


class RankingListViewtest(TestCase):
    def setUp(self) -> None:
        self.user = User._default_manager.create(
            username="testuser1",
            email="testuser@example1",
            password="testpassword1",
            score=100,
        )
        self.user = User._default_manager.create(
            username="testuser2",
            email="testuser@example2",
            password="testpassword2",
            score=90,
        )

    def test_ranking_list_view(self) -> None:
        self.client.login(email="testuser@example", password="testpassword")

        url = reverse("users:ranking")
        response = self.client.get(url)
        ranking_order = [user.username for user in response.context["ranking"]]
        expected_order = ["testuser1", "testuser2"]

        self.assertEqual(response.status_code, 200)
        self.assertIn("ranking", response.context)
        self.assertIn(self.user, response.context["ranking"])
        self.assertEqual(ranking_order, expected_order)
