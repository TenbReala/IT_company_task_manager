from django.test import TestCase
from task_manager.forms import TeamSearchForm


class TeamSearchFormTest(TestCase):

    def test_form_is_valid_with_data(self):
        form = TeamSearchForm(data={"query": "dev"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["query"], "dev")

    def test_form_is_valid_without_data(self):
        form = TeamSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["query"], "")

    def test_widget_placeholder_and_class(self):
        form = TeamSearchForm()
        query_field = form.fields["query"]
        self.assertEqual(query_field.widget.attrs["placeholder"], "Search team...")
        self.assertIn("form-control", query_field.widget.attrs["class"])
