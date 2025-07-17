from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from task_manager.models import Task, TaskType, Project


class TaskModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Refactor")
        self.project = Project.objects.create(name="Order Test Project")

    def test_str_representation(self):
        task = Task.objects.create(
            name="Code Review",
            description="Look at the PR",
            deadline=timezone.now() + timedelta(days=1),
            is_complete=False,
            priority=Task.Priority.MEDIUM,
            task_type=self.task_type,
            project=self.project,
        )
        expected = f"{task.name} {task.deadline} {task.priority} {task.is_complete}"
        self.assertEqual(str(task), expected)

    def test_ordering_by_is_complete(self):
        t1 = Task.objects.create(
            name="t1",
            description="...",
            deadline=timezone.now() + timedelta(days=1),
            is_complete=False,
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
            project=self.project,
        )
        t2 = Task.objects.create(
            name="t2",
            description="...",
            deadline=timezone.now() + timedelta(days=2),
            is_complete=True,
            priority=Task.Priority.LOW,
            task_type=self.task_type,
            project=self.project,
        )
        tasks = list(Task.objects.all())
        self.assertEqual(tasks[0], t1)
        self.assertEqual(tasks[1], t2)
