from django import forms
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, datetime

from django.utils.timezone import localtime, make_aware

from task_manager.forms import TaskForm, TaskSearchForm
from task_manager.models import Task, TaskType, Worker, Project, Position


class TaskFormTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Backend")
        self.worker = Worker.objects.create_user(
            username="dev", password="test123", position=self.position
        )
        self.task_type = TaskType.objects.create(name="Bugfix")
        self.project = Project.objects.create(name="Test Project")

    def test_form_valid_with_full_data(self):
        data = {
            "name": "Fix bug",
            "description": "Fix login bug",
            "deadline": localtime(timezone.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M"),
            "is_complete": False,
            "priority": Task.Priority.HIGH,
            "task_type": self.task_type.id,
            "project": self.project.id,
            "assignees": [self.worker.id],
        }
        form = TaskForm(data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_project_field_removed_when_locked(self):
        form = TaskForm(project_locked=True)
        self.assertNotIn("project", form.fields)

    def test_deadline_initial_format(self):
        task = Task.objects.create(
            name="Deadline test",
            description="check format",
            deadline=make_aware(datetime.now() + timedelta(days=3)),
            is_complete=False,
            priority=Task.Priority.LOW,
            task_type=self.task_type,
            project=self.project,
        )
        form = TaskForm(instance=task)
        self.assertIn("deadline", form.initial)
        self.assertRegex(form.initial["deadline"], r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}")

    def test_deadline_widget_attrs(self):
        form = TaskForm()
        field = form.fields["deadline"]
        self.assertIsInstance(field.widget, forms.DateTimeInput)
        self.assertEqual(field.widget.input_type, "datetime-local")
        self.assertIn("form-control", field.widget.attrs.get("class", ""))


class TaskSearchFormTest(TestCase):
    def test_form_is_valid_with_data(self):
        form = TaskSearchForm(data={"query": "auth"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["query"], "auth")

    def test_form_is_valid_without_data(self):
        form = TaskSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["query"], "")

    def test_widget_placeholder_and_class(self):
        form = TaskSearchForm()
        query_field = form.fields["query"]
        self.assertEqual(query_field.widget.attrs["placeholder"], "Search task...")
        self.assertIn("form-control", query_field.widget.attrs["class"])
