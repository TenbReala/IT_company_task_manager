from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from task_manager.models import Worker, Position, Project, Task, Team, TaskType
from datetime import timedelta
from django.utils import timezone


class IndexViewTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Backend")
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Test123',
        )
        self.client.force_login(self.user)

        self.team = Team.objects.create(name="Test team")
        self.team.members.add(self.user)

        self.project = Project.objects.create(name="Test project")
        self.team.projects.add(self.project)

        self.task_type = TaskType.objects.create(name="Test task_type")
        self.task = Task.objects.create(
            name="Test task",
            task_type=self.task_type,
            deadline=timezone.now() + timedelta(days=1),
            project=self.project,
        )
        self.task.assignees.add(self.user)

    def test_index_context(self):
        response = self.client.get(reverse("task_manager:index"))
        self.assertEqual(response.status_code, 200)

        self.assertIn(self.task, response.context["my_tasks"])
        self.assertIn(self.task, response.context["upcoming_tasks"])
        self.assertIn(self.user, response.context["my_team"])
        self.assertIn(self.project, response.context["projects"])

