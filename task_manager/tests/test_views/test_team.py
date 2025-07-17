from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Team


class TestTeamViews(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="test123"
        )
        self.client.force_login(self.user)

        self.team1 = Team.objects.create(name="Alpha Team")
        self.team2 = Team.objects.create(name="Beta Team")

    def test_team_list_view_get_queryset(self):
        url = reverse("task_manager:team-list")
        response = self.client.get(url, {"query": "Alpha"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alpha Team")
        self.assertNotContains(response, "Beta Team")

    def test_team_list_view_get_context_data(self):
        url = reverse("task_manager:team-list")
        response = self.client.get(url, {"query": "Alpha"})
        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].data.get("query"), "Alpha")

    def test_team_create_view(self):
        url = reverse("task_manager:team-create")
        response = self.client.post(url, {"name": "New Team"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(name="New Team").exists())

    def test_team_detail_view(self):
        url = reverse("task_manager:team-detail", args=[self.team1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.team1.name)

    def test_team_update_view(self):
        url = reverse("task_manager:team-update", args=[self.team1.pk])
        response = self.client.post(url, {"name": "Renamed Team"})
        self.assertEqual(response.status_code, 302)
        self.team1.refresh_from_db()
        self.assertEqual(self.team1.name, "Renamed Team")

    def test_team_delete_view(self):
        url = reverse("task_manager:team-delete", args=[self.team1.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Team.objects.filter(pk=self.team1.pk).exists())
