from django.forms import Form
from djangocodemirror.fields import CodeMirrorField


class SubmissionForm(Form):
    code = CodeMirrorField(
        label="Code",
        required=True,
        config_name="python",
    )
