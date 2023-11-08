from django.forms import CharField, Form


class ProblemForm(Form):
    code = CharField(label="Source Code")
