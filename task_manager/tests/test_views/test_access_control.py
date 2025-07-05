from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position, TaskType, Project, Task, Team


class TestLoginRequired(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name="Team 1")
        self.task_type = TaskType.objects.create(name="Test task type")
        self.task = Task.objects.create(
            name="Test task",
            task_type=self.task_type,
            deadline="2025-06-02T09:26:54.015362+00:00",
        )
        self.project = Project.objects.create(name="Test project", )
        self.position = Position.objects.create(name="Test position")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            position=self.position,
            password="test12",
        )

        self.urls = [
            reverse("task_manager:index"),
            reverse("task_manager:worker-list"),
            reverse("task_manager:worker-update", args=[self.user.id]),
            reverse("task_manager:worker-detail", args=[self.user.id]),
            reverse("task_manager:worker-delete", args=[self.user.id]),
            reverse("task_manager:projects-list"),
            reverse("task_manager:project-create"),
            reverse("task_manager:project-detail", args=[self.project.id]),
            reverse("task_manager:project-update", args=[self.project.id]),
            reverse("task_manager:project-delete", args=[self.project.id]),
            reverse("task_manager:project-task-create", args=[self.project.id]),
            reverse("task_manager:position-list"),
            reverse("task_manager:position-create"),
            reverse("task_manager:position-detail", args=[self.position.id]),
            reverse("task_manager:position-update", args=[self.position.id]),
            reverse("task_manager:position-delete", args=[self.position.id]),
            reverse("task_manager:task-type-list"),
            reverse("task_manager:task-type-create"),
            reverse("task_manager:task-type-detail", args=[self.task_type.id]),
            reverse("task_manager:task-type-update", args=[self.task_type.id]),
            reverse("task_manager:task-type-delete", args=[self.task_type.id]),
            reverse("task_manager:task-list"),
            reverse("task_manager:task-create"),
            reverse("task_manager:task-detail", args=[self.task.id]),
            reverse("task_manager:task-update", args=[self.task.id]),
            reverse("task_manager:task-delete", args=[self.task.id]),
            reverse("task_manager:team-list"),
            reverse("task_manager:team-create"),
            reverse("task_manager:team-detail", args=[self.team.id]),
            reverse("task_manager:team-delete", args=[self.team.id]),
        ]

    def test_login_required(self):
        for url in self.urls:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200, msg=f"{url} = {res.status_code}")
            self.assertEqual(res.status_code, 302, msg=f"{url} = {res.status_code}")
            self.assertRedirects(res, f"/accounts/login/?next={url}")

    def test_authenticated_user_access(self):
        self.client.force_login(self.user)
        for url in self.urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 302], msg=f"{url} = {response.status_code}")
