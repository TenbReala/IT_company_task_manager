from django.test import TestCase
from task_manager.forms import ProjectSearchForm


class ProjectSearchFormTest(TestCase):

    def test_form_is_valid_with_data(self):
        form = ProjectSearchForm(data={"query": "internal"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["query"], "internal")

    def test_form_is_valid_without_data(self):
        form = ProjectSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["query"], "")

    def test_widget_placeholder_and_class(self):
        form = ProjectSearchForm()
        query_field = form.fields["query"]
        self.assertEqual(query_field.widget.attrs["placeholder"], "Search project...")
        self.assertIn("form-control", query_field.widget.attrs["class"])
