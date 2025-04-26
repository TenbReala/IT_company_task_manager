from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from task_manager.models import Worker


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
    query = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={
        "placeholder": "Search workers...",
        "class": "form-control"
    }))


class TeamSearchForm(forms.Form):
    query = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={
        "placeholder": "Search team...",
        "class": "form-control"
    }))


class TaskSearchForm(forms.Form):
    query = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={
        "placeholder": "Search task...",
        "class": "form-control"
    }))


class ProjectSearchForm(forms.Form):
    query = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={
        "placeholder": "Search project...",
        "class": "form-control"
    }))

