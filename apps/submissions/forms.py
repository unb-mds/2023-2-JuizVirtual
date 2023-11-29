from django.forms import CharField, Form, Textarea


class SubmissionForm(Form):
    code = CharField(
        label="Source Code",
        required=True,
        min_length=15,
        widget=Textarea(attrs={"rows": 12, "style": "width: 100%;"}),
    )
