from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.users.forms import CreateUserForm


class RegisterView(View):
    template_name = "registration/register.html"

    def get(self, request: HttpRequest) -> HttpResponse | None:
        form = CreateUserForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse | None:
        form = CreateUserForm(self.request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

        return render(request, self.template_name, {"form": form})
