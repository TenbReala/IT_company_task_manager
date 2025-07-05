from django.test import TestCase
from task_manager.models import Project, TaskType, Task
from django.utils import timezone
from datetime import timedelta


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test Project")
        self.task_type = TaskType.objects.create(name="Bug")

    def test_str_representation(self):
        self.assertEqual(str(self.project), "Test Project")

    def test_progress_no_tasks(self):
        self.assertEqual(self.project.progress(), 0)

    def test_progress_with_tasks(self):
        now = timezone.now()
        Task.objects.create(
            name="task1",
            description="desc",
            deadline=now + timedelta(days=1),
            is_complete=True,
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
            project=self.project
        )
        Task.objects.create(
            name="task2",
            description="desc",
            deadline=now + timedelta(days=1),
            is_complete=True,
            priority=Task.Priority.MEDIUM,
            task_type=self.task_type,
            project=self.project
        )
        Task.objects.create(
            name="task3",
            description="desc",
            deadline=now + timedelta(days=1),
            is_complete=True,
            priority=Task.Priority.LOW,
            task_type=self.task_type,
            project=self.project
        )
        Task.objects.create(
            name="task4",
            description="desc",
            deadline=now + timedelta(days=1),
            is_complete=False,
            priority=Task.Priority.LOW,
            task_type=self.task_type,
            project=self.project
        )
        self.assertEqual(self.project.progress(), 75)
