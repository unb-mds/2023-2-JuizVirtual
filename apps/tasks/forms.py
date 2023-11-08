from django.forms import CharField, Form


class TaskForm(Form):
    code = CharField(label="Source Code")
