from django import forms
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Worker, Task


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
        )


class WorkerUpdateForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "email", "position")


class WorkerSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search workers...", "class": "form-control"}
        ),
    )


class TeamSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search team...", "class": "form-control"}
        ),
    )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        project_locked = kwargs.pop("project_locked", False)
        super().__init__(*args, **kwargs)
        deadline = self.initial.get("deadline") or self.instance.deadline
        if deadline:
            self.initial["deadline"] = deadline.strftime("%Y-%m-%dT%H:%M")

        if project_locked:
            self.fields.pop("project", None)


class TaskSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search task...", "class": "form-control"}
        ),
    )


class ProjectSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search project...", "class": "form-control"}
        ),
    )
