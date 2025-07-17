from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position


class TestPositionViews(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Dev")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
            position=self.position,
        )
        self.client.force_login(self.user)

    def test_position_list_view(self):
        response = self.client.get(reverse("task_manager:position-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.position.name)

    def test_position_create_view(self):
        url = reverse("task_manager:position-create")
        response = self.client.post(url, {"name": "New Position"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Position.objects.filter(name="New Position").exists())

    def test_position_update_view(self):
        url = reverse("task_manager:position-update", args=[self.position.id])
        response = self.client.post(url, {"name": "Updated Position"})
        self.assertEqual(response.status_code, 302)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Updated Position")

    def test_position_delete_view(self):
        url = reverse("task_manager:position-delete", args=[self.position.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Position.objects.filter(id=self.position.id).exists())
