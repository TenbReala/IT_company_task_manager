from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import localtime

from task_manager.models import Position, Project, TaskType, Task


class TestTaskViews(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Dev")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
            position=self.position,
        )
        self.client.force_login(self.user)

        self.project1 = Project.objects.create(name="Project_1")
        self.task_type = TaskType.objects.create(name="Test Type")
        self.deadline_obj = localtime(timezone.now() + timedelta(days=1))
        self.deadline_str = self.deadline_obj.strftime("%Y-%m-%dT%H:%M")

        Task.objects.create(
            name="Done Task",
            deadline=self.deadline_obj,
            is_complete=True,
            task_type=self.task_type,
            project=self.project1,
        )

    def test_task_list_view_get_queryset(self):
        response = self.client.get(reverse("task_manager:task-list"), {"query": "Done Task"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Done Task")
        self.assertNotContains(response, "Task Two")

    def test_task_list_view_get_context_data(self):
        response = self.client.get(reverse("task_manager:task-list"), {"query": "Done Task"})
        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].data.get("query"), "Done Task")

    def test_task_create_view_get_context_data_with_project(self):
        url = reverse("task_manager:project-task-create", args=[self.project1.id])
        response = self.client.get(url)
        self.assertEqual(response.context["project_locked"], True)
        self.assertEqual(response.context["project_pk"], self.project1.id)

    def test_task_create_view_form_valid_sets_project(self):
        url = reverse("task_manager:project-task-create", args=[self.project1.id])
        data = {
            "name": "Fix login bug",
            "deadline": self.deadline_str,
            "task_type": self.task_type.id,
        }
        self.client.post(url, data)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.latest("id")
        self.assertEqual(task.project, self.project1)

    def test_task_create_view_get_success_url_redirects_to_project(self):
        url = reverse("task_manager:project-task-create", args=[self.project1.id])
        data = {
            "name": "Fix logout bug",
            "deadline": self.deadline_str,
            "task_type": self.task_type.id,
            "priority": "LOW",
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("task_manager:project-detail", args=[self.project1.id]))

    def test_task_create_view_get_success_url_default(self):
        url = reverse("task_manager:task-create")
        data = {
            "name": "Non-project task",
            "deadline": self.deadline_str,
            "task_type": self.task_type.id,
            "priority": "LOW",
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("task_manager:task-list"))

    def test_task_detail_view(self):
        task = Task.objects.create(
            name="Detail Task",
            deadline=self.deadline_obj,
            task_type=self.task_type,
            project=self.project1,
        )
        url = reverse("task_manager:task-detail", args=[task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Detail Task")

    def test_task_update_view(self):
        task = Task.objects.create(
            name="Old Name",
            deadline=self.deadline_obj,
            task_type=self.task_type,
            project=self.project1,
        )
        url = reverse("task_manager:task-update", args=[task.id])
        response = self.client.post(url, {
            "name": "Updated Name",
            "deadline": self.deadline_str,
            "task_type": self.task_type.id,
            "priority": "LOW",
        })
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.name, "Updated Name")

    def test_task_delete_view(self):
        task = Task.objects.create(
            name="To Delete",
            deadline=self.deadline_obj,
            task_type=self.task_type,
            project=self.project1,
        )
        url = reverse("task_manager:task-delete", args=[task.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_task_complete_view_marks_task_if_user_assigned(self):
        task = Task.objects.create(
            name="Complete Me",
            deadline=self.deadline_obj,
            task_type=self.task_type,
            project=self.project1,
            is_complete=False
        )
        task.assignees.add(self.user)

        url = reverse("task_manager:task-complete", args=[task.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertTrue(task.is_complete)

    def test_task_complete_view_does_not_complete_unassigned_task(self):
        task = Task.objects.create(
            name="Not Yours",
            deadline=self.deadline_obj,
            task_type=self.task_type,
            project=self.project1,
            is_complete=False
        )
        url = reverse("task_manager:task-complete", args=[task.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertFalse(task.is_complete)
