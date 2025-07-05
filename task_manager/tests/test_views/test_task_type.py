from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import TaskType, Position


class TestTaskTypeViews(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Test Type")
        self.position = Position.objects.create(name="Dev")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
            position=self.position,
        )
        self.client.force_login(self.user)

    def test_task_type_list_view(self):
        response = self.client.get(reverse("task_manager:task-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task_type.name)

    def test_task_type_create_view(self):
        response = self.client.post(reverse("task_manager:task-type-create"), {"name": "New Type"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TaskType.objects.filter(name="New Type").exists())

    def test_task_type_update_view(self):
        url = reverse("task_manager:task-type-update", args=[self.task_type.id])
        response = self.client.post(url, {"name": "Updated Type"})
        self.assertEqual(response.status_code, 302)
        self.task_type.refresh_from_db()
        self.assertEqual(self.task_type.name, "Updated Type")

    def test_task_type_delete_view(self):
        url = reverse("task_manager:task-type-delete", args=[self.task_type.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TaskType.objects.filter(id=self.task_type.id).exists())
