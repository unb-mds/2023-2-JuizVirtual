from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.users.forms import CreateUserForm


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
