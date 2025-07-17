from django.test import TestCase
from django.contrib.auth import get_user_model

from task_manager.forms import WorkerCreationForm, WorkerUpdateForm, WorkerSearchForm
from task_manager.models import Position


class WorkerFormTestBase(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="QA")
        self.user_model = get_user_model()


class WorkerCreationFormTest(WorkerFormTestBase):

    def test_form_valid_data(self):
        form_data = {
            "username": "testuser",
            "password1": "Testpass123",
            "password2": "Testpass123",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "position": self.position.id,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_missing_required_fields(self):
        form = WorkerCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password1", form.errors)
        self.assertIn("password2", form.errors)


class WorkerUpdateFormTest(WorkerFormTestBase):

    def test_form_valid_update(self):
        user = self.user_model.objects.create_user(
            username="updatable",
            password="somepass",
            first_name="Old",
            last_name="Name",
            email="old@example.com",
            position=self.position,
        )
        form_data = {
            "username": "updated",
            "first_name": "New",
            "last_name": "Name",
            "email": "new@example.com",
            "position": self.position.id,
        }
        form = WorkerUpdateForm(instance=user, data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        updated_user = form.save()
        self.assertEqual(updated_user.username, "updated")
        self.assertEqual(updated_user.first_name, "New")


class WorkerSearchFormTest(TestCase):

    def test_form_is_valid_with_data(self):
        form = WorkerSearchForm(data={"query": "john"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["query"], "john")

    def test_form_is_valid_without_data(self):
        form = WorkerSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["query"], "")

    def test_widget_placeholder_and_class(self):
        form = WorkerSearchForm()
        query_field = form.fields["query"]
        self.assertEqual(query_field.widget.attrs["placeholder"], "Search workers...")
        self.assertIn("form-control", query_field.widget.attrs["class"])
