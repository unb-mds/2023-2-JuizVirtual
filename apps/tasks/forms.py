from django import forms
from django.forms import CharField, Form


class TaskForm(Form):
    code = CharField(
        label="Source Code",
        widget=forms.Textarea(attrs={"style": "height: 300px;"}),
    )
