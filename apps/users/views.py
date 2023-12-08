from typing import TYPE_CHECKING

from django.contrib.auth import login
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from apps.users.forms import CreateUserForm
from apps.users.models import User

if TYPE_CHECKING:
    RankingViewBase = ListView[User]
else:
    RankingViewBase = ListView


class RegisterView(View):
    template_name = "registration/register.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = CreateUserForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CreateUserForm(self.request.POST)
        if form.is_valid():
            user = form.save()

            # Since we have multiple authentication backends, we need to
            # specify which one we want to use. In this case, we want to
            # use the :class:`ModelBackend`, which is the default one.
            login(request, user, "django.contrib.auth.backends.ModelBackend")
            return redirect("home")

        return render(request, self.template_name, {"form": form})


class ProfileView(View):
    template_name = "users/profile.html"

    def get(self, request: HttpRequest, *, username: str) -> HttpResponse:
        user = get_object_or_404(User, username=username)
        return render(request, self.template_name, {"user": user})


class RankingView(RankingViewBase):
    model = User
    template_name = "ranking/list.html"
    context_object_name = "ranking"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[User]:
        return User._default_manager.all().order_by("-score")
