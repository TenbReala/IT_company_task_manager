from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from task_manager.models import Position, Project, TaskType, Task


class TestProjects(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Dev")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
            position=self.position,
        )
        self.client.force_login(self.user)

        self.project1 = Project.objects.create(name="Project_1")
        self.project2 = Project.objects.create(name="Project_2")

        self.task_type = TaskType.objects.create(name="Test Type")
        Task.objects.create(
            name="Done Task",
            deadline=timezone.now() + timedelta(days=1),
            is_complete=True,
            task_type=self.task_type,
            project=self.project1,
        )
        Task.objects.create(
            name="Pending Task",
            deadline=timezone.now() + timedelta(days=2),
            is_complete=False,
            task_type=self.task_type,
            project=self.project1,
        )

    def test_listview_get_queryset(self):
        response = self.client.get(reverse("task_manager:projects-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Project_1")
        self.assertContains(response, "Project_2")

    def test_listview_get_context_data(self):
        response = self.client.get(
            reverse("task_manager:projects-list"), {"query": self.project1.name}
        )
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].data.get("query"), self.project1.name
        )
        self.assertTrue(response.context["search_form"].is_bound)

    def test_update_view(self):
        url = reverse("task_manager:project-update", args=[self.project1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project1.name)

    def test_detail_view_context_progress(self):
        response = self.client.get(
            reverse("task_manager:project-detail", args=[self.project1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("progress", response.context)
        self.assertEqual(response.context["progress"], 50)

    def test_create_view_post_valid_data(self):
        url = reverse("task_manager:project-create")
        response = self.client.post(url, {"name": "New Project"})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name="New Project").exists())

    def test_delete_view_post(self):
        url = reverse("task_manager:project-delete", args=[self.project1.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(id=self.project1.id).exists())
