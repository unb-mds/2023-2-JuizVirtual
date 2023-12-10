from django.forms import CharField, FileField, Form
from djangocodemirror.fields import CodeMirrorField


class SubmissionForm(Form):
    code = CodeMirrorField(
        min_length=15,
        label="Code",
        required=True,
        config_name="python",
    )


class UploadFileForm(Form):
    title = CharField(max_length=255)
    file = FileField()
